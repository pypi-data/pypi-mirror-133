from .all_of_your_base import MetaBase


class PluginBase(MetaBase):
    # plugin profile schema is intended to be defined at startup-time once. This should include things that
    # never change usecase to usecase and span the entire lifecycle of the service. Such as default
    # authentication credentials for a service account or AWS region of the SNS instance.

    def __init__(self, **plugin_profile):
        self._validate_profile(profile=plugin_profile, schema=self.PLUGIN_PROFILE_SCHEMA)
        self.plugin_profile = plugin_profile
