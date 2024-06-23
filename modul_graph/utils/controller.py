from .service import get_start_competences_plus_semester, does_fitting_subgraph_exist


def is_feasible(standard_curriculum: str):
    start_comps = list(get_start_competences_plus_semester().keys())
    feasible: bool = does_fitting_subgraph_exist(start_comps)
    print(feasible)


def get_example_graphs() -> list[list[str, int]]:
    pass