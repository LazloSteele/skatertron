from pydantic import BaseModel, ConfigDict


class Event(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    competition_id: int
    evt_number: str
    evt_title: str
    