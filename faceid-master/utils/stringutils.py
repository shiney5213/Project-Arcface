import hashlib
from . import timeutils

SALT = "keeface20200520"

def generate_user_hash(word:str) :
    word = word + SALT
    return "u"+generate_hash(word)

def generate_group_hash(user_id:str, group_name:str) :
    word = user_id + group_name + str(timeutils.get_microtime())
    return "g"+generate_hash(word)

def generate_person_hash(group_id:str, person_id:str, person_name:str) :
    word = group_id + person_id + person_name
    return "p"+generate_hash(word)

def generate_hash(word:str) :
    sha = hashlib.new('md5')
    encoded = word.encode('utf-8')
    sha.update(encoded)
    return sha.hexdigest()

def passwd_validator(passwd:str):
    min_length = 8
    max_length = 20

    SpecialSym=['!','@','#','$','%','^','&','*']

    result_detail = "ok"
    return_val=True

    if len(passwd) < min_length:
        result_detail = f'the length of password should be at least {min_length} char long'
        return_val=False
    if len(passwd) > max_length:
        result_detail = f'the length of password should be not be greater than {max_length}'
        return_val=False
    if not any(char.isdigit() for char in passwd):
        result_detail = 'the password should have at least one numeral'
        return_val=False
    # if not any(char.isupper() for char in passwd):
    #     result_detail = 'the password should have at least one uppercase letter'
    #     return_val=False
    if not any(char.islower() for char in passwd):
        result_detail = 'the password should have at least one lowercase letter'
        return_val=False
    if not any(char in SpecialSym for char in passwd):
        result_detail = 'the password should have at least one of the symbols !@#$%^&*'
        return_val=False

    return {"result":return_val, "detail":result_detail}