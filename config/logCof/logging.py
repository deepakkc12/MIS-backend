import logging
import os
from datetime import datetime
from pathlib import Path
from .dailyFileHandler import DailyFileHandler

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent  # Adjust as needed
LOG_DIR = BASE_DIR / 'logs'

def get_daily_handler(**kwargs):
    folder_path = kwargs.get('folder_path')
    level = kwargs.get('level', 'INFO')
    handler = DailyFileHandler(folder_path)
    handler.setLevel(level)
    formatter = logging.Formatter('{asctime} [{levelname}] {name} - {message}', style='{')
    handler.setFormatter(formatter)
    return handler


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'info_file': {
            '()': get_daily_handler,
            'folder_path': str(LOG_DIR / 'info'),
            'level': 'INFO',
        },
        'warning_file': {
            '()': get_daily_handler,
            'folder_path': str(LOG_DIR / 'warning'),
            'level': 'WARNING',
        },
        'error_file': {
            '()': get_daily_handler,
            'folder_path': str(LOG_DIR / 'error'),
            'level': 'ERROR',
        },
    },
    'loggers': {
        '': {
            'handlers': ['info_file', 'warning_file', 'error_file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
