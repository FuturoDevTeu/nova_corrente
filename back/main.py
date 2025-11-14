from fastapi import FastAPI
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

import os

app = FastAPI()

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos
    allow_headers=["*"],  # Permite todos os headers
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from auth_routes import auth_router

app.include_router(auth_router)

from funcionario_routes import funcionario_router
app.include_router(funcionario_router)

from equipe_routes import equipe_router
app.include_router(equipe_router)

from estatistica_routes import estatistica_router
app.include_router(estatistica_router)

from ia_routes import ia_router
app.include_router(ia_router)

from atividade_routes import atividade_router
app.include_router(atividade_router)

