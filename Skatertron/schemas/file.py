from pydantic import BaseModel, ConfigDict


class File(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    skate_id: int
    file_name: str
    file_path: str
    file_type: str
