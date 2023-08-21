import re
from pydantic import BaseModel, EmailStr, field_validator, constr, validator
from typing import Optional



class UserCreateSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=64)
    password2: constr(min_length=8, max_length=64)

    @field_validator("password")
    def password_must_contain_special_characters(cls, v):
        if not re.search(r"[^a-zA-Z0-9]", v):
            raise ValueError("Password must contain special characters")
        return v

    @field_validator("password")
    def password_must_contain_numbers(cls, v):
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain numbers")
        return v

    @field_validator("password")
    def password_must_contain_uppercase(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain uppercase characters")
        return v

    @field_validator("password")
    def password_must_contain_lowercase(cls, v):
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain lowercase characters")
        return v
    
    @validator("password2")
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v
    
class UserUpdateSchema(BaseModel):
    email: EmailStr

class UserSchema(BaseModel):
    id: int
    email: str

    class ConfigDict:
        from_attributes = True




class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    
    
class TokenData(BaseModel):
    id: int
    email: str


class ResetPasswordSchema(BaseModel):
    password1: constr(min_length=8, max_length=64)
    password2: constr(min_length=8, max_length=64)

    @field_validator("password2")
    def passwords_match(cls, password2, values, **kwargs):
        if "password1" in values and password2 != values["password1"]:
            raise ValueError("Passwords do not match")
        return password2
    
    @field_validator("password1")
    def password_must_contain_special_characters(cls, v):
        if not re.search(r"[^a-zA-Z0-9]", v):
            raise ValueError("Password must contain special characters")
        return v

    @field_validator("password1")
    def password_must_contain_numbers(cls, v):
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain numbers")
        return v

    @field_validator("password1")
    def password_must_contain_uppercase(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain uppercase characters")
        return v

    @field_validator("password1")
    def password_must_contain_lowercase(cls, v):
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain lowercase characters")
        return v