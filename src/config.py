import logging
import os
from datetime import datetime

from args import cmd_args
from src.core.project_state import ProjectState

# Other
ENCODING = "utf-8"

# Version
VERSION = (0, 1, 0)

# Root
ROOT_DIR = os.getcwd()
SRC_DIR = os.path.join(ROOT_DIR, 'src')

# State
STATE = cmd_args.state

# Secrets
SECRETS_DIR = os.path.join(ROOT_DIR, 'secrets')
DEBUG_SECRETS_PATH = os.path.join(SECRETS_DIR, 'dev.json')
PRODUCTION_SECRETS_PATH = os.path.join(SECRETS_DIR, 'prod.json')
SECRET_CONFIG_PATH = DEBUG_SECRETS_PATH if STATE is not ProjectState.PRODUCTION else PRODUCTION_SECRETS_PATH

# Configs
CONFIGS_DIR = os.path.join(ROOT_DIR, 'configs')
STATUS_CODES_CONFIG_PATH = os.path.join(CONFIGS_DIR, 'status_codes.json')

# Logs
CONSOLE_LOG_LEVEL = logging.DEBUG
FILE_LOG_LEVEL = logging.DEBUG
LOGS_DIR = os.path.join(ROOT_DIR, 'logs')
CURRENT_PROCESS_LOGS_DIR = os.path.join(LOGS_DIR, datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
LATEST_LOG_FILE_PATH = os.path.join(LOGS_DIR, 'latest_debug.log')
LATEST_LOG_MAX_FILE_SIZE = 1024 * 1024 * 20  # 20MB
LATEST_LOG_BACKUP_COUNT = 1  # 1 backup file
APPLICATION_LOG_FILE_PATH = os.path.join(CURRENT_PROCESS_LOGS_DIR, 'debug.log')
APPLICATION_LOG_MAX_FILE_SIZE = 1024 * 1024 * 50  # 50MB
APPLICATION_LOG_BACKUP_COUNT = 2  # 2 backup files

# Server
HOST = "0.0.0.0"
PORT = 8000

# Redis
REDIS_ENCODING = ENCODING
MAX_STORAGE_CAPACITY = 2000

REDIS_DB_AUTH = 0
REDIS_DB_DATA = 1

# Auth
ACCESS_TOKEN_EXPIRE = 6 * 60 * 60  # 6h
REFRESH_TOKEN_EXPIRE = 1 * 60 * 60 * 24 * 90  # 90d
REFRESH_TOKEN_REDIS_TTL = REFRESH_TOKEN_EXPIRE
ACCESS_TOKEN_REDIS_TTL = ACCESS_TOKEN_EXPIRE

# Devices
DEVICE_PAIR_REQUEST_TTL = 20
