from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username : str = Field(min_length=5, max_length=50)
    email : str = Field(min_length=5, max_length=100)

class UserResponse(BaseModel):
    id : int
    username : str
    email : str

    model_config = {
        "from_attributes": True
    }

class TaskCreate(BaseModel):
    title : str = Field(min_length=1, max_length=100)
    description : str = Field(min_length=5, max_length=200)

class TaskResponse(BaseModel):
    id : int
    title : str
    description : str

    model_config = {
        "from_attributes": True
    }