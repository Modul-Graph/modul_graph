from .repository import db_get_module_via_module_area, db_get_semester_for_obl_module_via_module_area, db_get_module_areas_of_obligatory_modules, db_get_provided_comps_per_module, db_get_provided_comps_for_module_list, db_get_possible_modules_via_existing_comps, db_get_module_areas_of_optional_modules, db_get_module_cells_connected_to_module_areas, db_get_semester_of_module_cell, db_get_module_areas_for_module, db_get_module_area_for_module_cell, db_get_summer_for_module, db_get_winter_for_module, db_get_possible_modules_plus_provided_comps_via_existing_comps, db_get_standard_curricula
from neomodel import db


# data_access processes data for and from repository:
# - prep for repo: prep list arguments for cypher syntax
# - processing returned values: unwind nested lists and remove metadata

def test_db_connection() -> bool:
    result, meta = db.cypher_query('MATCH p=(:Module)-[r:PROVIDES]->(:Competence) RETURN p', resolve_objects=True)
    if len(result) > 1:
        return False
    return True


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


def da_get_module_areas_of_optional_modules(obl_module_areas: list[str]) -> list[str]:
    result: list[list[str]] = db_get_module_areas_of_optional_modules(__prepare_list_as_cypher_var(obl_module_areas))[0]
    return __unwind(result)


def da_get_module_area_for_module_cell(module_cell: str) -> list[str]:
    result: list[list[str]] = db_get_module_area_for_module_cell(module_cell)[0]
    return __unwind(result)


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


# ----------------------------------------------------------------------------------------------------------------------
# get competence(s)
def da_get_provided_comps_per_module(module: str) -> list[str]:
    result: list[list[str]] = db_get_provided_comps_per_module(module)[0]
    return __unwind(result)


def da_get_provided_comps_for_module_list(modules: list[str]) -> list[str]:
    result: list[list[str]] = db_get_provided_comps_for_module_list(__prepare_list_as_cypher_var(modules))[0]
    return __unwind(result)


# ----------------------------------------------------------------------------------------------------------------------
# get module cell(s)
def da_get_module_cells_connected_to_module_areas(module_areas: list[str]) -> list[str]:
    result: list[list[str]] = db_get_module_cells_connected_to_module_areas(__prepare_list_as_cypher_var(module_areas))[0]
    return __unwind(result)


# ----------------------------------------------------------------------------------------------------------------------
# get season(s)
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


# ----------------------------------------------------------------------------------------------------------------------
# helper

# should only be used for lists where the inner nested lists contain only one element each
# that means, the cypher query should have returned one single column
# unwinding is necessary for nested lists because accessing the inner list of result=list[list[...]] by result[0] might throw "index out of range" error
def __unwind(nested_list: list[list[str | int | bool]]) -> list[str | int | bool]:
    ret: list[str | int | bool] = []
    for i, mod in enumerate(nested_list):
        ret.append(nested_list[i][0])
    return ret


def __prepare_list_as_cypher_var(input_list: list[str]):
    for i, item in enumerate(input_list):
        if not input_list[i].startswith('\''):
            input_list[i] = '\'' + input_list[i]
        if not input_list[i].endswith('\''):
            input_list[i] = input_list[i] + '\''
    return input_list