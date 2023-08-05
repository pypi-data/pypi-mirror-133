import docker
from nikola_plugin_manager.drivers import DriverPluginBase

from .actions import MonitorJob, RunJob


class DockerPlugin(DriverPluginBase):
    NETWORK_PREFIX = 'nikola_'
    # TODO: rename nikola_plugin_docker_driver_monitor
    external_monitoring_image = '642342036691.dkr.ecr.us-east-1.amazonaws.com/cxr_docker_driver_monitor:0.0.1'
    PLUGIN_PROFILE_SCHEMA = {
        'type': 'object',
        'properties': {
            'baseUrl': {
                'type': 'string',
                'description': 'URL to the Docker server. For example, unix:///var/run/docker.sock'
            },
            'correlationId': {
                'type': 'string',
                'format': '[a-zA-Z0-9][a-zA-Z0-9_.-]+',
                'description': 'This is the correlation ID for the job to run.'
                               'It can be used for correlation of other related tasks such as in a sidecar pattern.'
                               'It is assumed that the same correlationId will have been sent to the run_job'
                               'action using this plugin'
            },
        },
        'additionalProperties': False,
        'required': ['correlationId']
    }

    def __init__(self, **plugin_profile):
        super().__init__(**plugin_profile)

        self._client = docker.DockerClient(
            **({'base_url': plugin_profile['baseUrl']} if plugin_profile.get('baseUrl') else {})
        )

        self.monitoring_supported = True
        self.sidecars_supported = True

    def run_job(self, **action_profile):
        return RunJob(plugin=self, **action_profile)()

    def monitor_job(self, **action_profile):
        return MonitorJob(plugin=self, **action_profile)()
