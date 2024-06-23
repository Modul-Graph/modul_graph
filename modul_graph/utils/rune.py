from neomodel import db


# Funktionen in __main__.py schreiben (nach Dateneintrag in DB)
# console: python -m modul_graph
def test_db_connection() -> bool:
    result, meta = db.cypher_query('MATCH p=(:Module)-[r:PROVIDES]->(:Competence) RETURN p', resolve_objects=True)
    print("TEST")
    print(result)
    print(meta)
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
        semester, meta3 = get_semester_for_obl_module_via_module_area(module_area)
        # bachelor thesis and minor module don't have one single semester specified
        if len(semester) != 1 or len(semester[0]) != 1:
            ignored_modules.append(module_area[0][0])
        else:
            semesters.append(semester[0][0])
            obl_module, meta2 = get_obl_module_via_module_area(module_area)
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


def get_module_areas_of_obligatory_modules():
    return db.cypher_query('MATCH (n:ModuleArea)<-[:FILLS]-(m:Module) WITH n, count(DISTINCT m) AS relCount WHERE relCount = 1 RETURN n.name')


def get_semester_for_obl_module_via_module_area(module_area: str) -> int:
    return db.cypher_query('MATCH (m:ModuleArea {name: \'' + module_area[0] + '\'})-[:FILLS]->(:ModuleCell)-[:IS_IN]->(s:Semester) RETURN s.number')


def get_obl_module_via_module_area(module_area: str) -> str:
    return db.cypher_query('MATCH (m:ModuleArea {name: \'' + module_area[0] + '\'})<-[:FILLS]-(n:Module) RETURN n.name')


def get_provided_comps_per_module(module: str) -> list[str]:
    return db.cypher_query('MATCH (m:Module {name: \'' + module + '\'})-[:PROVIDES]->(c:Competence) RETURN c.name')
