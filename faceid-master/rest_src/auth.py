import jwt
from datetime import datetime, timedelta
from email_validator import validate_email, EmailNotValidError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
from jwt import PyJWTError
from passlib.context import CryptContext
from pydantic import BaseModel

from sqlalchemy.orm import Session
from sqlalchemy import exc

from db import crud, db_models

from utils import stringutils

from db.database import SessionLocal
from contextlib import contextmanager

@contextmanager
def session_scope():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()

# command> openssl rand -hex 32
SECRET_KEY = "9baefb12876922d6576bf968b621005418d13cfa90071e15cbe323826021e6ab"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User info.
class SignUp(BaseModel):
    user_id: str # email
    user_name: str
    passwd: str # hashed

class SignIn(BaseModel):
    user_id: str # email
    passwd: str # hashed

# signup
def regist(signup: SignUp) :
    try :
        user_id_result = available_user_id(signup.user_id)
        if not user_id_result["result"]:
            return user_id_result
        passwd_result = stringutils.passwd_validator(signup.passwd)
        if not passwd_result["result"] :
            return passwd_result

        with session_scope() as db:
            if crud.get_user_by_user_id(signup.user_id, db) is None:
                signup.passwd = get_password_hash(signup.passwd)
                result = crud.create_user(signup, db)
            else:
                return {"result":False, "detail":"can not use this email!"}

    except EmailNotValidError as e:
        return {"result":False, "detail":"user_id is not valid"}

    except exc.SQLAlchemyError as error:
        print("signup error", error)
        return {"result":False, "detail":"could not sign-up!"}

    return {"result":True, "detail": "success!"}

#signin
def signin(signin:SignIn):
    try :
        validate_email(signin.user_id)
        # passwd_result = stringutils.passwd_validator(signin.passwd)
        # if not passwd_result["result"] :
        #     return passwd_result
        result = login_for_access_token(signin)
    except EmailNotValidError as e:
        return {"result":False, "detail":"user_id is not valid"}
    except exc.SQLAlchemyError as error:
        print("signin error", error)
        return {"result":False, "detail":"could not sign-in!"}

    return {"result":True, "detail":result}

# user
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def available_user_id(user_id:str):
    try :
        validate_email(user_id)
    except EmailNotValidError as e:
        return {"result":False, "detail":"check your ID what should be email address!"}

    with session_scope() as db:
        user = crud.get_user_by_user_id(user_id,db)
        print("get user===>", user)
        if user is None:
            return {"result":True, "detail":"ok"}

    return {"result":False, "detail":"user_id is not valid"}

# token
def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    # timeout
    # if expires_delta:
    #     expire = datetime.utcnow() + expires_delta
    # else:
    #     expire = datetime.utcnow() + timedelta(minutes=15)
    expire = 0

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def check_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user_hash = get_user_hash_from_token(token)
        if user_hash is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    with session_scope() as db:
        user = crud.get_user_by_user_hash(user_hash, db)
        db.expunge_all()

    if user is None:
        raise credentials_exception
    return user

def get_user_hash_from_token(token:str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_hash: str = payload.get("sub")
    return user_hash


def get_current_active_user(token: str = Depends(check_token)):
    if token.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return token

def authenticate_user(signin: SignIn, db: Session):
    user = crud.get_user(signin, db)
    print("authenticate_user", user)
    if not user:
        return False
    if not verify_password(signin.passwd, user.passwd):
        return False
    return user

# @app.post("/token", response_model=Token)
def login_for_access_token(signin: SignIn):
    with session_scope() as db:
        user = authenticate_user(signin, db)
        db.expunge_all()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_hash}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

