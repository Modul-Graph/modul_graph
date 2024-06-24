from .service import get_start_competences_plus_semester_and_obl_mods, does_feasible_subgraph_exist


def is_feasible(standard_curriculum: str):
    # todo: pass argument through to db
    start_comps = list(get_start_competences_plus_semester_and_obl_mods()[0].keys())
    feasible: bool = does_feasible_subgraph_exist(start_comps)
    print(feasible)


def get_example_graphs() -> list[list[str, int]]:
    # todo: implement
    pass