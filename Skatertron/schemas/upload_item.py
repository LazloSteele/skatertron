from pydantic import BaseModel, ConfigDict


class UploadItem(BaseModel):
    file_handle: str
    skate_id: str
