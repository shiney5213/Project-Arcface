import uvicorn

from fastapi import FastAPI, Path, Query, Body, Form, File, UploadFile, HTTPException, Depends
# to use StaticsFiles > pip install aiofiles
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, Response,JSONResponse
# security
# to use html form or OAuth2PasswordRequestForm > pip install python-multipart
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

# fastapi has pydantic 
from pydantic import BaseModel 

from db import crud, db_models
from db.database import engine
from rest_src import rest_models, auth, user, group, person, device
from rest_src import role as r
import face_controller
from utils import stringutils

from sqlalchemy.orm import Session
from sqlalchemy import exc

from PIL import Image
import base64
import io

db_models.Base.metadata.create_all(bind=engine)

# Title
app = FastAPI(
    title="FaceID",
    description="This is a lightweight face recognition project by ooo.",
    version="0.1.0 Beta",
)

# static resource
app.mount("/service", StaticFiles(directory="web"), name="service")
# validators = {"foo": "if you need define this"}

# Check Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authorize")

@app.get("/api/validate")
def validate_token(token: str = Depends(oauth2_scheme)):
    return {"result":True, "token": token}

##########################################
# no Authentication
##########################################
@app.get("/api/status")
async def check_status():
    return {"status":"running"}

@app.get("/api/available/{user_id}")
async def available_user_id(user_id):
    return auth.available_user_id(user_id)

@app.post("/api/signup")
async def sign_up(signup: auth.SignUp) :
    return auth.regist(signup)

@app.post("/api/signin")
async def sign_in(signin: auth.SignIn) :
    result = auth.signin(signin)
    content = {"result":False, "detail": "fail"}
    headers = {}

    print("result===>", result)
    if not result is None:
        if result["result"] :
            datail = result["detail"]
            headers = {"Authorization": "Bearer "+datail["access_token"].decode('utf-8')}
            content["result"] = True
            content["detail"] = "success"
    
    return JSONResponse(content=content, headers=headers)

# to test swagger authorize
# @app.post("/authorize")
# async def authorize(form_data: OAuth2PasswordRequestForm = Depends()) :
#     signin = auth.SignIn(user_id=form_data.username, passwd=form_data.password)
#     result = auth.signin(signin)
#     print(result)
#     return result

##########################################
# Authentication
##########################################
def check_token(token:str = Depends(oauth2_scheme)):
    user = auth.check_token(token)
    return user

## Group
@app.post("/api/group")
async def create_group(new_group: group.NewGroup, auth: str = Depends(check_token)) :
    try :
        owner_hash = auth.user_hash
        group_id = group.create_group(new_group.group_name, owner_hash)
        if not group_id is None :
            face_controller.create_group(group_id)
            return {"result":True, "detail":"ok"}
    except Exception as error:
        print("error group creation", error)
        return {"result":False, "detail":error}
    
    return {"result":False, "detail":"creation failed"}

@app.get("/api/groups")
def get_groups(auth: str = Depends(check_token)):
    try :
        owner_hash = auth.user_hash
        results = group.list_group(owner_hash)
        return {"result":True, "detail": results}
    except Exception as error:
        print("error group list", error)
    
    return {"result":False, "detail": "can not list my groups"}

@app.delete("/api/group/{group_id}")
def remove_group(group_id:str, auth: str = Depends(check_token)):
    try :
        owner_hash = auth.user_hash
        result = group.delete_group(group_id, owner_hash)
        return result
    except Exception as error:
        print("error group list", error)
    
    return {"result":False, "detail": "can not delete the group"}

## Role
@app.post("/api/role")
async def create_role(new_role: r.Role, auth: str = Depends(check_token)) :
    result = r.create_role(new_role)
    return result

@app.get("/api/roles/{group_id}")
def get_roles(group_id:str, auth: str = Depends(check_token)) :
    results = r.get_roles(group_id)
    print("roles=",results)
    return {"result":True, "detail": results}

## Person
@app.get("/api/persons/{group_id}")
async def get_persons(group_id:str, auth: str = Depends(check_token)):
    results = person.get_persons(group_id)
    return {"result":True, "detail": results}

@app.post("/api/person")
async def create_person(new_person: person.RegistPerson, auth: str = Depends(check_token)) :
    print("server in")
    return person.create_person(new_person)

@app.post("/api/identify")
async def identify(snap_img: person.SnapImage) :
    result = person.identify(snap_img)
    return result

@app.post("/api/allow_role")
async def allow_roles(allow_role: r.AllowRole, auth: str = Depends(check_token)) :
    # exist user
    if person.get_person_by_hash( allow_role.person_hash) is None :
        return {"result":False, "detail": "person not exist!"}
    # exist role
    if r.get_role( allow_role.group_id, allow_role.role_id) is None :
        return {"result":False, "detail": "role not exist!"}
    # already allowed
    roles = r.get_roles_by_person_hash(allow_role.person_hash)

    if not roles is None:
        for item in roles :
            if item.role_id == allow_role.role_id :
                return {"result":False, "detail": "the person has the same role!"}

    results = r.allow_role_to_person(allow_role)
    return {"result":True, "detail": results}

if __name__ == '__main__' :
    uvicorn.run(app, host="0.0.0.0", port=7000)


