import datetime

from pydantic import BaseModel, ConfigDict
from Skatertron.enums.file_status import FileStatus


class File(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    skate_id: int
    file_name: str
    file_path: str
    file_type: str
    creation_time: datetime.datetime
    file_status_enum: FileStatus
