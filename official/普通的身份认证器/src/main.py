from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status, Header, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import jwt
from pydantic import BaseModel
from hashlib import sha256
import logging
from fastapi.logger import logger as fastapi_logger

import OpenSSL
import base64


ACCESS_TOKEN_EXPIRE_MINUTES = 30
PUBLIC_KEY = open("jwt.key.pub", "r").read()
PRIVATE_KEY = open("jwt.key", "r").read()
SALT = b'd_Yn2xWvnu'


users_db = {
    "admin": {
        "username": "admin",
        "flag": "flag{just_A_simple_Json_Web_T0ken_exp1oit_",
        "disabled": False,
    },
    "guest": {
        "username": "guest",
        "flag": "只有 'admin' 用户才有 flag 哦！",
        "disabled": False,
    }
}


with open("cert.pem") as f:
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, f.read())


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    disabled: Optional[bool] = None


class UserInDB(User):
    flag: str


class TokenOption(BaseModel):
    hg_token: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

logger = logging.getLogger(__name__)

app.mount("/static", StaticFiles(directory="static"), name="static")


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if username != "guest":
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm="RS256")
    return encoded_jwt


def check_hackergame_token(hg_token):
    raise_error = False
    if hg_token is None:
        raise_error = True
    else:
        try:
            id, sig = hg_token.split(":", 1)
            sig = base64.b64decode(sig, validate=True)
            OpenSSL.crypto.verify(cert, sig, id.encode(), "sha256")
        except Exception as e:
            raise_error = True
    if raise_error:
        raise HTTPException(status_code=403, detail="比赛 token 校验错误。\n如果您正在使用网页完成此题目，请从比赛平台打开题目（推荐），或正确输入比赛 token。\n如果您正在使用非网页方式请求后端，请确认 HTTP 请求头 hg-token 设置正确。")
    return True


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, PUBLIC_KEY)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except:
        raise credentials_exception
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(hg_token: Optional[str] = Header(None)):
    check_hackergame_token(hg_token)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": "guest"}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/profile", response_model=UserInDB)
async def read_users_me(raw: Request,
                        current_user: User = Depends(get_current_active_user), 
                        hg_token: Optional[str] = Header(None)):
    check_hackergame_token(hg_token)
    if current_user.username == 'admin':
        # format flag
        user = current_user.copy()
        user.flag = user.flag + \
            sha256(SALT + hg_token.encode('utf-8')).hexdigest()[:6] + '}'
        # log user data for future analysis
        fastapi_logger.warn(f"User with token {hg_token[:10]} gets flag with jwt {raw.headers['authorization']}")
    else:
        user = current_user
    return user


@app.get("/")
def index():
    return FileResponse('index.html', media_type='text/html')


@app.post("/debug")
async def debug():
    return {
        "ACCESS_TOKEN_EXPIRE_MINUTES": ACCESS_TOKEN_EXPIRE_MINUTES,
        "PUBLIC_KEY": PUBLIC_KEY
    }
