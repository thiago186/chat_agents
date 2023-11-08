"""This module contains the login related routes."""

import logging

from fastapi import APIRouter, HTTPException, status

from schemas.users import User, UserBase
import connectors.users_connector as users_connector

router = APIRouter(
    prefix="/login",
    tags=["login"],
)


@router.post("/create_user")
async def create_user(user_base: UserBase):
    """Creates the user in the database."""
    user = User(**user_base.dict())
    user.set_password(user_base.password)
    logging.debug(f"Password set using hashing algorithm.")
    try:
        await users_connector.create_user(user)
        return {"detail": "User created successfully."}

    except Exception as e:
        if str(e) == "User already exists.":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already exists.")
