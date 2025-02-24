from pydantic import BaseModel, ConfigDict, conint


class Skate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    event_id: conint(strict=True)
    skater_name: str
    no_video: bool
    skate_position: int
