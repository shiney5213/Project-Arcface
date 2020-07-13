from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from db import crud, db_models
from db.database import SessionLocal
from contextlib import contextmanager

import face_controller
from utils import stringutils

import base64
import io
from PIL import Image

class Role(BaseModel):
    group_id: str
    role_id: str
    role_name: str

class AllowRole(BaseModel):
    group_id:str
    person_hash: str
    role_type: str # role or group
    role_id: str

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

def get_role(group_id:str, role_id:str):
    try :
        with session_scope() as db:
            result = crud.get_role(group_id, role_id, db)
            return result
    except Exception as error:
        print("get role error", error)
    return None

def get_roles(group_id:str):
    try :
        with session_scope() as db:
            results = crud.get_roles(group_id, db)
            return jsonable_encoder(results)
    except Exception as error:
        print("list role error", error)
    return None

def get_roles_by_person_hash(person_hash:str) :
    try :
        with session_scope() as db:
            results = crud.get_roles_by_person_hash(person_hash, db)
            db.expunge_all()
            return results
    except Exception as error:
        print("get_roles error", error)
    return None

def create_role(new_role:Role):
    try :
        with session_scope() as db:
            role = crud.get_role(new_role.group_id, new_role.role_id, db)
            if not role is None:
                return {"result":False, "detail": "already have the same role!"}
            result = crud.create_role(new_role.group_id, new_role.role_id, new_role.role_name, db)
            return {"result":True, "detail": "ok"}
    except Exception as error:
        return {"result":False, "detail": str(error)}

def allow_role_to_person(allow:AllowRole):
    try :
        with session_scope() as db:
            results = crud.allow_role_to_person(allow, db)
            return results
    except Exception as error:
        print("allow role error", error)
    return None