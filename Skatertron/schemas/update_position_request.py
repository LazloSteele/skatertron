from pydantic import BaseModel, Field


class UpdateEventPositionRequest(BaseModel):
    event_id: int = Field(..., description="The ID of the event, represented as a string")
    event_position: int = Field(..., description="The current position of the event")
    new_event_position: int = Field(..., description="The new position to move the event to")