from enum import Enum


class MigrationState(str, Enum):
    """The model to describe the migration states"""

    NOT_STARTED = 'NOT_STARTED'
    RUNNING = 'RUNNING'
    ERROR = 'ERROR'
    SUCCESS = 'SUCCESS'