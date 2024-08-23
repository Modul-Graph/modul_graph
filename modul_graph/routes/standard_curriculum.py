"""
This file contains all routes that get, transform or create standard curriculums
"""
from typing import List

from fastapi import APIRouter
from neomodel import NodeSet, CardinalityViolation  # type: ignore

from modul_graph.models.module_area import ModuleArea
from modul_graph.DTOs import StandardCurriculumDTO, CompetenceScDTO
from modul_graph.models.standard_curriculum import StandardCurriculum
from modul_graph.utils.analysis_controller import get_competence_sc as get_competence_sc_service
from modul_graph.models.module import Module

router = APIRouter(
    prefix="/sc",
)


@router.get("/get_all", tags=["READ"])
async def get_standard_curriculums() -> List[StandardCurriculumDTO]:
    """
    Get all standard curriculums available in the database
    :return: List of all standard curriculums
    """
    res: List[StandardCurriculumDTO] = []

    for node in StandardCurriculum.nodes.all():
        assert isinstance(node, StandardCurriculum)

        res.append(node.serialize)

    return res


@router.get("/get_modules")
async def get_std_curr_modules(sc_name: str) -> List[str]:
    res: List[str] = []

    sc: StandardCurriculum = StandardCurriculum.nodes.get(name=sc_name)

    for elem in sc.has_module.all():
        assert isinstance(elem, Module)

        res.append(elem.name)

    return res


@router.get("/get_module_areas")
async def get_std_curr_module_areas(sc_name: str) -> List[str]:
    res: List[str] = []

    sc: StandardCurriculum = StandardCurriculum.nodes.get(name=sc_name)

    for module in sc.has_module.all():
        try:
            for module_area in module.fills_module_area.all():
                assert isinstance(module_area, ModuleArea)

                res.append(module_area.name)
        except CardinalityViolation:
            # some modules don't fill module areas
            # (even though they should)
            # -> cardinality violated
            pass

    return res


@router.get("/competence/{sc}", tags=["READ"])
async def get_competence_sc(sc: str) -> CompetenceScDTO:
    return get_competence_sc_service(sc)
