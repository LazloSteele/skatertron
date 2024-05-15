from pydantic import BaseModel, ConfigDict


class Skate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    evt_id: int
    skater: str
