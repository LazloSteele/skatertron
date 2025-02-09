from enum import Enum


class FootageExceptions(Enum):
    SCRATCH = 'SCRATCH'
    NO_VIDEO = 'NO_VIDEO'
    NO_PHOTO = 'NO_PHOTO'
    MULTIPLE_VIDEOS = 'MULTIPLE_VIDEOS'
    