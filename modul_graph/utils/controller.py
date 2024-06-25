from .service import get_start_competences_plus_semester_and_obl_mods, does_feasible_subgraph_exist
from .std_curr import instantiate_std_curr_obj


def is_feasible(standard_curriculum: str) -> bool:
    instantiate_std_curr_obj(standard_curriculum)
    start_comps = list(get_start_competences_plus_semester_and_obl_mods()[0].keys())
    return does_feasible_subgraph_exist(start_comps)


def get_example_graphs() -> list[list[str, int]]:
    # todo: implement
    pass