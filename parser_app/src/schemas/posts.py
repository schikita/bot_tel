
from pydantic import BaseModel


class PostSchema(BaseModel):
    post_id: int
    text: str

    class Config:
        from_attributes = True


class PostsResponse(BaseModel):
    posts: list[PostSchema]

    class Config:
        orm_mode = True
