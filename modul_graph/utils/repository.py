from neomodel import db


def get_module_areas_of_obligatory_modules():
    return db.cypher_query('MATCH (n:ModuleArea)<-[:FILLS]-(m:Module) WITH n, count(DISTINCT m) AS relCount WHERE relCount = 1 RETURN n.name')


def get_semester_for_obl_module_via_module_area(module_area: str):
    return db.cypher_query('MATCH (m:ModuleArea {name: \'' + module_area + '\'})-[:FILLS]->(:ModuleCell)-[:IS_IN]->(s:Semester) RETURN s.number')


def get_obl_module_via_module_area(module_area: str):
    return db.cypher_query('MATCH (m:ModuleArea {name: \'' + module_area + '\'})<-[:FILLS]-(n:Module) RETURN n.name')


def get_provided_comps_per_module(module: str):
    return db.cypher_query('MATCH (m:Module {name: \'' + module + '\'})-[:PROVIDES]->(c:Competence) RETURN c.name')


def get_provided_comps_for_module_list(modules: list[str]):
    modules = prepare_list_as_cypher_var(modules)
    return db.cypher_query('MATCH (m:Module)-[:PROVIDES]->(c:Competence) WHERE m.name in [' + ', '.join(modules) + '] RETURN c.name')


def get_possible_modules_plus_provided_comps_via_existing_comps(comps: list[str]):
    comps = prepare_list_as_cypher_var(comps)
    return db.cypher_query('MATCH (c1:Competence)<-[:NEEDS]-(m:Module)-[:PROVIDES]->(c2:Competence) WHERE c1.name in [' + ', '.join(comps) + '] RETURN m.name, c2.name')


def get_possible_modules_via_existing_comps(comps: list[str]):
    comps = prepare_list_as_cypher_var(comps)
    return db.cypher_query('MATCH (c:Competence)<-[:NEEDS]-(m:Module) WHERE c.name in [' + ', '.join(comps) + '] RETURN m.name')


def get_module_areas_for_module(module: str):
    return db.cypher_query('MATCH (n:ModuleArea)<-[:FILLS]-(:Module {name:\'' + module + '\'}) RETURN n.name')


def prepare_list_as_cypher_var(input_list: list[str]):
    for i, item in enumerate(input_list):
        if not input_list[i].startswith('\''):
            input_list[i] = '\'' + input_list[i]
        if not input_list[i].endswith('\''):
            input_list[i] = input_list[i] + '\''
    return input_list


def get_module_areas_for_optional_modules(obl_module_areas: list[str]):
    obl_module_areas = prepare_list_as_cypher_var(obl_module_areas)
    return db.cypher_query('MATCH (n:ModuleArea) WHERE not n.name IN [' + ', '.join(obl_module_areas) + '] RETURN n.name')


def get_module_cells_connected_to_module_areas(module_area: list[str]):
    module_areas = prepare_list_as_cypher_var(module_area)
    return db.cypher_query('MATCH (mc:ModuleCell)<-[:FILLS]-(ma:ModuleArea) WHERE ma.name in [' + ', '.join(module_areas) + '] RETURN mc.identifier')


def get_semester_of_module_cell(module_cell: str):
    return db.cypher_query('MATCH (:ModuleCell {identifier:\'' + module_cell + '\'})-[:IS_IN]->(s:Semester) RETURN s.number')


def get_module_area_for_module_cell(module_cell: str):
    return db.cypher_query('MATCH (:ModuleCell {identifier:\'' + module_cell + '\'})<-[:FILLS]-(m:ModuleArea) RETURN m.name')


def get_summer_for_module(module: str):
    return db.cypher_query('MATCH (m:Module {name:\'' + module + '\'}) RETURN m.is_in_summer')


def get_winter_for_module(module: str):
    return db.cypher_query('MATCH (m:Module {name:\'' + module + '\'}) RETURN m.is_in_winter')