import gettext

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .routes.analysis import router as analysis_router
from .routes.standard_curriculum import router as standard_curriculum_router

from neomodel import config

# Setup DB connection params
config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'  # default

app = FastAPI(root_path="/api/v1")
app.include_router(analysis_router)
app.include_router(standard_curriculum_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
