from fastapi import APIRouter, Depends

from Models import User
from Schemas import UserResponse
from Security.Auth import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user