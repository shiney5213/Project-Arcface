from pydantic import BaseModel
from typing import List

# Person Group

# role


class RoleGroup(BaseModel):
    group_id: str
    role_group_id: str = None # auto creation
    role_group_name: str

class RoleToRoleGroup(BaseModel):
    role_group_id: str
    role_id: str

# person
class Person(BaseModel):
    group_id: str
    person_id: str
    person_name: str = None




