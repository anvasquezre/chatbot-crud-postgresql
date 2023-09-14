from fastapi import FastAPI
from v1 import app



api = FastAPI()

api.include_router(app.router, include_in_schema=True)

