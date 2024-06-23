from neomodel import db


def get_module_areas_of_obligatory_modules():
    return db.cypher_query('MATCH (n:ModuleArea)<-[:FILLS]-(m:Module) WITH n, count(DISTINCT m) AS relCount WHERE relCount = 1 RETURN n.name')


def get_semester_for_obl_module_via_module_area(module_area: str) -> int:
    return db.cypher_query('MATCH (m:ModuleArea {name: \'' + module_area[0] + '\'})-[:FILLS]->(:ModuleCell)-[:IS_IN]->(s:Semester) RETURN s.number')


def get_obl_module_via_module_area(module_area: str) -> str:
    return db.cypher_query('MATCH (m:ModuleArea {name: \'' + module_area[0] + '\'})<-[:FILLS]-(n:Module) RETURN n.name')


def get_provided_comps_per_module(module: str) -> list[str]:
    return db.cypher_query('MATCH (m:Module {name: \'' + module + '\'})-[:PROVIDES]->(c:Competence) RETURN c.name')