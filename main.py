from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException

from models import Gender, Role, UpdateUserRequest, User

app = FastAPI()


db: List[User] = [
    User(id=UUID("944fa4a5-a9c6-43fa-9f2d-22ee52cd3915"), 
         first_name="Kunal",
         last_name="Pandey",
         gender=Gender.male,
         roles=[Role.student]
         ),
    User(id=UUID("a04a9680-3f93-4258-acb5-7f4f8c694328"), 
         first_name="Pratibha",
         last_name="Sonare",
         gender=Gender.female,
         roles=[Role.student]
         )
]

@app.get("/")
async def root():
    return {"hello":"world"} 

@app.get("/api/v1/users")
async def fetch_users():
    return db

@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code=404,
        detail=f"user {user_id} not found"
    )

@app.put("/api/v1/users/{user_id}/{first_name}")
async def update_first_name(user_id: UUID, first_name: str):
    for user in db:
        if user.id == user_id:
            user.first_name = first_name
            return
    raise HTTPException(
        status_code=404,
        detail=f"User: {user_id} is not present in out record!"
    )

@app.put("/api/v1/users/{user_id}")
async def update_user_info(user_info: UpdateUserRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_info.first_name is not None:
                user.first_name = user_info.first_name
            if user_info.middle_name is not None:
                user.middle_name = user_info.middle_name
            if user_info.last_name is not None:
                user.last_name = user_info.last_name
            if user_info.gender is not None:
                user.gender = user_info.gender
            if user_info.roles is not None:
                user.roles = user_info.roles
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with user id: {user_id} is not available in our records!"
    )