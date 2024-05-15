from pydantic import BaseModel, ConfigDict


class Skate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    event_id: int
    skater_name: str
