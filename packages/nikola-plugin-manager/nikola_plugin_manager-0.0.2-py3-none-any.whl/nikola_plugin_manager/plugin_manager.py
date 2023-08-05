import importlib
import os

from .exceptions import (
    InvalidProfileException,
    NoSuchActionException,
    PluginCorruptError,
    PluginNotInstalledError
)
from .plugin_base import PluginBase
from .profile_validator import ProfileValidator


class PluginManager:
    def __init__(self, plugins: list[str], plugin_name: str) -> None:
        """[summary]
        Initiates the plugin manager. The plugin manager is responsible for working within an application with
        various plugins for a given plugin type. Each plugin is abstracted from the application to common intent
        functions.

        Args:
            plugins ([type] list[str]): [description] A List of strings for each plugin to manage
            plugin_name ([type] str): [description] The plugin that the caller is interested in.
                (E.G. cxr_notification_plugin_sns)

        Raises:
            PluginNotInstalledError: [description] If the plugin_name is not within the plugins list
            PluginCorruptError: [description] If the plugin is corrupted by either not containing a plugin which
                inherits from the base plugin class or the plugin inherits too many times from the base plugin class
        """
        self.plugin_name = plugin_name
        if self.plugin_name not in plugins:
            raise PluginNotInstalledError(f"Plugin {self.plugin_name} is not an installed plugin.")

        self._plugin_module = importlib.import_module(self.plugin_name)

        # Get plugin main class by searching for classes that inherit from PluginBase
        bases = []
        for i in dir(self._plugin_module):
            attr = getattr(self._plugin_module, i)
            isclass = isinstance(attr, type)
            if isclass and issubclass(attr, PluginBase) and not attr.__module__.startswith('nikola_plugin_manager.'):
                bases.append(attr)

        if not bases:
            raise PluginCorruptError(f"Plugin {self.plugin_name} does not contain a base plugin class.")
        elif len(bases) > 1:
            raise PluginCorruptError(f"Plugin {self.plugin_name} contains more than one base plugin class.")

        self._plugin_class = bases[0]
        self._plugin_profile_schema = self._plugin_class.PLUGIN_PROFILE_SCHEMA

        if 'properties' not in self._plugin_profile_schema:
            raise InvalidProfileException(
                f"All profiles must have a properties key at the top level: {self._plugin_profile_schema}"
            )

        self.plugin_profile = {key: os.environ[key] for key in self._plugin_profile_schema['properties']}

        # Validate the plugin profile schema
        ProfileValidator(profile=self.plugin_profile, schema=self._plugin_profile_schema).validate()

        self._plugin = self._plugin_class(**self.plugin_profile)

    def action(self, action, **action_profile):
        func = getattr(self._plugin, action)
        if not func:
            # This should be caught by plugin base during development. All actions should be validated via an interface.
            raise NoSuchActionException(f'Action {action} on plugin {self._plugin} does not exist.')

        return func(**action_profile)
