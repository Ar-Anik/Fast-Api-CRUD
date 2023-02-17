from fastapi import FastAPI, status, HTTPException
from database import SessionLocal
from typing import List
from schema import Person, UpdatePerson
import uvicorn
import models

app = FastAPI()
db = SessionLocal()

mdl = models.Person

@app.get('/', response_model=List[Person], status_code=status.HTTP_200_OK)
def get_all_data():
    allData = db.query(mdl).all()
    return allData

@app.get("/{pid}", response_model=Person, status_code=status.HTTP_200_OK)
def get_data(pid: int):
    find_person = db.query(mdl).filter(mdl.id == pid).first()

    if find_person:
        return find_person

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person Not Found")


@app.post('/add', response_model=Person, status_code=status.HTTP_201_CREATED)
def add_data(person: Person):
    newPerson = mdl(
        id = person.id,
        firstName = person.firstName,
        lastName = person.lastName,
        gender = person.gender
    )

    find_person = db.query(mdl).filter(mdl.id == person.id).first()

    if find_person is None:
        db.add(newPerson)
        db.commit()

        return newPerson

    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Data Already Exist")


@app.put('/update/{pid}', response_model=Person, status_code=status.HTTP_202_ACCEPTED)
def update_data(pid: int, person: UpdatePerson):
    find_person = db.query(mdl).filter(mdl.id == pid).first()

    if find_person is not None:
        find_person.firstName = person.firstName
        find_person.lastName = person.lastName
        find_person.gender = person.gender

        db.commit()

        return find_person

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person Not Found")


@app.delete('/delete/{pid}', response_model=Person, status_code=status.HTTP_200_OK)
def delete_data(pid: int):
    find_person = db.query(mdl).filter(mdl.id == pid).first()

    if find_person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person Not Found")

    db.delete(find_person)
    db.commit()

    raise HTTPException(status_code=status.HTTP_200_OK, detail="Person Successfully Deleted")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("9000")))
