from fastapi import APIRouter, Depends

from src.auth.users import auth_backend, fastapi_users, current_active_user
from src.auth.schemas import UserRead, UserCreate
from src.models import User

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)


@router.get("/protected-route")
def protected_route(user: User = Depends(current_active_user)):
    return f"Hello, {user.email}"


@router.get("/unprotected-route")
def unprotected_route():
    return "Hello, anonym"
