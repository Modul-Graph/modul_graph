from fastapi import APIRouter, Response

from modul_graph.utils.semester_router_service import SemesterRouterService

router = APIRouter(
    prefix="/semester",
)


@router.post("/{number}")
async def create_semester(number: int) -> Response:
    SemesterRouterService().create_semester(number)
    return Response(status_code=201)


@router.delete("/{number}")
async def delete_semester(number: int) -> Response:
    SemesterRouterService().delete_semester(number)
    return Response(status_code=200)