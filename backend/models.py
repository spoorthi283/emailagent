
from pydantic import BaseModel, Field
from pydantic import BaseModel, EmailStr

class EmailRequest(BaseModel):
    recipients: list[EmailStr]
    subject: str
    body: str

class PromptRequest(BaseModel):
    prompt: str = Field(
        min_length=3,
        max_length=5000
    )


class ContactRequest(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100
    )

    email: str = Field(
        min_length=5,
        max_length=254
    )
