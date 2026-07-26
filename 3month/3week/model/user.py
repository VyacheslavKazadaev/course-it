from pydantic import BaseModel
from datetime import datetime

class UserInput(BaseModel):
    username: str
    email: str


class User(BaseModel):
    """
    Модель пользователя
    """
    id: int
    username: str
    email: str
    created_at: datetime