import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from .database import Base

# User 
class User(Base):
    __tablename__   = "user"
    no              = Column(Integer, primary_key=True, autoincrement=True)
    user_hash       = Column(String(64), unique=True, index=True, nullable=False)
    user_id         = Column(String(50), unique=True, index=True, nullable=False) # email only
    user_name       = Column(String(50), index=True, nullable=False)
    passwd          = Column(String(512), nullable=False) #hash
    email_confirmed = Column(Boolean, default=False, nullable=False)
    created         = Column(DateTime, default=datetime.datetime.utcnow)
    last_modified   = Column(DateTime, default=datetime.datetime.utcnow)

# Person Group = Maybe Company ?
class Group(Base):
    __tablename__ = "group"
    no            = Column(Integer, primary_key=True, autoincrement=True)
    group_id      = Column(String(64), index=True, nullable=False) # auto creation hash string(user_id + group_name + timestamp)
    group_name    = Column(String(50), index=True, nullable=False, default="Default Group")
    created       = Column(DateTime, default=datetime.datetime.utcnow)
    owner_hash    = Column(String(64), ForeignKey("user.user_hash"), nullable=False, index=True)

# Group that I'm in
class GroupOfUser(Base):
    __tablename__ = "group_of_user"
    no            = Column(Integer, primary_key=True, autoincrement=True)
    user_hash     = Column(String(64), ForeignKey("user.user_hash"), nullable=False, index=True)
    group_id      = Column(String(64), index=True, nullable=False)
    created       = Column(DateTime, default=datetime.datetime.utcnow)

# Person
class Person(Base):
    __tablename__ = "person"
    no            = Column(Integer, primary_key=True, autoincrement=True)
    person_hash   = Column(String(64), unique=True, index=True, nullable=False) #hash(group_id + person_id + person_name + timestamp)
    group_id      = Column(String(64), ForeignKey("group.group_id"), index=True, nullable=False)
    person_id     = Column(String(64), index=True, nullable=False) # usually email
    person_name   = Column(String(50), index=True)

class RoleOfPerson(Base):
    __tablename__ = "role_of_person"
    no            = Column(Integer, primary_key=True, autoincrement=True)
    person_hash   = Column(String(64), ForeignKey("person.person_hash"), index=True, nullable=False)
    role_type     = Column(String(10), nullable=False, default="role") # role or group
    role_id       = Column(String(64), nullable=False) # role of role_group_id

# Person Images
class Img(Base):
    __tablename__ = "img"
    no            = Column(Integer, primary_key=True, autoincrement=True)
    person_hash   = Column(String(64), ForeignKey("person.person_hash"), index=True, nullable=False)
    img_id        = Column(Integer)
    data_dir      = Column(String(256))

# Role
class Role(Base):
    __tablename__ = "role"
    no            = Column(Integer, primary_key=True, autoincrement=True)
    group_id      = Column(String(64), ForeignKey("group.group_id"), index=True, nullable=False)
    role_id       = Column(String(64), index=True, nullable=False)
    role_name     = Column(String(50), index=True) # attendence, 301 gate etc.

class RoleGroup(Base):
    __tablename__   = "role_group"
    no              = Column(Integer, primary_key=True, autoincrement=True)
    group_id        = Column(String(64), ForeignKey("group.group_id"), index=True, nullable=False) # company group
    role_group_id   = Column(String(64), index=True, nullable=False) # role_group
    role_group_name = Column(String(50), index=True)

class CommandAfterConfirm(Base):
    __tablename__  = "command_after_confirm"
    no             = Column(Integer, primary_key=True, autoincrement=True)
    role_id        = Column(String(64), ForeignKey("role.role_id"), nullable=False)
    command_id     = Column(String(64), unique=True, index=True, nullable=False) # auto creation
    command_name   = Column(String(50), index=True)
    url            = Column(String(128))

# Device - role dependency
class AllowedDeviceInGroup(Base):
    __tablename__   = "allowed_device_in_group"
    no            = Column(Integer, primary_key=True, autoincrement=True)
    group_id      = Column(String(64), ForeignKey("group.group_id"), index=True, nullable=False)
    device_id     = Column(String(64), unique=True, nullable=False, index=True) # auto creation
    device_name   = Column(String(50), index=True)
    ip_address    = Column(String(128), nullable=False) # ip + port or url

