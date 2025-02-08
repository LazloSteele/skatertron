from pydantic import BaseModel, ConfigDict, conint
from Skatertron.enums.footage_exceptions import FootageExceptions



class Skate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    event_id: conint(strict=True)
    skater_name: str
    footage_exceptions: FootageExceptions
    skate_position: int
