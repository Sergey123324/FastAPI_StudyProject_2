from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Security.JWT import create_access_token
from Database import get_session
from Models import User
from Schemas import RegisterRequest, UserResponse, LoginRequest
from Security.Password import hash_password, verify_password


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_session)
):
    existing_user = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(data.password)

    user = User(
        username=data.username,
        email=data.email,
        password_hash=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@router.post("/login")
def login(
        data: LoginRequest,
        db: Session = Depends(get_session)
):
    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

