from datetime import timedelta, datetime

import jwt
from fastapi import HTTPException, APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jwt import PyJWTError
from starlette import status

from models.user import User, RegisterUser
from rest.dependencies import RepoProvider, repos_provider


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def get_current_user(token: str = Depends(oauth2_scheme), repos: RepoProvider = Depends(repos_provider)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    user = await repos.users_repo.get_user(username)
    if not user:
        raise credentials_exception
    del user.hashed_password
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/register")
async def create_user(user: RegisterUser, repos: RepoProvider = Depends(repos_provider)):
    user = await repos.users_repo.create_user(user, user.password)

    return user


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), repos: RepoProvider = Depends(repos_provider)):
    user = await repos.users_repo.get_user(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not repos.users_repo.check_password(user, form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = create_access_token({"username": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):

    return current_user
