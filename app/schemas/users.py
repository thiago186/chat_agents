"""This module contains all the schemas for the application."""

from datetime import datetime
import logging
from typing import Optional
from uuid import uuid4, UUID

from sqlmodel import SQLModel, Field

from dependencies.auth import encrypt_field, verify_field


class User(SQLModel, table=True):
    """This class defines the schema for the User model."""
    user_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    email: str Field(..., unique=True)
    username: str
    hashed_password: str
    current_plan: str
    plan_due_date: Optional[datetime]
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    active: bool = Field(default=True)

    def set_password(self, password: str):
        self.hashed_password = encrypt_field(password)

    def verify_password(self, password: str):
        return verify_field(password, self.hashed_password)
