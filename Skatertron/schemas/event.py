from pydantic import BaseModel, ConfigDict


class Event(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    competition_id: int
    event_number: str
    event_name: str
    