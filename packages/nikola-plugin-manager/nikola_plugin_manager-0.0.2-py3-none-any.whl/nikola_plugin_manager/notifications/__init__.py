from ..plugin_base import PluginBase


# All functions must be installed on all plugins.
class NotificationPluginBase(PluginBase):
    PLUGIN_PROFILE_SCHEMA = {}

    def send_message(self, **plugin_profile):
        raise NotImplementedError("Send Message function is not implemented")
