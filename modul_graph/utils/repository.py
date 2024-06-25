from neomodel import db


# repository sends cypher queries to db, each of which returns tuple of result and metadata
# structure of return type: tuple[list[list[str|int|...]], list[str]]
#   = tuple[list_of_rows[list_of_content_of_each_column_for_one_row], list_of_column_names]


# ----------------------------------------------------------------------------------------------------------------------
# get module area(s)
def db_get_module_areas_of_obligatory_modules() -> tuple[list[list[str]], list[str]]:
    return db.cypher_query('MATCH (n:ModuleArea)<-[:FILLS]-(m:Module) WITH n, count(DISTINCT m) AS relCount WHERE relCount = 1 RETURN n.name')


def db_get_module_areas_for_module(module: str) -> tuple[list[list[str]], list[str]]:
    return db.cypher_query('MATCH (n:ModuleArea)<-[:FILLS]-(:Module {name:\'' + module + '\'}) RETURN n.name')


def db_get_module_areas_of_optional_modules(obl_module_areas: list[str]) -> tuple[list[list[str]], list[str]]:
    return db.cypher_query('MATCH (n:ModuleArea) WHERE not n.name IN [' + ', '.join(obl_module_areas) + '] RETURN n.name')


def db_get_module_area_for_module_cell(module_cell: str) -> tuple[list[list[str]], list[str]]:
    return db.cypher_query('MATCH (:ModuleCell {identifier:\'' + module_cell + '\'})<-[:FILLS]-(m:ModuleArea) RETURN m.name')


# ----------------------------------------------------------------------------------------------------------------------
# get semester(s)
def db_get_semester_for_obl_module_via_module_area(module_area: str) -> tuple[list[list[int]], list[str]]:
    return db.cypher_query('MATCH (m:ModuleArea {name: \'' + module_area + '\'})-[:FILLS]->(:ModuleCell)-[:IS_IN]->(s:Semester) RETURN s.number')


def db_get_semester_of_module_cell(module_cell: str) -> tuple[list[list[int]], list[str]]:
    return db.cypher_query('MATCH (:ModuleCell {identifier:\'' + module_cell + '\'})-[:IS_IN]->(s:Semester) RETURN s.number')


# ----------------------------------------------------------------------------------------------------------------------
# get module(s)
def db_get_module_via_module_area(module_area: str) -> tuple[list[list[str]], list[str]]:
    return db.cypher_query('MATCH (m:ModuleArea {name: \'' + module_area + '\'})<-[:FILLS]-(n:Module) RETURN n.name')


def db_get_possible_modules_via_existing_comps(comps: list[str]) -> tuple[list[list[str]], list[str]]:
    return db.cypher_query('MATCH (c:Competence)<-[:NEEDS]-(m:Module) WHERE c.name in [' + ', '.join(comps) + '] RETURN m.name')


# currently not in use
def db_get_possible_modules_plus_provided_comps_via_existing_comps(comps: list[str]) -> tuple[list[list[str]], list[str]]:
    return db.cypher_query('MATCH (c1:Competence)<-[:NEEDS]-(m:Module)-[:PROVIDES]->(c2:Competence) WHERE c1.name in [' + ', '.join(comps) + '] RETURN m.name, c2.name')


# ----------------------------------------------------------------------------------------------------------------------
# get competence(s)
def db_get_provided_comps_per_module(module: str) -> tuple[list[list[str]], list[str]]:
    return db.cypher_query('MATCH (m:Module {name: \'' + module + '\'})-[:PROVIDES]->(c:Competence) RETURN c.name')


def db_get_provided_comps_for_module_list(modules: list[str]) -> tuple[list[list[str]], list[str]]:
    return db.cypher_query('MATCH (m:Module)-[:PROVIDES]->(c:Competence) WHERE m.name in [' + ', '.join(modules) + '] RETURN c.name')


# ----------------------------------------------------------------------------------------------------------------------
# get module cell(s)
def db_get_module_cells_connected_to_module_areas(module_areas: list[str]) -> tuple[list[list[str]], list[str]]:
    return db.cypher_query('MATCH (mc:ModuleCell)<-[:FILLS]-(ma:ModuleArea) WHERE ma.name in [' + ', '.join(module_areas) + '] RETURN mc.identifier')


# ----------------------------------------------------------------------------------------------------------------------
# get season(s)
def db_get_summer_for_module(module: str) -> tuple[list[list[bool]], list[str]]:
    return db.cypher_query('MATCH (m:Module {name:\'' + module + '\'}) RETURN m.is_in_summer')


def db_get_winter_for_module(module: str) -> tuple[list[list[bool]], list[str]]:
    return db.cypher_query('MATCH (m:Module {name:\'' + module + '\'}) RETURN m.is_in_winter')