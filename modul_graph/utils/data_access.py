from .repository import db_get_module_via_module_area, db_get_semester_for_obl_module_via_module_area, db_get_module_areas_of_obligatory_modules, db_get_provided_comps_for_module, db_get_provided_comps_for_module_list_plus_sem_of_provision, db_get_possible_modules_via_existing_comps, db_get_module_areas_of_optional_modules, db_get_module_cells_connected_to_module_areas, db_get_semester_of_module_cell, db_get_module_areas_for_module, db_get_module_area_for_module_cell, db_get_summer_for_module, db_get_winter_for_module, db_get_possible_modules_plus_provided_comps_via_existing_comps, db_get_standard_curricula, db_get_winter_for_standard_curriculum, db_get_needed_comps_for_module, db_get_previous_modules_for_single_module, db_get_highest_semester_of_std_curr, db_get_modules_indirectly_connected_to_comp, db_get_providing_modules_for_comp, db_get_comp_existing
from neomodel import db


# data_access processes data for and from repository:
# - prep for repo: prep list arguments for cypher syntax
# - processing returned values: unwind nested lists and remove metadata


def test_db_connection() -> bool:
    result, meta = db.cypher_query('MATCH p=(:Module)-[r:PROVIDES]->(:Competence) RETURN p', resolve_objects=True)
    if len(result) > 1:
        return False
    return True


# ----------------------------------------------------------------------------------------------------------------------
# get standard curriculum
def da_get_standard_curricula() -> list[str]:
    result: list[list[str]] = db_get_standard_curricula()[0]
    return __unwind(result)


# ----------------------------------------------------------------------------------------------------------------------
# get module area(s)
def da_get_module_areas_of_obligatory_modules() -> list[str]:
    result: list[list[str]] = db_get_module_areas_of_obligatory_modules()[0]
    return __unwind(result)


def da_get_module_areas_for_module(module: str) -> list[str]:
    result: list[list[str]] = db_get_module_areas_for_module(module)[0]
    return __unwind(result)


def da_get_module_areas_of_optional_modules_unwound_no_duplicates(obl_module_areas: list[str]) -> list[str]:
    result: list[list[str]] = db_get_module_areas_of_optional_modules(__prepare_list_as_cypher_var(obl_module_areas))[0]
    # a module could belong to several areas -> then inner nested list of result won't contain single element -> unwind() can't be used here
    ret: list[str] = []
    if len(result) < 1:
        return ret
    for nested_list in result:
        for item in nested_list:
            ret.append(item)
            # remove duplicates
    ret = list(set(ret))
    return ret


def da_get_module_area_for_module_cell(module_cell: str) -> list[str]:
    result: list[list[str]] = db_get_module_area_for_module_cell(module_cell)[0]
    return list(set(__unwind(result)))


# ----------------------------------------------------------------------------------------------------------------------
# get semester(s)
def da_get_semester_for_obl_module_via_module_area(module_area: str) -> list[int]:  # returns list because bachelor thesis and minor module don't have single semester entry
    result: list[list[int]] = db_get_semester_for_obl_module_via_module_area(module_area)[0]
    return __unwind(result)


# ! check return value for -1 when using da_get_semester_of_module_cell()
def da_get_semester_of_module_cell(module_cell: str) -> int:
    result: list[list[int]] = db_get_semester_of_module_cell(module_cell)[0]
    unwind_result = __unwind(result)
    # unwind_result could be emtpy
    if len(unwind_result) > 0:
        return unwind_result[0]
    else:
        return -1


def da_get_highest_semester_of_std_curr() -> int:
    result: list[list[int]] = db_get_highest_semester_of_std_curr()[0]
    return result[0][0]


# ----------------------------------------------------------------------------------------------------------------------
# get module(s)
def da_get_obl_module_via_module_area(module_area: str) -> str:
    result: list[list[str]] = db_get_module_via_module_area(module_area)[0]
    unwind_result: list[str] = __unwind(result)
    # a module area belonging to an obligatory module is connected to only one module
    # and so the inner nested list contains only one element -> can be referenced via []
    if len(unwind_result) > 0:
        return unwind_result[0]
    # separate return case if list empty, because referencing empty list via [0] would throw error
    else:
        return ''


def da_get_possible_modules_via_existing_comps(comps: list[str]) -> list[str]:
    result: list[list[str]] = db_get_possible_modules_via_existing_comps(__prepare_list_as_cypher_var(comps))[0]
    return __unwind(result)


# currently not in use
def da_get_possible_modules_plus_provided_comps_via_existing_comps(comps: list[str]) -> list[list[str]]:
    result: list[list[str]] = db_get_possible_modules_plus_provided_comps_via_existing_comps(__prepare_list_as_cypher_var(comps))[0]
    return result


def da_get_previous_modules_for_single_module(new_mod: str, existing_mods: list[str]) -> list[str]:
    result: list[list[str]] = db_get_previous_modules_for_single_module(new_mod, __prepare_list_as_cypher_var(existing_mods))[0]
    return list(set(__unwind(result)))


def da_get_modules_indirectly_connected_to_comp(comp: str) -> list[str]:
    result: list[list[str]] = db_get_modules_indirectly_connected_to_comp(comp)[0]
    return __unwind(result)


def da_get_providing_modules_for_comp(comp: str) -> list[str]:
    result: list[list[str]] = db_get_providing_modules_for_comp(comp)[0]
    return __unwind(result)


# ----------------------------------------------------------------------------------------------------------------------
# get competence(s)
def da_get_provided_comps_per_module(module: str) -> list[str]:
    result: list[list[str]] = db_get_provided_comps_for_module(module)[0]
    return __unwind(result)


def da_get_provided_comps_for_module_list_plus_sem_of_provision_without_duplicates(modules: list[str]) -> tuple[list[str], list[int]]:

    # result format: list[list['comp', 'semester_of_module']] with several inner lists -> unwind doesn't work
    result: list[tuple[str | int]] = db_get_provided_comps_for_module_list_plus_sem_of_provision(__prepare_list_as_cypher_var(modules))[0]
    # comps, sems: tuple[list[str], list[int]] -- or [] if no values in result
    if len(result) < 1:
        return [], []
    comps, sems = zip(*result)
    # needs to be list because later on, pop() is needed
    comps = list(comps)
    # comps are provided one semester AFTER the module took place
    sems = [x + 1 for x in sems]

    # throw out duplicates and only keep the one with the lowest semester
    duplicate_comps: list[str] = [item for item in set(comps) if comps.count(item) > 1]
    indices_to_delete: list[int] = []
    for i, dupl_comp in enumerate(duplicate_comps):
        indices_of_double_comp: list[int] = [c for c in range(len(comps)) if comps[c] == dupl_comp]
        sem_of_comp_provision: int = 100     # random high number, has to be higher than semester count in standard curriculum
        index_to_keep: int = len(indices_of_double_comp)
        for ind in indices_of_double_comp:
            if sems[ind] < sem_of_comp_provision:
                sem_of_comp_provision = sems[ind]
                index_to_keep = ind
        indices_to_delete += [index_to_delete for index_to_delete in indices_of_double_comp if index_to_delete != index_to_keep]

    indices_to_keep: list[int] = [i for i in range(len(comps)) if i not in indices_to_delete]
    comps_to_keep: list[str] = [comps[i] for i in range(len(comps)) if i in indices_to_keep]
    sems_to_keep: list[int] = [sems[i] for i in range(len(comps)) if i in indices_to_keep]
    return comps_to_keep, sems_to_keep


def da_get_needed_comps_for_module(module: str) -> list[str]:
    result: list[list[str]] = db_get_needed_comps_for_module(module)[0]
    return __unwind(result)


def da_get_comp_existing(comp: str) -> bool:
    result: list[list[str]] = db_get_comp_existing(comp)[0]
    if not result[0][0]:
        return False
    return True


# ----------------------------------------------------------------------------------------------------------------------
# get module cell(s)
def da_get_module_cells_connected_to_module_areas_without_duplicates(module_areas: list[str]) -> list[str]:
    result: list[list[str]] = db_get_module_cells_connected_to_module_areas(__prepare_list_as_cypher_var(module_areas))[0]
    return list(set(__unwind(result)))


# ----------------------------------------------------------------------------------------------------------------------
# get season(s) for modules and standard curriculum
def da_get_summer_for_module(module: str) -> bool:
    result: list[list[bool]] = db_get_summer_for_module(module)[0]
    unwind_result = __unwind(result)
    # unwind_result could be emtpy
    if len(unwind_result) > 0:
        return unwind_result[0]
    else:
        return False


def da_get_winter_for_module(module: str) -> bool:
    result: list[list[bool]] = db_get_winter_for_module(module)[0]
    unwind_result = __unwind(result)
    # unwind_result could be emtpy
    if len(unwind_result) > 0:
        return unwind_result[0]
    else:
        return False


def da_get_winter_for_standard_curriculum(name: str) -> bool:
    result: list[list[bool]] = db_get_winter_for_standard_curriculum(name)[0]
    # start_winter is required attribute, must be present -> no error when accessing by [0][0]
    return result[0][0]


# ----------------------------------------------------------------------------------------------------------------------
# helper

# should only be used for lists where the inner nested lists contain only one element each
# that means, the cypher query should have returned one single column
# unwinding is necessary for nested lists because accessing the inner list of result=list[list[...]] by result[0] might throw "index out of range" error
def __unwind(nested_list: list[list[str | int | bool]]) -> list[str | int | bool]:
    ret: list[str | int | bool] = []
    for i, mod in enumerate(nested_list):
        if len(nested_list[i]) > 1:
            print("\nDon't do that, unwind should be used carefully.\n")
        ret.append(nested_list[i][0])
    return ret


def __prepare_list_as_cypher_var(input_list: list[str]):
    for i, item in enumerate(input_list):
        if not input_list[i].startswith('\''):
            input_list[i] = '\'' + input_list[i]
        if not input_list[i].endswith('\''):
            input_list[i] = input_list[i] + '\''
    return input_list