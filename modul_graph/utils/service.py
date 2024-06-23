from .repository import get_obl_module_via_module_area, get_semester_for_obl_module_via_module_area, get_module_areas_of_obligatory_modules, get_provided_comps_per_module, get_possible_modules_plus_provided_comps_via_existing_comps, get_provided_comps_for_module_list, get_possible_modules_via_existing_comps, get_module_areas_for_optional_modules, get_module_cells_connected_to_module_area
from neomodel import db


def test_db_connection() -> bool:
    result, meta = db.cypher_query('MATCH p=(:Module)-[r:PROVIDES]->(:Competence) RETURN p', resolve_objects=True)
    if len(result) > 1:
        return False
    return True


def get_start_competences_plus_semester() -> dict[str, int]:
    # get names of moduleAreas connected to obligatory modules
    module_areas, meta1 = get_module_areas_of_obligatory_modules()

    # declaration of variables
    obligatory_modules: list[str] = []
    semesters: list[int] = []
    ignored_modules: list[str] = []     # in case it needs to be accessed at some point
    competences_plus_semester: dict[str, int] = dict()

    # get obligatory modules and their corresponding semesters
    for module_area in module_areas:
        semester, meta3 = get_semester_for_obl_module_via_module_area(module_area[0])
        # bachelor thesis and minor module don't have one single semester specified
        if len(semester) != 1 or len(semester[0]) != 1:
            ignored_modules.append(module_area[0][0])
        else:
            semesters.append(semester[0][0])
            obl_module, meta2 = get_obl_module_via_module_area(module_area[0])
            obligatory_modules.append(obl_module[0][0])
    obl_modules_plus_semester = dict(zip(obligatory_modules, semesters))

    # get competences provided by obligatory modules and their earliest possible time of provision
    for module in obligatory_modules:
        comps, meta4 = get_provided_comps_per_module(module)
        # if comps is empty, foreach will throw error
        if len(comps) < 1:
            continue
        for comp in comps:
            semester_of_module: int = obl_modules_plus_semester[module]
            comp_unwind = comp[0]
            # if competence is not included in final dict or if the semester of competence provision can be lowered: update dict
            if comp_unwind not in competences_plus_semester.keys() or competences_plus_semester[comp_unwind] > semester_of_module:
                competences_plus_semester.update({comp_unwind: semester_of_module})

    return competences_plus_semester


def __get_next_level_modules(comps: list[str]) -> list[list[str], list[str]]:
    result, meta = get_possible_modules_via_existing_comps(comps)
    return result


def __get_next_level_comps(modules: list[str]) -> list[str]:
    result, meta = get_provided_comps_for_module_list(modules)
    return result


def __get_free_slots() -> list[str]:
    mod_areas_obl, meta1 = get_module_areas_of_obligatory_modules()
    mod_areas_opt, meta2 = get_module_areas_for_optional_modules(__unwind(mod_areas_obl))
    free_slots, meta3 = get_module_cells_connected_to_module_area(__unwind(mod_areas_opt))
    return list(set(__unwind(free_slots)))


# returns list of "module + semester" tuples
def __get_subgraph(start_comps: list[str]) -> list[str]:
    subgraph: list[str] = []
    free_slots: int = len(__get_free_slots())
    competence_pool: list[str] = start_comps.copy()

    while free_slots > 0:
        possible_modules, meta = get_possible_modules_via_existing_comps(competence_pool)
        __unwind(possible_modules)
        if len(possible_modules) == 0:
            return []
        free_slots -= len(possible_modules)
        while free_slots < 0:
            possible_modules.pop()
            free_slots += 1
        subgraph += possible_modules
        competence_pool += get_provided_comps_for_module_list(possible_modules)

    return subgraph


def __unwind(nested_list: list[str]):
    for i, mod in enumerate(nested_list):
        nested_list[i] = nested_list[i][0]
    return nested_list


def does_fitting_subgraph_exist(start_comps: list[str]) -> bool:
    subgraph: list[str] = __get_subgraph(start_comps)
    # enough modules to fill WPF slots?
    if not subgraph:
        return False
    else:
        return fitting_algorithm(subgraph)


def fitting_algorithm(subgraph) -> bool:
    return True