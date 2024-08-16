"""
This file contains all routes that get, create, edit or delete modules
"""
from fastapi import APIRouter, Response
from modul_graph.utils.router_service import RouterService
from modul_graph.DTOs import ModuleDTO

router = APIRouter(prefix="/module")


@router.get("/{name}")
async def get_module(name: str) -> ModuleDTO:
    return RouterService().get_module(name)


@router.post("/")
async def create_module(module: ModuleDTO) -> Response:
    RouterService().create_module(module)
    return Response(status_code=201)


@router.delete("/{name}")
async def delete_module(name: str) -> Response:
    RouterService().delete_module(name)
    return Response(status_code=201)


@router.put("/{name}")  # old name (unique) as path param
async def update_module(name: str, module: ModuleDTO) -> Response:
    RouterService().update_module(name, module)
    return Response(status_code=201)

