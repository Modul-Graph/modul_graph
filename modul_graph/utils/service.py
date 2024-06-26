from .data_access import da_get_winter_for_module, da_get_module_areas_of_optional_modules_unwound_no_duplicates, da_get_semester_for_obl_module_via_module_area, da_get_module_areas_of_obligatory_modules, da_get_semester_of_module_cell, da_get_summer_for_module, da_get_module_area_for_module_cell, da_get_module_cells_connected_to_module_areas_without_duplicates, da_get_obl_module_via_module_area, da_get_module_areas_for_module, da_get_provided_comps_for_module_list_plus_sem_of_provision_without_duplicates, da_get_provided_comps_per_module, da_get_possible_modules_via_existing_comps, da_get_obl_module_via_module_area, da_get_winter_for_standard_curriculum
from .std_curr import std_curr
from collections import Counter

# service provides controller with processed data and gets its data from data_access (NOT from repository)


# ----------------------------------------------------------------------------------------------------------------------
# public functions (accessed by controller)

def get_start_competences_plus_semester_and_obl_mods() -> tuple[dict[str, int], list[str]]:
    # get names of module areas connected to obligatory modules (each will be single module area, not list)
    module_areas: list[str] = da_get_module_areas_of_obligatory_modules()

    # declaration of variables
    obligatory_modules: list[str] = []
    semesters: list[int] = []
    ignored_modules: list[str] = []     # in case it needs to be accessed at some point
    competences_plus_semester: dict[str, int] = dict()

    # get obligatory modules and their corresponding semesters
    for module_area in module_areas:
        semester: list[int] = da_get_semester_for_obl_module_via_module_area(module_area)
        # bachelor thesis and minor module don't have one single semester specified
        if len(semester) != 1:
            ignored_modules.append(module_area)
        else:
            semesters.append(semester[0])
            obl_module: str = da_get_obl_module_via_module_area(module_area)
            obligatory_modules.append(obl_module)
    obl_modules_plus_semester = dict(zip(obligatory_modules, semesters))

    # get competences provided by obligatory modules and their earliest possible time of provision
    for module in obligatory_modules:
        comps: list[str] = da_get_provided_comps_per_module(module)
        # if comps is empty, foreach would throw error
        if len(comps) < 1:
            continue
        for comp in comps:
            semester_of_comp_provision: int = obl_modules_plus_semester[module] + 1
            # if competence is not yet included in dict or if the semester of competence provision can be lowered: update dict
            if comp not in competences_plus_semester.keys() or competences_plus_semester[comp] > semester_of_comp_provision:
                competences_plus_semester.update({comp: semester_of_comp_provision})

    return competences_plus_semester, obligatory_modules


def does_feasible_subgraph_exist(start_comps_plus_sem_and_obl_mods: tuple[dict[str, int], list[str]]) -> bool:
    subgraph: list[str] = __get_subgraph_for_feasibility_analysis(start_comps_plus_sem_and_obl_mods)
    # enough modules to fill free slots?
    # 'not subgraph' means __get_subgraph... returned []
    if not subgraph:
        return False
    return True


# ----------------------------------------------------------------------------------------------------------------------
# private functions

def __get_subgraph_for_feasibility_analysis(start_comps_plus_sem_and_obl_mods: tuple[dict[str, int], list[str]]) -> list[str]:
    # subgraph initialised to obligatory modules
    subgraph: list[str] = start_comps_plus_sem_and_obl_mods[1]
    types_of_free_slots, sems_of_free_slots, winter_of_free_slots = __get_free_slots_by_type_plus_semester_plus_season()
    if len(types_of_free_slots) == 0:
        return ['No slots for optional Modules']
    competence_pool: list[str] = list(start_comps_plus_sem_and_obl_mods[0].keys())
    provided_in_sem: list[int] = list(start_comps_plus_sem_and_obl_mods[0].values())
    status: str = ""

    for curr_sem in range(min(sems_of_free_slots), max(sems_of_free_slots) + 1):

        # get provided competences up until current semester
        limited_comps: list[str] = [competence_pool[i] for i in range(len(competence_pool)) if provided_in_sem[i] <= curr_sem]

        # list[str], list[list[str]]
        possible_modules, areas_of_poss_mods = __get_next_level_modules_plus_areas(limited_comps, subgraph)
        areas_of_poss_mods = [areas_of_poss_mods[i] for i in range(len(possible_modules)) if possible_modules[i] not in subgraph]
        possible_modules = [item for item in possible_modules if item not in subgraph]
        if len(possible_modules) == 0:
            return []

        status, found_modules, types_of_free_slots, winter_of_free_slots = __fit_possible_modules_to_free_slots(possible_modules, areas_of_poss_mods, list(types_of_free_slots), list(winter_of_free_slots))
        subgraph += found_modules
        if not types_of_free_slots:
            return subgraph
        comps_of_found_modules, sems_of_comp_provision = da_get_provided_comps_for_module_list_plus_sem_of_provision_without_duplicates(found_modules)
        competence_pool += comps_of_found_modules
        provided_in_sem += sems_of_comp_provision

        # delete duplicates from competence_pool and provided_in_sem
        # explanation: key is unique value from competence_pool which has duplicates in competence_pool
        indices_containing_duplicates: list[int] = [i for key in (key for key, count in Counter(competence_pool).items() if count > 1) for i, x in enumerate(competence_pool) if x == key]
        first_index_per_duplicate: list[int] = [competence_pool.index(key) for key, count in Counter(competence_pool).items()]
        indices_to_delete: list[int] = list(set(indices_containing_duplicates) - set(first_index_per_duplicate))
        provided_in_sem = [sem for i, sem in enumerate(provided_in_sem) if i not in indices_to_delete]
        competence_pool = [comp for i, comp in enumerate(competence_pool) if i not in indices_to_delete]

    if len(types_of_free_slots) != 0:
        return []
    return subgraph


def __get_free_slots_by_type_plus_semester_plus_season() -> tuple[list[list[str]], list[int], list[bool]]:
    free_slots_ids: list[str] = __get_free_slots_and_types()[0]
    free_slots_types: list[list[str]] = __get_free_slots_and_types()[1]
    semesters: list[int] = []
    winter: list[bool] = []

    for cell in free_slots_ids:
        semester = da_get_semester_of_module_cell(cell)
        if semester == -1:
            continue
        # if standard curriculum starts in winter, semesters with odd numbers are in winter
        res_modulo: int = 1 if da_get_winter_for_standard_curriculum(std_curr.name) else 0
        winter.append(semester % 2 == res_modulo)
        semesters.append(semester)

    # sort by semester
    if len(free_slots_ids) != 0:
        sorted_by_sem: list[any] = zip(*sorted(zip(free_slots_ids, free_slots_types, semesters, winter), key=lambda x: x[2]))
        free_slots_ids, free_slots_types, semesters, winter = sorted_by_sem

    return free_slots_types, semesters, winter


def __get_free_slots_and_types() -> tuple[list[str], list[list[str]]]:
    mod_areas_obl: list[str] = da_get_module_areas_of_obligatory_modules()
    mod_areas_opt: list[str] = da_get_module_areas_of_optional_modules_unwound_no_duplicates(mod_areas_obl)
    free_slots: list[str] = da_get_module_cells_connected_to_module_areas_without_duplicates(mod_areas_opt)
    types: list[list[str]] = []
    for slot in free_slots:
        types.append(da_get_module_area_for_module_cell(slot))
    return list(set(free_slots)), types


def __get_next_level_modules_plus_areas(comps: list[str], existing_mods: list[str]) -> tuple[list[str], list[list[str]]]:
    modules: list[str] = __get_next_level_modules(comps, existing_mods)
    modules = list(set(modules))
    areas: list[list[str]] = []
    for mod in modules:
        areas.append(da_get_module_areas_for_module(mod))
    return modules, areas


def __get_next_level_modules(comps: list[str], existing_mods: list[str]) -> list[str]:
    result: list[str] = da_get_possible_modules_via_existing_comps(comps)
    # don't include duplicates and bachelor thesis
    modules = list(set(result) - {'Bachelorarbeit'} - {'Praktikum'})
    # don't include already used modules in next level modules
    return [item for item in modules if item not in existing_mods]


# find cell/slot to fill for one module, then delete cell and module from lists
# possible_modules & areas belong together
# free_slots (contains not IDs but types of module cells, p.ex. "WPF Informatik") & semester & winter belong together
def __fit_possible_modules_to_free_slots(possible_modules: list[str], areas_of_poss_mods: list[list[str]], types_of_free_slots: list[list[str]], winter_of_free_slots: list[bool]) -> tuple[str, list[str], list[list[str]], list[bool]]:
    possible_mods_season_winter: list[bool] = []
    possible_mods_season_summer: list[bool] = []
    found_modules: list[str] = []
    indices_to_remove_from_free_slot_lists: list[int] = []

    # compute for each module if it can be visited during winter or summer
    for i, mod in enumerate(possible_modules):
        possible_mods_season_winter.append(da_get_winter_for_module(mod))
        possible_mods_season_summer.append(da_get_summer_for_module(mod))

    # copy because the list itself will be modified in the loop
    for i, slot in enumerate(types_of_free_slots.copy()):
        found_module: str = ''
        for j, single_slot_type in enumerate(slot):
            for k, mod in enumerate(possible_modules):
                matches_summer_winter: bool = (possible_mods_season_summer[k] and not winter_of_free_slots[j]) or (possible_mods_season_winter[k] and winter_of_free_slots[j])
                if matches_summer_winter and single_slot_type in areas_of_poss_mods[k]:
                    found_module = mod
                    break
            if found_module != '':
                found_modules.append(found_module)
                index_to_remove: int = possible_modules.index(found_module)
                possible_modules.pop(index_to_remove)
                areas_of_poss_mods.pop(index_to_remove)
                possible_mods_season_summer.pop(index_to_remove)
                possible_mods_season_winter.pop(index_to_remove)
                indices_to_remove_from_free_slot_lists.append(i)
                break
        if found_module == '':
            remaining_free_slots, and_their_winter = __remove_indices(types_of_free_slots, winter_of_free_slots, indices_to_remove_from_free_slot_lists)
            return "", found_modules, remaining_free_slots, and_their_winter

    remaining_free_slots, and_their_winter = __remove_indices(types_of_free_slots, winter_of_free_slots, indices_to_remove_from_free_slot_lists)
    return "SUCCESS", found_modules, remaining_free_slots, and_their_winter


def __remove_indices(list1: list[list[str]], list2: list[bool], indices: list[int]) -> tuple[list[list[str]], list[bool]]:
    ret_list1: list[list[str]] = [item for i, item in enumerate(list1) if i not in indices]
    ret_list2: list[bool] = [item for i, item in enumerate(list2) if i not in indices]
    return ret_list1, ret_list2