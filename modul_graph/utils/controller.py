from .service import does_feasible_subgraph_exist, get_path_to_competence
from .data_access import da_get_standard_curricula, da_get_providing_modules_for_comp, da_get_comp_existing
from modul_graph.DTOs import AnalysisResponseDTO, AnalysisStatus
from .graph_exception import GraphException


def is_feasible(standard_curriculum: str) -> bool:
    if standard_curriculum not in da_get_standard_curricula():
        raise GraphException(f'"{standard_curriculum}" is an invalid name. Valid would be {da_get_standard_curricula()}')
    return does_feasible_subgraph_exist(standard_curriculum)


def get_example_graph(wanted_competence: str, standard_curriculum: str) -> list[list[str | list[int]] | list[list[int]]]:
    if not da_get_comp_existing(wanted_competence):
        raise GraphException('The requested competition does not exist.')
    if not da_get_providing_modules_for_comp(wanted_competence):
        raise GraphException('The requested competence is not being provided by any module in your selected standard curriculum.')
    return get_path_to_competence(wanted_competence, standard_curriculum)