from Demos.security.lsaregevent import ret_code
from fastapi import Depends
from sqlalchemy.orm import Session
from src.app.infrastructure.db.session import get_bd as _get_db

def get_db() -> Session:
    return Depends(_get_db)
