"""This file contains the connector for the users table."""

import os
from sqlmodel import SQLModel, Session, create_engine, select

from dotenv import load_dotenv

from schemas.users import User
from dependencies.auth import verify_field

load_dotenv()

DATABASE_URL = (
    f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}"
    f"@{os.environ['DATABASE_HOST']}:{os.environ['DATABASE_PORT']}"
    f"/{os.environ['POSTGRES_DB']}"
)

engine = create_engine(DATABASE_URL, echo=os.environ["SQL_ECHO"].lower()=="true")

def build_tables(password):
    """
    Create all tables that don't exist in the database. 
    This function is only available for the admin user.
    """
    if verify_field(password, os.environ["USERS_RESET_PASSWORD_ENCRYPTED"]):
        SQLModel.metadata.create_all(engine)
    else:
        print("You don't have permission to do this. Users will not be reseted.")


def reset_tables(password):
    """
    Reset all the tables in the database. 
    This function is only available for the admin user.
    """
    if verify_field(password, os.environ["USERS_RESET_PASSWORD_ENCRYPTED"]):
        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
    else:
        print("You don't have permission to do this. Users will not be reseted.")


async def create_user(user: User):
    """
    Create a new user in the database.
    """
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


async def update_user_active_status(user_id: int, active: bool):
    """
    Update a user's 'active' attribute in the database.
    """
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user:
            user.active = active
            session.commit()
            session.refresh(user)
            return user


async def get_user_by_email(email: str):
    """
    Get a user by its email.
    """
    with Session(engine) as session:
        statement = select(User).where(User.email == email)
        users = session.exec(statement)
        return users.first()


async def get_user_by_id(user_id: str):
    """
    Get a user by its email.
    """
    with Session(engine) as session:
        statement = select(User).where(User.user_id == user_id)
        users = session.exec(statement)
        return users.first()
