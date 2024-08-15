from fastapi import HTTPException

from .service import get_start_competences_plus_semester_and_obl_mods, does_feasible_subgraph_exist
from .std_curr import instantiate_std_curr_obj
from .data_access import da_get_standard_curricula
from ..DTOs import CompetenceScDTO
from ..models.standard_curriculum import StandardCurriculum

from .service import get_competence_sc as service_get_competence_sc


def is_feasible(standard_curriculum: str) -> bool:
    if standard_curriculum not in da_get_standard_curricula():
        raise ValueError(f'"{standard_curriculum}" is an invalid name. Valid would be {da_get_standard_curricula()}')
    instantiate_std_curr_obj(standard_curriculum)
    return does_feasible_subgraph_exist(tuple(get_start_competences_plus_semester_and_obl_mods()))


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


def get_example_graphs() -> list[list[str, int]]:
    # todo: implement
    pass
