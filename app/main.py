from fastapi import Depends, FastAPI

from app.routers import users, sms

app = FastAPI()

app.include_router(users.router)
app.include_router(sms.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
