from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routers import users, sms

app = FastAPI()

app.include_router(users.router)
app.include_router(sms.router)


@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')