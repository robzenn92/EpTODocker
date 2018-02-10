#!/usr/bin/env python3

import structlog.dev
import logging.config
from sys import stdout
from os import environ

#: Default handler
LOGGING_DEFAULT_HANDLER = "console"

#: Default formatter
LOGGING_DEFAULT_FORMATTER = "STANDARD"


def get_logging_formatters():
    return {
        "MINIMAL": {
            "format": "%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "STANDARD": {
            "format": "[%(levelname)-7s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "VERBOSE": {
            "format": "%(asctime)s - %(name)s - %(levelname)-8s %(module)s %(process)d %(thread)d %(threadName)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
    }


def get_logging_handlers():
    handlers = {
        "console": {
            "level": environ['LOG_LEVEL'],
            "class": "logging.StreamHandler",
            "formatter": environ['LOG_FORMATTER'],
            "stream": stdout
        },
    }
    return handlers


def get_loggers():
    handlers = [LOGGING_DEFAULT_HANDLER]
    return {
        "": {
            "handlers": handlers,
            "level": environ['LOG_LEVEL'],
            "propagate": True
        }
    }


def get_dict_config():
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "root": {
            "level": environ['LOG_LEVEL'],
            "handlers": [LOGGING_DEFAULT_HANDLER]
        },
        "formatters": get_logging_formatters(),
        "handlers": get_logging_handlers(),
        "loggers": get_loggers()
    }


logging.config.dictConfig(get_dict_config())
log = logging.getLogger()

# structlog.configure_once(
#     processors=[
#         structlog.stdlib.add_log_level,
#         structlog.processors.KeyValueRenderer(),
#     ],
# )
logger = structlog.wrap_logger(log)
