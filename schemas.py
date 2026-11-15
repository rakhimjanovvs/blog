from pydantic import BaseModel, Field, field_validator, ConfigDict

class PostCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    body: str = Field(min_length=3)

    @field_validator("title", "body")
    @classmethod
    def validate_title(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Название поста должно содержать минимум 3 символов!")
        return v

class PostRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    body: str
    views: int

class CommentCreate(BaseModel):
    text: str = Field(min_length=3)

class CommentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str
    post_id: int