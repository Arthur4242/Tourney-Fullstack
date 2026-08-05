from fastapi import FastAPI

from backend.src.models.base import Base
from backend.src.database.database import engine

from backend.src.api.routes.usuario import router as usuario_router
from backend.src.api.routes.torneio import router as torneio_router

# Aplicação da API
app = FastAPI(
    title="Tournament API",
    version="1.0.0"
)

# Criar as tabelas
Base.metadata.create_all(bind=engine)

# Incluir as rotas
app.include_router(usuario_router)
app.include_router(torneio_router)