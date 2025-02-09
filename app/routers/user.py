from typing import List
from fastapi import Depends, HTTPException, Response, status, FastAPI, APIRouter
from app import schemas, utils
from app.database import get_db, engine
from sqlalchemy.orm import Session
from app.models import UserDB


from dbconnection import connection

# models.Base.metadata.create_all(bind=engine)
rout = APIRouter(prefix="/users", tags=["Users"])
# conn = connection()
# cur = conn.cursor()


@rout.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash_pass(user.password)
    new_user = UserDB(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@rout.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {id}  does not exist",
        )
    return user
