from .service import get_start_competences_plus_semester, enough_modules_to_fill_slots


def is_feasible(standard_curriculum: str):
    start_comps = list(get_start_competences_plus_semester().keys())
    feasible: bool = enough_modules_to_fill_slots(start_comps)
    print(feasible)


def get_example_graphs() -> list[list[str, int]]:
    pass