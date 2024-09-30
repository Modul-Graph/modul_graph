"""
This file contains all routes that get, transform or create standard curriculums
"""
from typing import List
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Response

from modul_graph.models.competence import Competence
from modul_graph.utils.module_area_router_service import ModuleAreaRouterService
from modul_graph.utils.module_router_service import ModuleRouterService
from modul_graph.utils.sc_DAO import get_rich_cp_clusters
from modul_graph.utils.sc_router_service import ScRouterService  # type: ignore
from neomodel import NodeSet, CardinalityViolation  # type: ignore

from modul_graph.DTOs import StandardCurriculumDTO, CompetenceScDTO, GraphDisplayResponseDTO, RichCPCluster, \
    GraphDisplayResponseNodeDTO, CellDTO
from modul_graph.models.module import Module
from modul_graph.models.module_area import ModuleArea
from modul_graph.models.module_cell import ModuleCell
from modul_graph.models.semester import Semester
from modul_graph.models.standard_curriculum import StandardCurriculum
from modul_graph.utils.analysis_DAO import da_get_standard_curricula
from modul_graph.utils.analysis_controller import get_competence_sc as get_competence_sc_service

router = APIRouter(
    prefix="/sc",
)


@router.get("/module_areas")
async def get_module_areas() -> List[str]:
    """
    Get all module areas of a standard curriculum
    :return: list of all module areas
    """
    module_areas: list[ModuleArea] = ModuleArea.nodes.all()
    return [module_area.name for module_area in module_areas]

@router.get("/wpf_module_areas")
async def get_all_wpf_module_areas() -> List[str]:
    """
    Get all WPF module areas
    :return: list of all wpf module area names
    """

    module_areas: NodeSet = ModuleArea.nodes.all()
    return [module_area.name for module_area in module_areas if module_area.is_wpf]

@router.get("/get_all", tags=["READ"])
async def get_standard_curriculums() -> List[StandardCurriculumDTO]:
    """
    Get all standard curriculums available in the database
    :return: List of all standard curriculums
    """
    res: List[StandardCurriculumDTO] = []

    for node in StandardCurriculum.nodes.all():
        assert isinstance(node, StandardCurriculum)

        res.append(StandardCurriculumDTO(name=node.name, start_winter=node.start_winter))

    return res


@router.get("/get_modules")
async def get_std_curr_modules(sc_name: str, ignore_wpf: bool = False) -> List[str]:
    res: List[str] = []

    sc: StandardCurriculum = StandardCurriculum.nodes.get(name=sc_name)

    for elem in sc.has_module.all():
        assert isinstance(elem, Module)

        # Ignore WPF mod
        module_areas: list[ModuleArea] = elem.fills_module_area.all()
        if ignore_wpf and any([not area.is_wpf for area in module_areas]):
            continue

        res.append(elem.name)

    return res


@router.get("/get_module_areas")
async def get_std_curr_module_areas(sc_name: str) -> List[str]:
    res: List[str] = []

    sc: StandardCurriculum = StandardCurriculum.nodes.get(name=sc_name)

    for module in sc.has_module.all():
        for module_area in module.fills_module_area.all():
            assert isinstance(module_area, ModuleArea)

            # Only append module area if it is a WPF module area
            if module_area.is_wpf:
                res.append(module_area.name)

    return res


@router.get("/competence/{sc}", tags=["READ"])
async def get_competence_sc(sc: str) -> CompetenceScDTO:
    return get_competence_sc_service(sc)


@router.put("/change_semester_count")
async def update_semester_connections(sc_name: str, semesters: List[int]) -> Response:
    sc: StandardCurriculum = StandardCurriculum.nodes.get(name=sc_name)
    if not sc:
        return Response(status_code=404, content="Standard Curriculum not found")

    ScRouterService().update_semester_connections(sc, semesters)

    return Response(status_code=200)


@router.get("/get_sc_graph", tags=["READ"])
async def get_sc_graph(sc_name: str) -> GraphDisplayResponseDTO:
    """
    Get the graph of a standard curriculum
    :param sc_name: the name of the standard curriculum
    :return: the graph of the standard curriculum
    """

    nodes: set[GraphDisplayResponseNodeDTO] = set()

    sc: StandardCurriculum = StandardCurriculum.nodes.get(name=sc_name)
    semesters: list[Semester] = sc.specifies_semester.all()
    for semester in semesters:

        module_cells: list[ModuleCell] = list(semester.contains_module_cell.all())

        for module_cell in module_cells:
            module_areas: list[ModuleArea] = list(module_cell.filled_by_module_area.all())
            wpf_module_areas = [module_area for module_area in module_areas if module_area.is_wpf]

            for wpf_module_area in wpf_module_areas:
                nodes.add(GraphDisplayResponseNodeDTO(id=f"wpf_module_area.name-{uuid4()}", label=wpf_module_area.name,
                                                      semester=semester.number))

            pflicht_module_areas = [module_area for module_area in module_areas if not module_area.is_wpf]

            for pflicht_module_area in pflicht_module_areas:
                pflicht_module: Module = pflicht_module_area.filled_by_module.single()
                nodes.add(GraphDisplayResponseNodeDTO(id=f"pflicht_module.name-{uuid4()}", label=pflicht_module.name,
                                                      semester=semester.number))

    return GraphDisplayResponseDTO(nodes=nodes, edges=set())


@router.get("/get_rich_cp_cluster")
def get_rich_cp_cluster(sc_name: str) -> list[RichCPCluster]:
    """
    GET rich CP clusters of a standard curriculum
    :param sc_name: the name of the standard curriculum
    :return: list of all cp clusters in the SC enriched with module information
    """

    if sc_name not in da_get_standard_curricula():
        raise HTTPException(status_code=406, detail="missing standard curriculum")

    print("test")

    sc: StandardCurriculum = StandardCurriculum.nodes.get(name=sc_name)

    return get_rich_cp_clusters(sc)


@router.get("/get_competences")
def get_competences() -> list[str]:
    """
    Return all comptences in sc
    :param sc_name: name
    :return: list of comptences
    """

    competences: list[Competence] = Competence.nodes.all()

    return [comp.name for comp in competences]


@router.get("/get_potential_cell_content")
def get_potential_cell_content() -> list[CellDTO]:
    """
    Get potential cell content for a standard curriculum
    :param sc_name: the name of the standard curriculum
    :return: list of potential cell content
    """

    module_areas: list[ModuleArea] = ModuleArea.nodes.all()
    print(module_areas)
    pflicht_module_areas: list[Module] = [area.filled_by_module.single() for area in module_areas if
                                          not area.is_wpf and len(area.fills_module_cell.all()) == 0]

    print(pflicht_module_areas)
    wpf_module_areas: list[ModuleArea] = [area for area in module_areas if area.is_wpf]

    res: list[CellDTO] = []

    for module in pflicht_module_areas:
        print(module)
        res.append(CellDTO(contains_wpf=False, data=ModuleRouterService().get_module(module.name)))

    for module_area in wpf_module_areas:
        res.append(CellDTO(contains_wpf=True, data=ModuleAreaRouterService().get_module_area(module_area.name)))

    return res


@router.get("/get_semesters")
def get_semesters() -> list[int]:
    """
    Get all semesters of a standard curriculum
    :param sc_name: the name of the standard curriculum
    :return: list of all semesters
    """

    return [semester.number for semester in Semester.nodes.all()]

@router.put("/competence/{name}")
def create_competence(name: str) -> None:
    """
    Create a competence
    :param name: the name of the competence
    """

    c = Competence.nodes.first_or_none(name=name)

    if c is not None:
        return

    comp: Competence = Competence(name=name)
    comp.save()
@router.delete("/competence/{name}")
def delete_competence(name: str) -> None:
    """
    Delete a competence
    :param name:
    :return:
    """

    c = Competence.nodes.first_or_none(name=name)

    if c is None:
        return

    c.delete()
