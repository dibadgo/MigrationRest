from enum import Enum


class MigrationState(str, Enum):
    NOT_STARTED = 'NOT_STARTED'
    RUNNING = 'RUNNING'
    ERROR = 'ERROR'
    SUCCESS = 'SUCCESS'