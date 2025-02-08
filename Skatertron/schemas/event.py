from pydantic import BaseModel, ConfigDict, conint


class Event(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    competition_id: conint(strict=True)
    event_number: str
    event_name: str
    event_rink: str
    event_position: int
    