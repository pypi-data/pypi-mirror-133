from .all_of_your_base import MetaBase


class PluginActionBase(MetaBase):

    def __init__(self, **action_profile):
        self._validate_profile(profile=action_profile, schema=self.ACTION_PROFILE_SCHEMA)
        self.action_profile = action_profile
