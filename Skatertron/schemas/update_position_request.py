from pydantic import BaseModel, Field


class UpdateEventPositionRequest(BaseModel):
    event_id_list: list[int] = Field(..., description="The db ID of the event, represented as a list of ints")