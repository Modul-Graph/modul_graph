from .service import does_feasible_subgraph_exist, get_path_to_competence
from .data_access import da_get_standard_curricula


def is_feasible(standard_curriculum: str) -> bool:
    if standard_curriculum not in da_get_standard_curricula():
        raise ValueError(f'"{standard_curriculum}" is an invalid name. Valid would be {da_get_standard_curricula()}')

    return does_feasible_subgraph_exist(standard_curriculum)


def get_example_graph(wanted_competence: str, standard_curriculum: str) -> list[list[str | list[int]] | list[list[int]]]:
    return get_path_to_competence(wanted_competence, standard_curriculum)