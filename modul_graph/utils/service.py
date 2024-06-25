from .data_access import da_get_winter_for_module, da_get_module_areas_of_optional_modules, da_get_semester_for_obl_module_via_module_area, da_get_module_areas_of_obligatory_modules, da_get_semester_of_module_cell, da_get_summer_for_module, da_get_module_area_for_module_cell, da_get_module_cells_connected_to_module_areas, da_get_obl_module_via_module_area, da_get_module_areas_for_module, da_get_provided_comps_for_module_list, da_get_provided_comps_per_module, da_get_possible_modules_via_existing_comps, da_get_obl_module_via_module_area


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
            semester_of_module: int = obl_modules_plus_semester[module]
            # if competence is not included in final dict or if the semester of competence provision can be lowered: update dict
            if comp not in competences_plus_semester.keys() or competences_plus_semester[comp] > semester_of_module:
                competences_plus_semester.update({comp: semester_of_module})

    return competences_plus_semester, obligatory_modules


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


# ----------------------------------------------------------------------------------------------------------------------
# private functions

def __get_next_level_modules(comps: list[str], existing_mods: list[str]) -> list[str]:
    result: list[str] = da_get_possible_modules_via_existing_comps(comps)
    # don't include duplicates and bachelor thesis
    modules = list(set(result) - {'Bachelorarbeit'})
    # don't include already used modules in next level modules
    return [item for item in modules if item not in existing_mods]


def __get_next_level_modules_plus_areas(comps: list[str], existing_mods: list[str]) -> tuple[list[str], list[list[str]]]:
    modules: list[str] = __get_next_level_modules(comps, existing_mods)
    areas: list[list[str]] = []
    for mod in modules:
        areas.append(da_get_module_areas_for_module(mod))
    return modules, areas


def __get_free_slots_and_types() -> tuple[list[str], list[list[str]]]:
    mod_areas_obl: list[str] = da_get_module_areas_of_obligatory_modules()
    mod_areas_opt: list[str] = da_get_module_areas_of_optional_modules(mod_areas_obl)
    free_slots: list[str] = da_get_module_cells_connected_to_module_areas(mod_areas_opt)
    types: list[list[str]] = []
    for slot in free_slots:
        types.append(da_get_module_area_for_module_cell(slot))
    return list(set(free_slots)), types


def __get_free_slots_by_type_plus_semester_plus_season() -> tuple[list[list[str]], list[int], list[bool]]:
    free_slots_id: list[str] = __get_free_slots_and_types()[0]
    free_slots: list[list[str]] = __get_free_slots_and_types()[1]
    semesters: list[int] = []
    winter: list[bool] = []

    for cell in free_slots_id:
        semester = da_get_semester_of_module_cell(cell)
        if semester == -1:
            continue
        winter.append(semester % 2 == 1)
        semesters.append(semester)

    # sort by semester
    free_slots_id, free_slots, semesters, winter = zip(*sorted(zip(free_slots_id, free_slots, semesters, winter), key=lambda x: x[2]))

    return free_slots, semesters, winter


# find cell/slot to fill for one module, then delete cell and module from lists
# possible_modules & areas belong together
# free_slots (contains not IDs but types of module cells, p.ex. "WPF Informatik") & semester & winter belong together
def __fit_possible_modules_to_free_slots(possible_modules: list[str], areas: list[list[str]], free_slots: list[list[str]], semester: list[int], winter: list[bool]) -> tuple[str, list[str]]:
    possible_mods_season_winter: list[bool] = []
    possible_mods_season_summer: list[bool] = []
    found_modules: list[str] = []

    # compute for each module if it can be visited during winter or summer
    for i, mod in enumerate(possible_modules):
        possible_mods_season_winter.append(da_get_winter_for_module(mod))
        possible_mods_season_summer.append(da_get_summer_for_module(mod))

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

        status, found_modules = __fit_possible_modules_to_free_slots(possible_modules, areas, free_slots, semester,
                                                                     winter)

        subgraph += found_modules
        competence_pool += da_get_provided_comps_for_module_list(possible_modules)

    return subgraph