from pydantic import BaseModel,Field,EmailStr

class User(BaseModel):
    name:str=Field(...,description="Name is required")
    email: EmailStr=Field(...,description="Email is required")
    password:str=Field(...,description="password is required")
    role:str=Field(...,description="Your role")
    #optional field in db
    create_at:str
    address:str
    mobile:str
    


class LoginModel(BaseModel):
    email: EmailStr = Field(..., description="Email is required")
    password: str = Field(..., description="Password is required")