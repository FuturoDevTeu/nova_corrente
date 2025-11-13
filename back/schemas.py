from pydantic import BaseModel
from typing import Optional, List

class UsuarioSchemas(BaseModel):
    login: str
    senha: str
    class Config:
        from_attributes = True

class FuncionarioSchemas(BaseModel):
    nome: str

    class Config:
        from_attributes = True




