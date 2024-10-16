from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth import auth_api

app = FastAPI(
    title='inventory-control',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PATCH', 'DELETE'],
    allow_headers=['*'],
)

app.include_router(auth_api)
