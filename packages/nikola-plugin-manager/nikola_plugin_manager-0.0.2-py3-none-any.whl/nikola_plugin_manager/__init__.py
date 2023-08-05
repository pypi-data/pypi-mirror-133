import logging

from .action_base import PluginActionBase  # noqa: F401
from .plugin_base import PluginBase  # noqa: F401
from .plugin_manager import PluginManager  # noqa: F401

logger = logging.getLogger('nikola_plugin_manager')
formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')


if __name__ == '__main__':
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
