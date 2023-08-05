# -*- coding: utf-8 -*-
import logging
from .bot import Bot

__author__ = 'luckydonald'
__version__ = "5.6"
__all__ = ["api_types", "bot", "Bot"]
VERSION = __version__

API_VERSION = "5" + "." + "6"  # so the bumpversion script doesn't breaks this accidentally.
API_DATE = "December 30, 2021"

logger = logging.getLogger(__name__)
logger.debug('pytgbot version {pytgbot} (API {api}, {api_date})'.format(
    pytgbot=__version__, api=API_VERSION, api_date=API_DATE
))
