from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from db import crud, db_models
from db.database import SessionLocal
from contextlib import contextmanager

from sqlalchemy import exc

from utils import stringutils

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

# regist person with face image
class NewGroup(BaseModel): # auto create default group after user's email confirmed
    group_name: str # Default Group

class Group(BaseModel): # auto create default group after user's email confirmed
    group_id: str
    group_name: str # Default Group
    owner_hash: str

def create_group(group_name:str, owner_hash:str):
    try :
        with session_scope() as db:
            group_id = stringutils.generate_group_hash(owner_hash, group_name)
            new_group = crud.create_group(group_id, group_name, owner_hash, db)
            group_of_user = crud.user_to_group(group_id, owner_hash, db)
        return group_id
    except exc.SQLAlchemyError as error:
        print("group creation error", error)
    return None

def user_to_group(user_hash:str, group_id:str):
    try :
        with session_scope() as db:
            group_of_user = crud.user_to_group(user_hash, group_id, db)
        return group_of_user
    except exc.SQLAlchemyError as error:
        print("user_to_group creation error", error)
    return None

def list_group(user_hash:str):
    try :
        with session_scope() as db:
            own_groups = crud.get_own_groups(user_hash, db)
            my_groups = crud.get_my_groups(user_hash, db)
            return jsonable_encoder({"own_groups": own_groups, "my_groups": my_groups})
    except exc.SQLAlchemyError as error:
        print("group list error", error)
    return None

def delete_group(group_id:str, owner_hash:str):
    try :
        with session_scope() as db:
            person_count = crud.get_person_count(group_id, db)
            print("delete_group", "person_count", person_count)
            if person_count < 1:
                deleted = crud.delete_group(group_id, owner_hash, db)
                if not deleted is None :
                    return {"result": True, "detail": "ok"}
            else:
                return {"result": False, "detail": "persons exist in this group. can not delete."}
    except exc.SQLAlchemyError as error:
        print("group creation error", error)
    return {"result": False, "detail": "could not delete this group"}