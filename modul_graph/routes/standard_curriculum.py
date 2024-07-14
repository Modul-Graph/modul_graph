"""
This file contains all routes that get, transform or create standard curriculums
"""
from typing import List

from fast_api import APIRouter
from neomodel import NodeSet  # type: ignore

from modul_graph.models.standard_curriculum import StandardCurriculumDTO, StandardCurriculum

__router = APIRouter(
    prefix="/sc",
)


@__router.get("/get_all", tags=["READ"])
async def get_standard_curriculums() -> List[StandardCurriculumDTO]:
    """
    Get all standard curriculums available in the database
    :return: List of all standard curriculums
    """
    res: List[StandardCurriculumDTO] = []

    for node in StandardCurriculum.nodes():
        assert isinstance(node, StandardCurriculum)

        res.append(node.serialize)

    return res
