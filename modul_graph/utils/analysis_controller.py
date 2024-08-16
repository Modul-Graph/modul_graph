from fastapi import HTTPException

from modul_graph.DTOs import AnalysisResponseDTO, AnalysisStatus, CompetenceScDTO
from .analysis_DAO import da_get_standard_curricula, da_get_providing_modules_for_comp, da_get_comp_existing
from .analysis_service import does_feasible_subgraph_exist, get_path_to_competence, \
    get_competence_sc as service_get_competence_sc
from .graph_exception import GraphException
from ..models.standard_curriculum import StandardCurriculum


def is_feasible(standard_curriculum: str) -> bool:
    if standard_curriculum not in da_get_standard_curricula():
        raise HTTPException(status_code=406, detail=AnalysisResponseDTO(status=AnalysisStatus.error,
                                                                        message=f'"{standard_curriculum}" is an invalid name'))

    try:
        return does_feasible_subgraph_exist(standard_curriculum)
    except GraphException as ex:
        raise HTTPException(status_code=404, detail=ex.dto)


def get_example_graph(wanted_competence: str, standard_curriculum: str) -> list[tuple[str, str, list[int], list[str]]]:
    if not da_get_comp_existing(wanted_competence):
        raise HTTPException(status_code=406, detail=AnalysisResponseDTO(status=AnalysisStatus.error,
                                                                        message=f'The requested competition does not exist.'))
    if not da_get_providing_modules_for_comp(wanted_competence):
        raise HTTPException(status_code=406, detail=AnalysisResponseDTO(status=AnalysisStatus.error,
                                                                        message='The requested competence is not being provided by any module'))

    try:
        return get_path_to_competence(wanted_competence, standard_curriculum)
    except GraphException as ex:
        raise HTTPException(status_code=404, detail=ex.dto)


def get_competence_sc(raw_sc: str) -> CompetenceScDTO:
    """
    Get competence standard curriculum
    :param raw_sc: standard curriculum to get competence standard curriculum for
    :raise HTTPException: if the standard curriculum does not exist
    :return: competence standard curriculum dto
    """
    if raw_sc not in da_get_standard_curricula():
        raise HTTPException(status_code=404, detail=f'"{raw_sc}" is not existing')
    else:
        sc: StandardCurriculum = StandardCurriculum.nodes.get(name=raw_sc)
        return service_get_competence_sc(sc)
