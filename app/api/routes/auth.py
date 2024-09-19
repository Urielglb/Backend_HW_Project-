from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.db import get_session
from app.services.auth import auth_user

router = APIRouter()


@router.post("")
def authenticate_user(pin: str, session: Session = Depends(get_session)):
    user = auth_user(session, pin)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
