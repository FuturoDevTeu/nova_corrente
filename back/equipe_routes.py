from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from models import Equipe, Funcionario, Atividade, FuncionarioEquipe, Foto, HistoricoConformidade
from projetoia.ia import analisar
import os
import shutil
import json

equipe_router = APIRouter(prefix="/equipe", tags=["equipe"])

@equipe_router.post("/cadastrar")
async def cadastrar(
    atividade: str = Form(...),
    nome_funcionarios: str = Form(...),  # virá como JSON string
    imagens: list[UploadFile] = File(...),
    sessao: Session = Depends(pegar_sessao)
):
    try:
        try:
            nomes = json.loads(nome_funcionarios)
            if isinstance(nomes, str):
                nomes = [nomes]
        except json.JSONDecodeError:
            nomes = [nome_funcionarios]

        
        temp_dir = "uploads_temp"
        os.makedirs(temp_dir, exist_ok=True)

        # Criar equipe
        nova_equipe = Equipe()
        sessao.add(nova_equipe)
        sessao.flush()

        # Atividade
        atividade_existente = sessao.query(Atividade).filter_by(nome=atividade).first()
        if not atividade_existente:
            atividade_existente = Atividade(nome=atividade)
            sessao.add(atividade_existente)
            sessao.flush()

        nova_equipe.atividades.append(atividade_existente)

        resultados_ia = []
        em_conformidade_geral = True  # se alguma imagem for fora de conformidade, vira False

        # Criar funcionários e vínculos com equipe
        for nome_funcionario in nomes:
            funcionario = sessao.query(Funcionario).filter_by(nome=nome_funcionario).first()
            if not funcionario:
                funcionario = Funcionario(nome=nome_funcionario)
                sessao.add(funcionario)
                sessao.flush()

            func_eq = FuncionarioEquipe(funcionario_id=funcionario.id, equipe_id=nova_equipe.id)
            sessao.add(func_eq)
            sessao.flush()

        # Processar as imagens enviadas
        for img_file in imagens:
            caminho_imagem = os.path.join(temp_dir, img_file.filename)
            with open(caminho_imagem, "wb") as buffer:
                shutil.copyfileobj(img_file.file, buffer)

            # --- 🔍 Rodar IA ---
            epis_faltando, status_text, caminho_resultado = await analisar(caminho_imagem)

            # Se algum resultado for fora de conformidade, marca a equipe como fora
            if status_text == "FORA DE CONFORMIDADE":
                em_conformidade_geral = False

            # Salvar foto original (ou a analisada)
            foto = Foto(foto=caminho_resultado)
            sessao.add(foto)
            sessao.flush()

            resultados_ia.append({
                "imagem": img_file.filename,
                "faltando": epis_faltando,
                "status": status_text
            })

        # Salvar histórico da equipe
        historico = HistoricoConformidade(
            equipe_id=nova_equipe.id,
            em_conformidade=em_conformidade_geral,
            observacao="Todas as imagens analisadas" if em_conformidade_geral else "Equipe fora de conformidade em uma ou mais imagens"
        )
        sessao.add(historico)
        sessao.commit()

        return {
            "mensagem": "Equipe cadastrada e imagens analisadas com sucesso",
            "conformidade_geral": "EM CONFORMIDADE" if em_conformidade_geral else "FORA DE CONFORMIDADE",
            "resultados": resultados_ia
        }

    except Exception as e:
        sessao.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao cadastrar equipe: {e}")
