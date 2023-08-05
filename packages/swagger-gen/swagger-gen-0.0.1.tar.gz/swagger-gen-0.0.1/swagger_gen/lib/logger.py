from typing import List
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging

MODULE_LOGGER = 'swagger_gen'


def _get_console_handler() -> logging.StreamHandler:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s: %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)

    return handler


def _get_logger():
    logger = logging.getLogger(MODULE_LOGGER)
    logger.setLevel(logging.INFO)
    logger.addHandler(_get_console_handler())

    return logger


_logger = _get_logger()


def get_logger():
    return _logger

# class LoggerProvider:
#     def __init__(self, level: int = logging.ERROR):
#         self._level = level
#         self._module_loggers: List[logging.Logger] = []

#     def get_logger(self, name: str):
#         logger = self._create_logger(name)
#         self._module_loggers.append(logger)
#         return logger

#     def set_level(self, level: int):
#         self._level = level

#         for _logger in self._module_loggers:
#             print('setting logger')
#             _logger.setLevel(self._level)

#     def _get_console_handler(self) -> logging.StreamHandler:
#         handler = logging.StreamHandler()
#         formatter = logging.Formatter(
#             '%(asctime)s %(name)-12s: %(levelname)-8s %(message)s')
#         handler.setFormatter(formatter)

#         return handler

#     def _create_logger(self, name: str):
#         logger = logging.getLogger(name)
#         logger.setLevel(self._level)
#         logger.addHandler(self._get_console_handler())

#         return logger


# logger_provider = LoggerProvider()
