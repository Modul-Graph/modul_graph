"""
This file contains all routes that get, create, edit or delete modules
"""
from fastapi import APIRouter
from utils.router_service import RouterService
from DTOs import ModuleDTO

router = APIRouter(prefix="/module")


@router.get("/{name}")
def get_module(name: str) -> ModuleDTO:
    return RouterService().get_module(name)


@router.post("/")
def create_module(module: ModuleDTO):
    return RouterService().create_module(module)


@router.delete("/{name}")
def delete_module(name: str):
    return RouterService().delete_module(name)


@router.put("/")
def update_module(module: ModuleDTO):
    return RouterService().update_module(module)