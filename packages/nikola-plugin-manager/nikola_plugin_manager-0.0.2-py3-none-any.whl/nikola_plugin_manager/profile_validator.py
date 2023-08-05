from jsonschema import Draft7Validator
from jsonschema.exceptions import ValidationError


class ProfileValidator:
    def __init__(self, profile, schema):
        self._profile = profile
        self._schema = schema

    def validate(self):
        results = [i for i in Draft7Validator(schema=self._schema).iter_errors(self._profile)]
        if len(results) == 1:
            raise ValidationError(results[0].message)
        elif results:
            raise ValidationError(f"Some errors were encountered:\n{[i.message for i in results]}")
