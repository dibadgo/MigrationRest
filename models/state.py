from enum import Enum


class MigrationState(Enum):
    NOT_STARTED = 'NOT_STARTED'
    RUNNING = 'RUNNING'
    ERROR = 'ERROR'
    SUCCESS = 'SUCCESS'