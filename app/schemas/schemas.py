from datetime import datetime
import time
from typing import List, Optional, Union
from uuid import uuid4

from pydantic import BaseModel


class BaseUser(BaseModel):
    """Base User model received on the request body"""
    email: str
    username: str
    password: str

class User(BaseUser):
    """User model"""
    user_id: uuid4
    email: str
    username: str
    hashed_password: str
    current_plan: str
    created_at: datetime
    active: bool
