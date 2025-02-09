from enum import Enum


class FileStatus(Enum):
    STAGED = 'STAGED'
    IN_PROGRESS = 'IN_PROGRESS'
    FINISHED = "FINISHED"
    ABORTED = "ABORTED"
    UPLOAD_ERROR = "UPLOAD_ERROR"
