from fastapi import HTTPException

from modul_graph.DTOs import CompetenceScDTO
from modul_graph.models.standard_curriculum import StandardCurriculum
from modul_graph.utils.analysis_DAO import da_get_standard_curricula
from modul_graph.utils.analysis_service import get_competence_sc as service_get_competence_sc


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
