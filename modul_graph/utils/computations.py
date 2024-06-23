from .cypher_queries import get_obl_module_via_module_area, get_semester_for_obl_module_via_module_area, get_module_areas_of_obligatory_modules, get_provided_comps_per_module


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



