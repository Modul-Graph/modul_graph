import math

from fastapi import APIRouter, HTTPException
from loguru import logger

from modul_graph.DTOs import AnalysisResponseDTO, AnalysisStatus, SuggestionRequestDTO, GraphDisplayResponseDTO, \
    GraphDisplayResponseNodeDTO, GraphDisplayResponseEdgeDTO
from modul_graph.experiments.pygad_suggestions import Suggestion
from modul_graph.i18n import _
from modul_graph.models.competence import Competence
from modul_graph.models.module import Module
from modul_graph.models.standard_curriculum import StandardCurriculum

router = APIRouter(prefix="/analysis")


@router.get("/doability/{sc}")
def get_doability(sc: str) -> AnalysisResponseDTO:
    """
    Return do
    :param sc: Standard curriculum to get the doability for
    :raises HTTPException 400: if standard curriculum doesn't exist
    :return: analysis result
    """

    try:
        sc_d: StandardCurriculum = StandardCurriculum.nodes.first_or_none(name=sc)

        if sc is None:
            raise ValueError("Standard curriculum does not exist")

        suggestions, score = Suggestion(sc_d, set()).gen_suggestion()

        is_ok = score > -math.inf

    except ValueError:
        raise HTTPException(400, "standard curriculum doesn't exist")

    res: AnalysisResponseDTO
    if is_ok:
        res = AnalysisResponseDTO(status=AnalysisStatus.success, message=_("Doability success message"))

    else:
        res = AnalysisResponseDTO(status=AnalysisStatus.error, message=_("Doability error message"))

    return res


@router.post("/suggestion")
def get_curriculum_suggestion(
    req: SuggestionRequestDTO) -> GraphDisplayResponseDTO:
    """
    Get a suggestion for a standard curriculum
    :param req: request DTO
    :return: analysis result
    """

    logger.info(f"{req}")

    # suggestions = get_example_graph(wanted_competence=req.competences[0].name, standard_curriculum=req.standard_curriculum.name)

    nodes: set[GraphDisplayResponseNodeDTO] = set()
    edges: set[GraphDisplayResponseEdgeDTO] = set()

    suggestions, score = Suggestion(req.standard_curriculum, set(req.competences)).gen_suggestion()

    # sort suggestions by semester
    suggestions = sorted(suggestions, key=lambda x: x[1].number)

    # Map each Competence to the module which provided it the most recent
    competences_to_modules: dict[str, set[Module]] = {}

    # competences should only be added to the dict if they happened in a past semester -> we store the competence -> module mapping here
    current_semester_num = -1
    current_semester_module_competences: list[tuple[Module, Competence]] = []

    for _, semester, module in suggestions:

        # if semester progressed, add all competences provided by modules in the current semester to the dict,
        # reset the list and update the current semester
        if current_semester_num < semester.number:
            # Add edges for all competences provided by modules in current semester
            for _module, _competence in current_semester_module_competences:
                competences_to_modules[_competence.name] = set()
                competences_to_modules[_competence.name].add(_module)

            current_semester_module_competences = []
            current_semester_num = semester.number

        # Add module as node
        nodes.add(GraphDisplayResponseNodeDTO(id=module.name, label=module.name, semester=semester.number))

        required_competences: set[Competence] = set(module.needs_competence.all())
        provided_competences: set[Competence] = set(module.provides_competence.all())

        for required_competence in required_competences:

            # if required competence is not in the dict, it wasn't provided by any module yet. Skip it...
            if required_competence.name not in competences_to_modules:
                continue

            # If requird competence was provided by a module previously, add an edge from the providing module to the current module
            else:
                for _module in competences_to_modules[required_competence.name]:
                    edges.add(GraphDisplayResponseEdgeDTO(source=_module.name, target=module.name,
                                                          id=f"{module.name}-{module.name}"))
        for provided_competence in provided_competences:
            current_semester_module_competences.append((module, provided_competence))

    # for suggestion in suggestions:
    #     for semester in suggestion[2]:
    #         nodes.add(SuggestionResponseNodeDTO(id=suggestion[0], label=suggestion[0], semester=semester))
    #
    #         for requirement in suggestion[3]:
    #             # Quirk: Sometimes we get an empty ('') requirement. That's a bug and we need to ignore that
    #             if not requirement:
    #                 continue

    return GraphDisplayResponseDTO(nodes=nodes, edges=edges)
