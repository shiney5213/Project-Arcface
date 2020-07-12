from . import db_models
from fastapi import Depends
from sqlalchemy.orm import Session

from rest_src import auth, person, group
from rest_src import role as r

from utils import stringutils
import pandas as pd

# user ######################################################
def get_user_by_user_id(user_id: str, db: Session):
    table = db_models.User
    return db.query(table).filter(table.user_id == user_id).first()

def get_user_by_user_hash(user_hash: str, db: Session):
    table = db_models.User
    return db.query(table).filter(table.user_hash == user_hash).first()

def create_user(user: auth.SignUp, db: Session):
    hashed_user_id = stringutils.generate_user_hash(user.user_id)
    new_user = db_models.User(user_id=user.user_id, user_name=user.user_name, passwd=user.passwd, user_hash=hashed_user_id)
    db.add(new_user)
    return new_user

def get_user(user: auth.SignIn, db: Session):
    table = db_models.User
    user = db.query(table).filter(table.user_id == user.user_id).first()
    return user

# group = company group ######################################################
def create_group(group_id:str, group_name:str, owner_hash:str, db: Session):
    new_group = db_models.Group(group_id=group_id, group_name=group_name, owner_hash=owner_hash)
    db.add(new_group)
    return new_group

def get_own_groups(user_hash:str, db: Session):
    table = db_models.Group
    return db.query(table).filter(table.owner_hash==user_hash).all()

def delete_group(group_id:str, owner_hash:str, db:Session):
    table = db_models.Group
    group = db.query(table).filter(table.group_id == group_id, table.owner_hash == owner_hash).first()
    if not group is None:
        db.delete(group)
        db.commit()
    return group

# user's group ######################################################
def user_to_group(group_id: group.Group, user_hash:str, db: Session):
    new_group_of_user = db_models.GroupOfUser(group_id=group_id, user_hash=user_hash)
    db.add(new_group_of_user)
    return new_group_of_user

def get_my_groups(user_hash:str, db: Session):
    users = db_models.GroupOfUser
    groups = db_models.Group
    resultset = db.query(groups) \
            .join(users, groups.group_id == users.group_id) \
            .filter(users.user_hash == user_hash).all()
    return resultset

# role & role group ######################################################
def get_role(group_id:str, role_id: str, db: Session):
    table = db_models.Role
    return db.query(table).filter(table.group_id == group_id, table.role_id == role_id).first()

def get_roles(group_id:str, db: Session, skip: int = 0, limit: int = 1000):
    table = db_models.Role
    return db.query(table).filter(table.group_id == group_id).offset(skip).limit(limit).all()

def get_roles_by_person_hash(person_hash:str, db: Session, skip: int = 0, limit: int = 1000):
    table = db_models.RoleOfPerson
    return db.query(table).filter(table.person_hash == person_hash).offset(skip).limit(limit).all()

def create_role(group_id:str, role_id:str, role_name:str, db: Session):
    new_role = db_models.Role(group_id=group_id, role_id=role_id, role_name=role_name)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

# person ######################################################
def get_person_count(group_id: str, db: Session):
    table = db_models.Person
    result = db.query(table).filter(table.group_id == group_id).count()
    return result

def get_person(group_id:str, person_id: str, db: Session):
    table = db_models.Person
    return db.query(table).filter(table.group_id == group_id, table.person_id == person_id).first()

def get_person_by_hash(person_hash:str, db: Session):
    table = db_models.Person
    return db.query(table).filter(table.person_hash == person_hash).first()

def get_persons(group_id:str, db: Session, skip: int = 0, limit: int = 1000):
    table = db_models.Person
    return db.query(table).filter(table.group_id == group_id).offset(skip).limit(limit).all()

def create_person(person: person.RegistPerson, person_hash:str, db: Session):
    new_person = db_models.Person(person_hash=person_hash, group_id=person.group_id, person_id=person.person_id, person_name=person.person_name)
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person

# img ######################################################
def get_max_img_id(person_hash: str, db: Session):
    table = db_models.Img
    max_img_id = 0
    max_img = db.query(table).filter(table.person_hash == person_hash).order_by(table.img_id.desc()).first()
    if not max_img is None : # 
        max_img_id = max_img.img_id + 1
    return max_img_id

def create_img(person_hash: str, max_img_id:int, db: Session):
    new_img = db_models.Img(person_hash=person_hash, img_id=max_img_id)
    db.add(new_img)
    db.commit()
    db.refresh(new_img)
    return new_img

# roles of person ######################################################
def get_roles_by_person_id(person_id: str, db: Session):
    table = db_models.RoleOfPerson
    return db.query(table).filter(table.person_id == person_id).all()

def allow_role_to_person(allow:r.AllowRole, db: Session):
    new_role = db_models.RoleOfPerson(person_hash=allow.person_hash, role_id=allow.role_id)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

def delete_role_of_person(person_id: str, role_id: str, db: Session):
    table = db_models.RoleOfPerson
    role = db.query(table).filter(table.person_id == person_id, table.role_id == role_id).first()
    if not role is None:
        db.delete(role)
        db.commit()
    return role
