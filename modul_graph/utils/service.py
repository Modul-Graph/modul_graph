from typing import Tuple, List, Dict, Any

from .repository import get_obl_module_via_module_area, get_semester_for_obl_module_via_module_area, get_module_areas_of_obligatory_modules, get_provided_comps_per_module, get_possible_modules_plus_provided_comps_via_existing_comps, get_provided_comps_for_module_list, get_possible_modules_via_existing_comps, get_module_areas_for_optional_modules, get_module_cells_connected_to_module_areas, get_semester_of_module_cell, get_module_areas_for_module, get_module_area_for_module_cell, get_summer_for_module, get_winter_for_module
from neomodel import db


def test_db_connection() -> bool:
    result, meta = db.cypher_query('MATCH p=(:Module)-[r:PROVIDES]->(:Competence) RETURN p', resolve_objects=True)
    if len(result) > 1:
        return False
    return True


def get_start_competences_plus_semester_and_obl_mods() -> tuple[dict[str, int], list[str]]:
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

    return competences_plus_semester, obligatory_modules


def __get_next_level_modules(comps: list[str], existing_mods: list[str]) -> list[str]:
    result, meta = get_possible_modules_via_existing_comps(comps)
    __unwind(result)
    # don't include duplicates and bachelor thesis
    modules = list(set(result) - {'Bachelorarbeit'})
    # don't include already used modules in next level modules
    return [item for item in modules if item not in existing_mods]


def __get_next_level_modules_plus_areas(comps: list[str], existing_mods: list[str]) -> tuple[list[str], list[list[str]]]:
    modules: list[str] = __get_next_level_modules(comps, existing_mods)
    areas: list[list[str]] = []
    for mod in modules:
        result, meta = get_module_areas_for_module(mod)
        areas.append(__unwind(result))
    return modules, areas


def __get_next_level_comps(modules: list[str]) -> list[str]:
    result, meta = get_provided_comps_for_module_list(modules)
    return __unwind(result)


def __get_free_slots_and_types() -> tuple[list[str], list[list[str]]]:
    mod_areas_obl, meta1 = get_module_areas_of_obligatory_modules()
    mod_areas_opt, meta2 = get_module_areas_for_optional_modules(__unwind(mod_areas_obl))
    free_slots, meta3 = get_module_cells_connected_to_module_areas(__unwind(mod_areas_opt))
    __unwind(free_slots)
    types: list[list[str]] = []
    for slot in free_slots:
        # [0] to not get meta data from query
        types.append(__unwind(get_module_area_for_module_cell(slot)[0]))
    return list(set(free_slots)), types


def __get_semester_of_mod_cell(cell: str) -> int:
    result, meta = get_semester_of_module_cell(cell)
    return __unwind(result)[0]


def __get_free_slots_by_type_plus_semester_plus_season() -> tuple[list[list[str]], list[int], list[bool]]:
    free_slots_id: list[str] = __get_free_slots_and_types()[0]
    free_slots: list[list[str]] = __get_free_slots_and_types()[1]
    semesters: list[int] = []
    winter: list[bool] = []

    for cell in free_slots_id:
        semester = __get_semester_of_mod_cell(cell)
        winter.append(semester % 2 == 1)
        semesters.append(semester)

    # sort by semester
    free_slots_id, free_slots, semesters, winter = zip(*sorted(zip(free_slots_id, free_slots, semesters, winter), key=lambda x: x[2]))

    return free_slots, semesters, winter


# find cell/slot to fill for one module, then delete cell and module from lists
# possible_modules & areas belong together
# free_slots (contains not IDs but types of module cells, p.ex. "WPF Informatik") & semester & winter belong together
def fit_possible_modules_to_free_slots(possible_modules: list[str], areas: list[list[str]], free_slots: list[list[str]], semester: list[int], winter: list[bool]) -> \
tuple[str, list[Any]] | tuple[str, list[str]]:
    possible_mods_season_winter: list[bool] = []
    possible_mods_season_summer: list[bool] = []
    found_modules: list[str] = []

    # compute for each module if it can be visited during winter or summer
    for i, mod in enumerate(possible_modules):
        possible_mods_season_winter.append(__unwind(get_winter_for_module(mod)[0])[0])
        possible_mods_season_summer.append(__unwind(get_summer_for_module(mod)[0])[0])

    for i, slot in enumerate(free_slots):
        found_module: str = ''
        for j, singleSlot in enumerate(slot):
            for k, mod in enumerate(possible_modules):
                matches_summer_winter: bool = (possible_mods_season_summer[k] and not winter) or (possible_mods_season_winter[k] and winter[j])
                if matches_summer_winter and singleSlot in areas[k]:
                    found_module = mod
                    break
            if found_module != '':
                found_modules.append(found_module)
                index_to_remove: int = possible_modules.index(found_module)
                possible_modules.pop(index_to_remove)
                areas.pop(index_to_remove)
                possible_mods_season_summer.pop(index_to_remove)
                possible_mods_season_winter.pop(index_to_remove)
                break
        if found_module == '':
            return "", found_modules

    return "SUCCESS", found_modules


def __get_subgraph_for_feasibility_analysis(start_comps: list[str]) -> list[str]:
    subgraph: list[str] = []
    free_slots, semester, winter = __get_free_slots_by_type_plus_semester_plus_season()
    competence_pool: list[str] = start_comps.copy()
    status: str = ""

    while status != "SUCCESS":
        # list[str], list[list[str]]
        possible_modules, areas = __get_next_level_modules_plus_areas(competence_pool, get_start_competences_plus_semester_and_obl_mods()[1])
        possible_modules = [item for item in possible_modules if item not in subgraph]
        if len(possible_modules) == 0:
            return []

        status, found_modules = fit_possible_modules_to_free_slots(possible_modules, areas, free_slots, semester, winter)

        subgraph += found_modules
        competence_pool += __get_next_level_comps(possible_modules)

    return subgraph


def __unwind(nested_list):
    for i, mod in enumerate(nested_list):
        nested_list[i] = nested_list[i][0]
    return nested_list


def does_feasible_subgraph_exist(start_comps: list[str]) -> bool:
    subgraph: list[str] = __get_subgraph_for_feasibility_analysis(start_comps)
    # enough modules to fill WPF slots?
    # 'not subgraph' means __get_subgraph... returned []
    if not subgraph:
        return False
    return True


def fitting_algorithm(subgraph) -> bool:
    # todo: implement
    return True