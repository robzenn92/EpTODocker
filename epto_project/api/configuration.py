#!/usr/bin/env python3

import os
import logging

# ---------------------
# Environment variables
# ---------------------

# Default values for log
DEFAULT_LOG_LEVEL = 'INFO'
DEFAULT_LOG_FORMAT = '[%(asctime)s.%(msecs)03d - %(levelname)s] %(filename)s:%(lineno)d | %(funcName)s - %(message)s'
DEFAULT_LOG_DATE_FORMAT = '%Y-%m-%d,%H:%M:%S'

LOG_LEVEL = os.environ['LOG_LEVEL'] if 'LOG_LEVEL' in os.environ else DEFAULT_LOG_LEVEL
LOG_FORMAT = os.environ['LOG_FORMAT'] if 'LOG_FORMAT' in os.environ else DEFAULT_LOG_FORMAT
LOG_DATE_FORMAT = os.environ['LOG_DATE_FORMAT'] if 'LOG_DATE_FORMAT' in os.environ else DEFAULT_LOG_DATE_FORMAT

# Constant to have a K and TTL meeting an expected delivery ratio
DEFAULT_CONSTANT = 2
CONSTANT = os.environ['CONSTANT'] if 'CONSTANT' in os.environ else DEFAULT_CONSTANT

# -----
# Log configuration
# -----

logger = logging.getLogger()
logger.handlers = []
logger.setLevel(LOG_LEVEL)
logger_handler = logging.StreamHandler()
logger_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT))
logger.addHandler(logger_handler)
