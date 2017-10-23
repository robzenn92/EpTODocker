#!/usr/bin/env python2

import os
import logging

#  -----
# Log configuration
#  -----
logger = logging.getLogger()
logger.setLevel(os.environ['LOG_LEVEL'])
logger_handler = logging.StreamHandler()
logger_handler.setFormatter(logging.Formatter(os.environ['LOG_FORMAT'], datefmt=os.environ['LOG_DATE_FORMAT']))
logger.addHandler(logger_handler)
