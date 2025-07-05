from typing import List
from ninja import Router
from django.contrib.auth.models import User
from ninja.errors import HttpError
from apps.users.schemas import LoginSchema, RegisterSchema, UserOut
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password


router = Router()


# Register endpoint
@router.post("/register")
def register_user(request, payload: RegisterSchema):
    if User.objects.filter(username=payload.username).exists():
        raise HttpError(400, "Username already taken")
    user = User.objects.create(
        username=payload.username,
        password=make_password(payload.password)
    )
    return {"id": user.id, "username": user.username}

# Login endpoint
@router.post("/login")
def login_user(request, payload: LoginSchema):
    user = authenticate(username=payload.username, password=payload.password)
    if user is None:
        raise HttpError(401, "Invalid credentials")
    return {"message": "Login successful", "user_id": user.id}

# List users
@router.get("/users", response=List[UserOut])
def list_users(request):
    return list(User.objects.values("id", "username"))
