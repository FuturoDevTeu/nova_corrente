from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, select
from datetime import datetime

from dependencies import pegar_sessao
from models import Equipe_Atividade, Epi, Atividade, HistoricoConformidade, Atividade_Epi

estatistica_router = APIRouter(prefix="/estatisticas", tags=["Estatísticas"])

@estatistica_router.get("/atividades-mes")
async def contar_equipe_possui_atividade(sessao: Session = Depends(pegar_sessao)):
    try:
        total = sessao.query(func.count()).select_from(Equipe_Atividade).scalar()

        return {
            "total": total
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao contar registros: {e}")

@estatistica_router.get("/conformes")
async def listar_epis_conformes(sessao: Session = Depends(pegar_sessao)):
    try:
        total = (
            sessao.query(func.count(HistoricoConformidade.id))
            .filter(HistoricoConformidade.em_conformidade != 0)
            .scalar()
        )

        return {
            "total": total
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao contar registros: {e}")

@estatistica_router.get("/nao-conformes")
async def contar_nao_conformes(sessao: Session = Depends(pegar_sessao)):
    try:
        total = (
            sessao.query(func.count(HistoricoConformidade.id))
            .filter(HistoricoConformidade.em_conformidade == 0)
            .scalar()
        )

        return {
            "total": total
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao contar registros: {e}")
    
@estatistica_router.get("/atividades-pizza")
async def grafico_atividades_pizza(sessao: Session = Depends(pegar_sessao)):
    try:
        # Query: pega o nome da atividade e quantas vezes ela aparece na tabela intermediária
        resultados = (
            sessao.query(
                Atividade.nome,
                func.count(Equipe_Atividade.c.Equipe_idEquipe).label("quantidade")
            )
            .join(Equipe_Atividade, Atividade.id == Equipe_Atividade.c.Atividade_idAtividade)
            .group_by(Atividade.nome)
            .all()
        )

        # Se não houver nada
        if not resultados:
            return {"labels": [], "values": []}

        # Quebra em listas
        labels = [r[0] for r in resultados]
        values = [r[1] for r in resultados]

        return {
            "labels": labels,
            "values": values
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao gerar gráfico: {e}")
    
    