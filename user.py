from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    tags=["Users"]
)

## CREATING USERS:

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    user_data = user.dict()
    
    exist = db.query(models.User).filter(models.User.email == user_data['email']).first()
    if exist is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=f"This email: {user_data['email']} is already registered. Please use another email or renew your password for this one.")
    
    exist = db.query(models.User).filter(models.User.username == user_data['username']).first()
    if exist is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=f"This username: {user_data['username']} is already taken. Please choose another username.")
    
    db_user = models.User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
