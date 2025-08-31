from fastapi import FastAPI
from fastapi import APIRouter
import routers


app = FastAPI()

app.include_router(
    routers.router,
    prefix='/posts',
    tags=['Post']
)