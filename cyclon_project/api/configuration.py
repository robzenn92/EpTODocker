#!/usr/bin/env python3

#  -----
# Log configuration
#  -----

# class LogProcessorIp:
#     def __call__(self, _logger, _log_method, event_dict):
#         event_dict['ip'] = os.environ['MY_POD_IP']
#         return event_dict

# structlog.configure(
#     processors=[LogProcessorIp()],
#     context_class=dict
# )

# def proc(logger, method_name, event_dict):
#     return repr(event_dict)
#
#
# def proc_ip(logger, method_name, event_dict):
#     event_dict['ip'] = os.environ['MY_POD_IP']
#     return event_dict

# logger = logging.getLogger()
# logger.setLevel(os.environ['LOG_LEVEL'])
# logger_handler = logging.StreamHandler()
# logger_handler.setFormatter(logging.Formatter(os.environ['LOG_FORMAT'], datefmt=os.environ['LOG_DATE_FORMAT']))
# logger.addHandler(logger_handler)

# logging.basicConfig(
#     level=os.environ['LOG_LEVEL'],
#     format=os.environ['LOG_FORMAT'],
#     datefmt=os.environ['LOG_DATE_FORMAT'],
#     handlers=[logging.StreamHandler()]
# )
#
# structlog.configure(context_class=dict)
# logger = structlog.wrap_logger(logger)
#
# logger.critical('hello world', user="Pippo", name="asdasda", coust="asdadasdsaddasdads")

# structlog.configure(
#     processors=[
#         structlog.stdlib.add_logger_name,
#         structlog.stdlib.add_log_level,
#         structlog.stdlib.PositionalArgumentsFormatter(),
#         structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M.%S"),
#         structlog.processors.StackInfoRenderer(),
#         # structlog.processors.format_exc_info
#     ],
#     # context_class=dict,
#     logger_factory=structlog.stdlib.LoggerFactory(),
#     wrapper_class=structlog.stdlib.BoundLogger,
#     cache_logger_on_first_use=True,
# )

# timestamper = structlog.processors.TimeStamper(fmt=os.environ['LOG_FORMAT'])
# pre_chain = [
#     # Add the log level and a timestamp to the event_dict if the log entry
#     # is not from structlog.
#     structlog.stdlib.add_log_level,
#     timestamper,
# ]
#
# log = logging.getLogger()
#
# # log.setLevel(os.environ['LOG_LEVEL'])
# # logger_handler = logging.StreamHandler()
# # logger_handler.setFormatter(logging.Formatter(os.environ['LOG_FORMAT'], datefmt=os.environ['LOG_DATE_FORMAT']))
# # log.addHandler(logger_handler)
#
# logging.config.dictConfig({
#         "version": 1,
#         "disable_existing_loggers": False,
#         "formatters": {
#             "my": {
#                 "()": structlog.stdlib.ProcessorFormatter,
#                 "processor": structlog.dev.ConsoleRenderer(colors=False),
#                 "format": os.environ['LOG_FORMAT'],
#                 "datefmt": os.environ['LOG_DATE_FORMAT']
#             }
#             # "plain": {
#             #     "()": structlog.stdlib.ProcessorFormatter,
#             #     "processor": structlog.dev.ConsoleRenderer(colors=False),
#             #     "foreign_pre_chain": pre_chain
#             # },
#             # "colored": {
#             #     "()": structlog.stdlib.ProcessorFormatter,
#             #     "processor": structlog.dev.ConsoleRenderer(colors=True),
#             #     "foreign_pre_chain": pre_chain,
#             # },
#         },
#         "handlers": {
#             "default": {
#                 "level": os.environ['LOG_LEVEL'],
#                 "class": "logging.StreamHandler",
#                 "formatter": "my",
#             },
#             # "file": {
#             #     "level": os.environ['LOG_LEVEL'],
#             #     "class": "logging.handlers.WatchedFileHandler",
#             #     "filename": "test.log",
#             #     "formatter": "plain",
#             # },
#         },
#         "loggers": {
#             "": {
#                 "handlers": ["default"],
#                 "level": os.environ['LOG_LEVEL'],
#                 "propagate": True,
#             },
#         }
# })
#
# structlog.configure_once(
#     processors=[
#         structlog.stdlib.add_log_level,
#         # structlog.stdlib.PositionalArgumentsFormatter(),
#         # structlog.processors.StackInfoRenderer(),
#         structlog.processors.format_exc_info,
#         structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
#     ],
#     context_class=dict,
#     # logger_factory=structlog.stdlib.LoggerFactory(),
#     wrapper_class=structlog.stdlib.BoundLogger,
#     cache_logger_on_first_use=True,
# )

# from structlog import wrap_logger, PrintLogger
# from structlog.processors import JSONRenderer

# logger = wrap_logger(PrintLogger(), processors=[JSONRenderer()])

# structlog.configure_once(
#     processors=[
#         structlog.stdlib.add_log_level,
#         structlog.processors.JSONRenderer(),
#         # structlog.stdlib.PositionalArgumentsFormatter(),
#         # structlog.processors.StackInfoRenderer(),
#         # structlog.processors.format_exc_info,
#         # structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
#     ],
#     # context_class=dict,
#     # logger_factory=structlog.stdlib.LoggerFactory(),
#     # wrapper_class=structlog.stdlib.BoundLogger,
#     cache_logger_on_first_use=True,
# )

import sys
import logging.config
import structlog.dev

#: Default handler
LOGGING_DEFAULT_HANDLER = "console"

#: Default formatter
LOGGING_DEFAULT_FORMATTER = "console"


def get_logging_formatters():
    return {
        "minimal": {
            "format": "%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "standard": {
            "format": "%(asctime)s - %(levelname)-5s [%(filename)s:%(lineno)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "verbose": {
            "format": "%(asctime)s - %(levelname)-5s %(module)s [%(filename)s:%(lineno)s] %(process)d %(thread)d %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "console": {
            "format": "%(asctime)s - %(levelname)-5s [%(filename)s:%(lineno)s] %(message)s",
            "datefmt": "%H:%M:%S"
        }
    }


def get_logging_handlers():
    handlers = {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "minimal",
            "stream": sys.stdout
        },
    }
    return handlers


def get_loggers():
    handlers = [LOGGING_DEFAULT_HANDLER]
    return {
        "": {
            "handlers": handlers,
            "level": "INFO",
            "propagate": True
        },
    }


def get_dict_config():
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "root": {
            "level": "INFO",
            "handlers": [LOGGING_DEFAULT_HANDLER],
        },
        "formatters": get_logging_formatters(),
        "handlers": get_logging_handlers(),
        "loggers": get_loggers()
    }


logging.config.dictConfig(get_dict_config())
log = logging.getLogger()

# structlog.configure_once(
#     processors=[
#         structlog.stdlib.add_log_level
#     ],
#     # context_class=dict,
#     # logger_factory=structlog.stdlib.LoggerFactory(),
#     # wrapper_class=structlog.stdlib.BoundLogger,
#     cache_logger_on_first_use=True
# )
#
# logger = structlog.wrap_logger(log)

logger = structlog.wrap_logger(log)
logger.info("LOOOOL")
