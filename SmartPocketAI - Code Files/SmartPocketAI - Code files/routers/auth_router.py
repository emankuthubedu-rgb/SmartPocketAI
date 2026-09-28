from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth import create_access_token, decode_access_token, get_current_user, hash_password, verify_password
from database import get_db
from models import User
from schemas import AuthResponse, LoginRequest, PublicUser, RegisterRequest, SessionInfoResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter(tags=["auth"])
bearer = HTTPBearer(auto_error=False)


def public_user(user: User) -> PublicUser:
    return PublicUser(name=user.name, username=user.username, email=user.email)


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    username = body.username.strip()
    email = body.email.lower().strip()
    if db.query(User).filter(func.lower(User.username) == username.lower()).first():
        raise HTTPException(status_code=409, detail="This username is already taken. Please choose another.")
    if db.query(User).filter(func.lower(User.email) == email).first():
        raise HTTPException(status_code=409, detail="An account with this email already exists. Try logging in instead.")

    user = User(name=body.name.strip(), username=username, email=email, password_hash=hash_password(body.password))
    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Username or email already exists.") from exc
    db.refresh(user)
    return AuthResponse(token=create_access_token(user), user=public_user(user))


@router.post("/login", response_model=AuthResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    identifier = body.identifier.strip().lower()
    user = db.query(User).filter(
        or_(func.lower(User.username) == identifier, func.lower(User.email) == identifier)
    ).first()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username/email or password.")
    return AuthResponse(token=create_access_token(user), user=public_user(user))


@router.get("/session-info", response_model=SessionInfoResponse)
def session_info(
    user: User = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
):
    payload = decode_access_token(credentials.credentials)
    login_time_raw = payload.get("login_time")
    try:
        login_time = datetime.fromisoformat(login_time_raw)
        if login_time.tzinfo is None:
            login_time = login_time.replace(tzinfo=timezone.utc)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=401, detail="Token does not contain a valid login time.") from exc
    duration = max(0, int((datetime.now(timezone.utc) - login_time).total_seconds() // 60))
    return SessionInfoResponse(
        username=user.username,
        login_time=login_time.isoformat(),
        session_duration_minutes=duration,
    )
