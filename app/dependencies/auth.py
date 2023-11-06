"""This module contains functions for encrypting and verifying fields."""

import bcrypt

def encrypt_field(field: str):
    """Encrypts a field using bcrypt."""
    hashed_field = bcrypt.hashpw(field.encode('utf-8'), bcrypt.gensalt())
    return hashed_field.decode('utf-8')

def verify_field(field: str, hashed_field: str):
    """Verifies a field using bcrypt."""
    return bcrypt.checkpw(field.encode('utf-8'), hashed_field.encode('utf-8'))
