from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime
from uuid import UUID

class User(BaseModel):
    external_id: UUID = Field(
        ..., 
        description="The unique identifier for the user, usually provided by an external system.",
        examples=["550e8400-e29b-41d4-a716-446655440000"]
    )
    
    name: str = Field(
        ..., 
        min_length=1, 
        max_length=100,
        description="Full name of the user.",
        examples=["John Doe"]
    )
    
    email: EmailStr = Field(
        ..., 
        description="Valid electronic mail address.",
        examples=["john.doe@example.com"]
    )
    
    date_of_birth: datetime = Field(
        ..., 
        description="The user's date and time of birth in ISO 8601 format.",
        examples=["1990-01-01T00:00:00"]
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "external_id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "John Doe",
                "email": "john.doe@example.com",
                "date_of_birth": "1990-01-01T00:00:00"
            }
        }
    )