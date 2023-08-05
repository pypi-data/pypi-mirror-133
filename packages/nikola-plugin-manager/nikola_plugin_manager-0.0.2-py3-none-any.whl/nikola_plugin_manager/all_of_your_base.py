from .profile_validator import ProfileValidator


class MetaBase:
    def _validate_profile(self, profile, schema):
        return ProfileValidator(profile=profile, schema=schema).validate()
