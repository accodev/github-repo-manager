import logging
import importlib

from action import Action

logger = logging.getLogger()


class NoActionFoundError(Exception):
    pass


def try_import(name: str) -> [object, None]:
    try:
        logger.debug(f'Trying to import {name} module')
        module = importlib.import_module(name)
        logger.debug(f'Module {name} imported')
        return module
    except ModuleNotFoundError:
        logger.debug(f'Could not import {name}')
        return None


def build(name: str, repo) -> Action:
    import sys
    import os
    import pathlib

    actions_dir = os.path.join(pathlib.Path(__file__).parent.resolve(), 'actions')
    logger.debug(f'Adding {actions_dir} to path')
    if actions_dir not in sys.path:
        sys.path.extend(*[actions_dir])

    module = try_import(f'actions.{name}action')
    if not module:
        module = try_import(f'actions.{name}')

    if not module:
        raise NoActionFoundError()

    logger.debug(f'Calling module.build()')
    return module.build(name, repo)
