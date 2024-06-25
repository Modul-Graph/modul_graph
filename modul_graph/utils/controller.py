from .service import get_start_competences_plus_semester_and_obl_mods, does_feasible_subgraph_exist


def is_feasible(standard_curriculum: str) -> bool:
    # todo: pass argument through to db (to all cypher queries, esp. attention to lookup of obl mods)
    start_comps = list(get_start_competences_plus_semester_and_obl_mods()[0].keys())
    return does_feasible_subgraph_exist(start_comps)


def get_example_graphs() -> list[list[str, int]]:
    # todo: implement
    pass