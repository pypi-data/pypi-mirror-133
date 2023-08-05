import json

import docker
from nikola_plugin_manager import PluginActionBase, logger

from ..responses import MonitorJobResponse


class MonitorJob(PluginActionBase):
    """
    Describe the action here
    """
    ACTION_PROFILE_SCHEMA = {
        'title': 'Nikola Docker Driver Plugin Run Job Action Schema',
        'type': 'object',
        'properties': {
            'callbackUrl': {
                'type': 'string',
                'format': 'uri',
                'description': 'The callback URL to post data to on job state change.'
            },
            'monitorData': {
                'type': 'object',
                'description': 'This is all the data that may be needed by the monitor to perform its duty.'
                               'It will be stored in a JSON string in the MONITOR_DATA env variable inside the '
                               'monitor container.'
            }
        },
        'additionalProperties': False,
        'required': ['callbackUrl']
    }

    def __init__(self, plugin, **action_profile):
        self._plugin = plugin
        super().__init__(**action_profile)

    def _prune_networks(self, prefix):
        logger.info(f"Pruning networks with prefix '{prefix}'")
        count = 0
        for n in self._plugin._client.networks.list(filters={'name': prefix}):
            try:
                n.remove()
                count += 1
            except docker.errors.APIError:
                # Ignore errors, probably an in-use network for a container that's still running.
                pass

        return count

    def __call__(self):
        logger.info(
            f'Starting monitor for {self._plugin.plugin_profile["correlationId"]} '
            f'with image {self._plugin.external_monitoring_image}'
        )
        monitoringJob = f'{self._plugin.NETWORK_PREFIX}{self._plugin.plugin_profile["correlationId"]}__monitor'
        jobId = f'{self._plugin.NETWORK_PREFIX}{self._plugin.plugin_profile["correlationId"]}__job'

        logger.info('Pruning networks before starting job.')
        count = self._prune_networks(self._plugin.NETWORK_PREFIX)
        logger.info(f'Pruned {count} networks')

        logger.info('Creating network')
        network_object = self._plugin._client.networks.create(name=monitoringJob)
        logger.info(f'Created networks {network_object.id}')

        container = self._plugin._client.containers.run(
            name=monitoringJob,
            image=self._plugin.external_monitoring_image,
            environment={
                self._plugin.JOB_ID_KEY: jobId,
                self._plugin.CALLBACK_URL_KEY: self.action_profile['callbackUrl'],
                self._plugin.MONITOR_DATA_KEY: json.dumps(self.action_profile.get('monitorData', {})),
            },
            # Use a new network for each container so it's isolated
            network=monitoringJob,
            detach=True,
            # The only way for docker to monitor the containers is if the socket from this environment is mounted
            # inside of that container. Get the socket from the client and mount it.
            volumes=['/var/run/docker.sock:/var/run/docker.sock']
        )

        logger.info(f'Monitor status: {container.status}')
        logger.info('Done starting monitor')

        return MonitorJobResponse({'monitor': container})
