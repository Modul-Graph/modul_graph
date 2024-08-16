"""
This file contains all routes that get, create, edit or delete modules
"""
from fastapi import APIRouter, Response

from modul_graph.DTOs import ModuleDTO
from modul_graph.utils.router_service import RouterService

router = APIRouter(prefix="/module")


@router.get("/{name}")
def get_module(name: str) -> ModuleDTO:
    return RouterService().get_module(name)


@router.post("/")
def create_module(module: ModuleDTO) -> Response:
    RouterService().create_module(module)
    return Response(status_code=201)


@router.delete("/{name}")
def delete_module(name: str) -> Response:
    RouterService().delete_module(name)
    return Response(status_code=201)


@router.put("/")
def update_module(module: ModuleDTO) -> Response:
    RouterService().update_module(module)
    return Response(status_code=201)
