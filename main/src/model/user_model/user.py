from pydantic import BaseModel, Field


class UserForm(BaseModel):
    id: int = Field(..., title='User ID')
    name: str = Field(..., title='Name')
    age: int = Field(..., title='Age')
    gender: str = Field(..., title='Gender')
    opposite_gender: str = Field(..., title='Opposite Gender')
    location: str = Field(..., title='Location')
    games: str = Field(..., title='Games')
    description: str = Field(..., title='Description')
    photo: str = Field(..., title='Photo')
    language: str = Field(..., title='Language')
    likes: int = Field(0, title='Likes')


class UserConfirmation(BaseModel):
    id: int = Field(..., title='User ID')
    confirmed: bool = Field(False, title='Confirmed')


class UserProfile(BaseModel):
    id: int = Field(..., title='User ID')
    name: str = Field(..., title='Name')
    age: int = Field(..., title='Age')
    gender: str = Field(..., title='Gender')
    opposite_gender: str = Field(..., title='Opposite Gender')
    location: str = Field(..., title='Location')
    games: str = Field(..., title='Games')
    description: str = Field(..., title='Description')
    photo: str = Field(..., title='Photo')
    language: str = Field(..., title='Language')
    likes: int = Field(..., title='Likes')
