from fastapi import FastAPI
from neomodel import config  # type: ignore
from starlette.middleware.cors import CORSMiddleware

from .routes.analysis import router as analysis_router
from .routes.module import router as module_router
from .routes.standard_curriculum import router as sc_router
from .routes.module_area import router as module_area_router
from .routes.cell import router as cell_router
from .routes.cp_cluster import router as cp_cluster_router

# Setup DB connection params
config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'  # default

app = FastAPI(root_path="/api/v1", response_model_exclude_none=True)

app.include_router(analysis_router)
app.include_router(sc_router)
app.include_router(module_router)
app.include_router(module_area_router)

app.include_router(cp_cluster_router)

app.include_router(cell_router)

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
