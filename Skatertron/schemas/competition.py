from pydantic import BaseModel, ConfigDict


class Competition(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    competition_name: str
    competition_year: int
    host_club: str
