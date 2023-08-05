import json

import docker
from nikola_plugin_manager import PluginActionBase, logger

from ..responses import RunJobResponse

# https://docker-py.readthedocs.io/en/stable/containers.html
# There's a lot of options for this action. Add the ones we need for now and we can expand it to include
# additional items as the need grows.


class RunJob(PluginActionBase):
    """
    Describe the action here
    """
    ACTION_PROFILE_SCHEMA = {
        'title': 'Nikola Docker Driver Plugin Run Job Action Schema',
        'type': 'object',
        'properties': {
            'taskData': {
                'type': 'object',
                'description': 'This is the data that is put sent into the docker container.'
                               "This data is what drives the container's logical function."
            },
            'image': {
                'type': 'string',
                'description': 'The image to run'
            },
            'command': {
                'oneOf': [
                    {'type': 'string'},
                    {'type': 'array', 'items': [{'type': 'string'}]}
                ],
                'description': 'The command to run in the container'
            },
            'environment': {
                'oneOf': [
                    {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'description': 'in the format ["SOMEVARIABLE=xxx"]'
                    },
                    {'type': 'object'}
                ],
                'description': 'Environment variables to set inside the container, as a dictionary or a list of strings'
            },
            'labels': {
                'oneOf': [
                    {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'description': 'list of names of labels to set with empty values (e.g. ["label1", "label2"])'
                    },
                    {
                        'type': 'object',
                        'description': 'A dictionary of name-value labels '
                                       '(e.g. {"label1": "value1", "label2": "value2"})'
                    }
                ]
            },
            'user': {
                'oneOf': [
                    {'type': 'string'},
                    {'type': 'number'}
                ],
                'description': 'Username or UID to run commands as inside the container'
            },
            'stdinOpen': {
                'type': 'boolean',
                'description': 'Keep STDIN open even if not attached.'
            },
            'tty': {
                'type': 'boolean',
                'description': 'Allocate a pseudo-TTY.'
            },
            'auth': {
                'type': 'object',
                'description': 'If set, used to login to a docker registry before pulling the image',
                'required': ['username', 'password', 'registry'],
                'properties': {
                    'username': {
                        'type': 'string',
                        'description': 'Username to login to the registry with'
                    },
                    'password': {
                        'type': 'string',
                        'description': 'Password to login to the registry with'
                    },
                    'registry': {
                        'type': 'string',
                        'description': 'Registry to pull a private image from'
                    }
                }
            },
        },
        'additionalProperties': False,
        'required': ['image']
    }

    def __init__(self, plugin, **action_profile):
        super().__init__(**action_profile)
        self._plugin = plugin

        self.correlation_id = self._plugin.plugin_profile['correlationId']
        self.private_networking = self._plugin.plugin_profile.get('privateNetworking', False)

        # Convert to non-camel case for injection to the api (devnet requires camel case for api compliance)
        if self.action_profile.get('stdinOpen'):
            self.action_profile['stdin_open'] = self.action_profile.pop('stdinOpen')

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
        logger.info(f'Starting task {self.correlation_id} with image {self.action_profile["image"]}')
        network = f'{self._plugin.NETWORK_PREFIX}{self.correlation_id}__job'
        self.action_profile['name'] = network

        logger.info('Pruning networks before starting job.')
        count = self._prune_networks(self._plugin.NETWORK_PREFIX)
        logger.info(f'Pruned {count} networks')

        logger.info('Creating network')
        network_object = self._plugin._client.networks.create(name=network)
        self.action_profile['network'] = network
        logger.info(f'Created networks {network_object.id}')

        logger.info('Preparing task data')
        self.action_profile['environment'] = self.action_profile.get('environment', {})
        taskData = json.dumps(self.action_profile.pop('taskData', {}))
        self.action_profile['environment'][self._plugin.TASK_DATA_KEY] = taskData

        if self.action_profile.get('auth'):
            # TODO: This will store the credentials in plaintext inside the container
            # Need to invesgitate if there's a way to securely pull a private image without storing the credentials
            # We should use credential helpers:
            # https://hackernoon.com/getting-rid-of-docker-plain-text-credentials-88309e07640d
            logger.info('Logging in Docker Client')
            self._plugin._client.login(**self.action_profile.pop('auth'))

        logger.info('Starting job')
        container = self._plugin._client.containers.run(**self.action_profile, detach=True)

        logger.info(f'Job status: {container.status}')
        logger.info('Done starting job')

        return RunJobResponse({
            'correlationId': self.correlation_id,
            'job': container
        })
