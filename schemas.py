from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import *

class Token_data(BaseModel):
    email : Optional[str] = None
 
class Signup(BaseModel):
    username: str
    email: EmailStr
    password: str

class gbv(BaseModel):
    pid : int
    firstName : str
    lastName : str
    gender : str
    ethicinity : str
    contact : int
    Id : str
    location : str
    postal : int
    report : str
    status : str
    created_at : datetime

    class Config:
        orm_mode = True
