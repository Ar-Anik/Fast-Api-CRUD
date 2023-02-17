from pydantic import BaseModel

class Schema(BaseModel):
    class Config:
        orm_mode = True

class Person(Schema):
    id: int
    firstName: str
    lastName: str
    gender: str

class UpdatePerson(Schema):
    firstName: str
    lastName: str
    gender: str
