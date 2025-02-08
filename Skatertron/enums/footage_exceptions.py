from enum import Enum


class FootageExceptions(Enum):
    SCRATCH = 'scratch'
    NO_VIDEO = 'no video'
    NO_PHOTO = 'no photo'
    MULTIPLE_VIDEOS = 'multiple videos'
    