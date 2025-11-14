from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from models import Atividade
from main import bcrypt_context
from sqlalchemy.orm import Session

atividade_router = APIRouter(prefix="/atividade", tags=["atividade"])


@atividade_router.get("/listar")
async def listar(sessao: Session = Depends(pegar_sessao)):
    try:
        atividades = sessao.query(Atividade).all()

        # Caso não exista nenhuma
        if not atividades:
            return {"mensagem": "Nenhuma atividade cadastrada."}

        # Converter para formato JSON-friendly
        retorno = []
        for a in atividades:
            retorno.append({
                "id": a.id,
                "nome": a.nome
            })

        return retorno

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar atividades: {str(e)}")
