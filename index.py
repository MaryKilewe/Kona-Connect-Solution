from __future__ import print_function

import time
from typing import Any, Dict, Optional

from fastapi import FastAPI

from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select

import datetime
from flask_login import current_user

class User(SQLModel, table=True):
    # TODO change the default value to the timestamp that the user is created
    id: Optional[int] = Field(default=datetime.datetime.utcnow, primary_key=True)
    name: str
    secret_name: str
    age: Optional[str] = None
      
engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)
# Create an instance of the API class
app = FastAPI()

@app.get("/")
async def root():
    # TODO include the user's name if they are logged in
    if current_user and current_user.is_authenticated():
        users_name = current_user.name
        return {"message": "Hello {}".format(users_name)}
    return {"message": "Hello {}".format("World")}


@app.post("/user")
async def create_new_user(*, user: User):    
    with Session(engine) as session:
      session.add(user)
      session.flush()
      session.commit()
    # TODO return the User ID
    users_id = user.id
    msg = f"User created with ID {users_id}"
    return {"message": msg}
    
@app.get("/user/{id}")
async def get_user(id: int):
  with Session(engine) as session:
     # TODO return the user based on the ID (and an error if not)
     statement = select(User).where(User.name == id)     
     user = session.exec(statement).first()
     if user:
        return {"user": user}
     else:
        return {'msg': 'User not found. A user with this ID does not exist in the system'}

@app.get("/api/webhooks")
async def handle_hook(*, event: Any):
    id = event.payload.conversation.id
    return {"message": "Hello World"}


  








