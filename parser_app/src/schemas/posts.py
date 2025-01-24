from typing import List

from pydantic import BaseModel


class PostSchema(BaseModel):
    post_id: int
    text: str

    class Config:
        orm_mode = True


class PostsResponse(BaseModel):
    posts: List[PostSchema]

    class Config:
        orm_mode = True
