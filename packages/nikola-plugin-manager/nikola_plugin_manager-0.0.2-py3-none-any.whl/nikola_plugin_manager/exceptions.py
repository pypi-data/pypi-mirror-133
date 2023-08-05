class PluginNotInstalledError(Exception):
    pass


class PluginCorruptError(Exception):
    pass


class NoSuchActionException(Exception):
    pass


class InvalidProfileException(Exception):
    pass
