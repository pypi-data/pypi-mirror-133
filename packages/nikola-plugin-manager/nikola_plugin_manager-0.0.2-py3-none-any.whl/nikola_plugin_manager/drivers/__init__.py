from ..plugin_base import PluginBase


class DriverPluginBase(PluginBase):
    PLUGIN_PROFILE_SCHEMA = {}

    TASK_DATA_KEY = 'TASK_DATA'
    MONITOR_DATA_KEY = 'MONITOR_DATA'
    CALLBACK_URL_KEY = 'POSTBACK_URL'
    JOB_ID_KEY = 'JOB_ID'

    def run_job(self, **plugin_profile):
        raise NotImplementedError("Run job function is not implemented")

    def monitor_job(self, **plugin_profile):
        raise NotImplementedError("Monitor job function is not implemented")
