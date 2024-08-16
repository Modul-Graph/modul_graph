from fastapi import FastAPI
from neomodel import config # type: ignore
from starlette.middleware.cors import CORSMiddleware

from .routes.analysis import router as analysis_router
from .routes.module import router as module_router
from .routes.standard_curriculum import router as sc_router

# Setup DB connection params
config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'  # default

app = FastAPI(root_path="/api/v1")
app.include_router(analysis_router)
app.include_router(sc_router)
app.include_router(module_router)
# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
