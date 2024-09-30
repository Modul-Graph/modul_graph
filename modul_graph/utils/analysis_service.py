from modul_graph.DTOs import PflichtmoduleDTO, WpfDTO, ModuleCompetenceDTO, CompetenceScDTO
from modul_graph.models.competence import Competence
from modul_graph.models.module import Module
from modul_graph.models.standard_curriculum import StandardCurriculum
from modul_graph.utils.analysis_DAO import da_get_semester_to_module_area_for_standard_curriculum


def get_competence_sc(sc: StandardCurriculum) -> CompetenceScDTO:
    """
    Get competence standard curriculum for standard curriculum
    :param sc: standard curriculum to get the competence standard curriculum for
    :return: competence standard curriculum
    """

    sem_ma = da_get_semester_to_module_area_for_standard_curriculum(sc)
    pflichtmodule: list[PflichtmoduleDTO] = []
    name_wpf: dict[str, WpfDTO] = {}

    for semester, module_areas in sem_ma.items():
        for module_area in module_areas:

            # Handle WPF part
            if module_area.is_wpf:
                modules: list[Module] = list(module_area.filled_by_module)

                if name_wpf.get(module_area.name) is None:
                    # initialize list of module competence dtos
                    module_competence_dtos: list[ModuleCompetenceDTO] = []
                    for module in modules:
                        competences: list[Competence] = list(module.provides_competence)
                        module_competence_dtos.append(
                            ModuleCompetenceDTO(name=module.name,
                                                competences=list(map(lambda x: x.name, competences)))

                        )

                    name_wpf[module_area.name] = WpfDTO(name=module_area.name, semesters={semester},
                                                        modules=module_competence_dtos)
                else:
                    name_wpf[module_area.name].semesters.add(semester)
            else:
                # Handle Pflichtmodule part
                module = list(module_area.filled_by_module)[0]
                competences = list(module.provides_competence)
                pflichtmodule.append(PflichtmoduleDTO(name=module.name, semester=semester,
                                                      competences=list(map(lambda x: x.name, competences))))

    return CompetenceScDTO(WPF=list(name_wpf.values()), pflichtmodule=pflichtmodule)
