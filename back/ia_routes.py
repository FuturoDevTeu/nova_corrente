from fastapi import APIRouter
from projetoia import ia
ia_router = APIRouter(prefix="/ia", tags=["ia"])

@ia_router.get("/")
async def home():
    return {"mensagem":"ia"}

@ia_router.get("/analisar")
async def validar():
    epis_faltando, status_text = await ia.analisar()
    print(epis_faltando, status_text)
    
    