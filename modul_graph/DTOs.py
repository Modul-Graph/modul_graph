"""
All DTOs needed for the REST-API are defined here.
"""
from enum import Enum
from typing import Optional
from typing import Self, Set

from pydantic import BaseModel, field_validator, ConfigDict, PositiveInt

from modul_graph.models.competence import Competence
from modul_graph.models.module import Module
from modul_graph.models.standard_curriculum import StandardCurriculum

"""
Module DTOs
"""


class ModuleDTO(BaseModel):
    name: str
    description: Optional[str] = None
    cp_plus_description: dict[str, int]
    summer: bool
    winter: bool

    # connections:
    std_curr_names: Optional[list[str]] = None
    module_areas: Optional[list[str]] = None
    needs_competences: Optional[list[str]] = None
    provides_competences: Optional[list[str]] = None
    needs_micro_units: Optional[list[str]] = None
    provides_micro_units: Optional[list[str]] = None


class ModuleAreaDTO(BaseModel):
    name: str
    filled_by_module: list[str]
    cp: Optional[int] = None


"""
Standard Curriculum DTOs
"""


class StandardCurriculumDTO(BaseModel):
    """
    Intermediate transfer object used in the REST-API endpoints
    """
    name: str
    start_winter: bool

    def get_node(self) -> StandardCurriculum | None:
        """
        Convert DTO to a StandardCurriculum node
        :return: the constructed node or None if node doesn't exist
        """
        return StandardCurriculum.get.get_or_none(name=self.name)


"""
Analysis DTOs
"""


class AnalysisStatus(str, Enum):
    """
    Enum for status string constraints
    """
    success = "success"
    info = "info"
    error = "error"
    warning = "warning"


class AnalysisResponseDTO(BaseModel):
    """
    Generic analysis response class. Other analysis respond classes might inherit this class
    """
    status: AnalysisStatus
    message: str


"""
Suggestion DTOs
"""


class SuggestionRequestDTO(BaseModel):
    """
    Request DTO for the suggestion endpoint
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True  # Set tpo true to allow Neomodel Node classes
    )

    standard_curriculum: StandardCurriculum

    competences: list[Competence]

    @field_validator("standard_curriculum", mode="before")
    @classmethod
    def standard_curriculum_must_exist_in_db(cls, value: str) -> StandardCurriculum:
        """
        Checks if the given standard curriculum exists in the database
        :param value: the standard curriculum name
        :return: the value if it exists in the database
        """

        if not isinstance(value, str):
            raise ValueError("Standard curriculum must be a string")

        sc = StandardCurriculum.nodes.get_or_none(name=value)
        if not StandardCurriculum.nodes.get_or_none(name=value):
            raise ValueError(f"Standard curriculum {value} does not exist in the database")

        return sc

    @field_validator("competences", mode="before")
    @classmethod
    def competences_must_exist_in_db(cls, value: list[str]) -> list[Competence]:
        """
        Checks if the given competences exist in the database
        :param value: the competences
        :return: the value if it exists in the database
        """

        not_existing_competences: list[str] = []
        existing_competences: list[Competence] = []
        for idx, competence in enumerate(value):

            if not isinstance(competence, str):
                raise ValueError(
                    f"Competences must be a list of strings! Got a non-string value at index {idx}: {competence}")

            c: Competence | None = Competence.nodes.get_or_none(name=competence)
            if c is None:
                not_existing_competences.append(competence)
            else:
                existing_competences.append(c)

        if not_existing_competences:
            raise ValueError(f"Competences {not_existing_competences} do not exist in the database")

        return existing_competences


class GraphDisplayResponseEdgeDTO(BaseModel):
    """
    Specifies the edge between two nodes/module in the suggestion graph
    """
    source: str
    target: str
    id: str

    def __hash__(self):
        return hash(self.id)


class GraphDisplayResponseNodeDTO(BaseModel):
    """
    Specifies nodes/modules in the suggestion response graph
    """
    id: str
    label: str
    semester: int

    @classmethod
    def from_module(cls, module: Module) -> Self:
        """
        Cast Module to SuggestionResponseNodeDTO
        :param module: the module to cast
        :return: the constructed DTO
        """
        return cls(id=module.element_id, label=module.name, semester=module.semester)

    def __hash__(self):
        return hash(self.id)


class GraphDisplayResponseDTO(BaseModel):
    """
    Wrapper class for the suggestion response
    """
    nodes: set[GraphDisplayResponseNodeDTO]
    edges: set[GraphDisplayResponseEdgeDTO]

    @classmethod
    def from_edge_list(cls, edge_list: list[tuple[GraphDisplayResponseNodeDTO, GraphDisplayResponseNodeDTO]]) -> Self:
        """
        Construct Suggestion Response DTO from edge list
        :param edge_list: edge list to construct the DTO from
        :return: the constructed DTO
        """
        nodes: set[GraphDisplayResponseNodeDTO] = set()
        edges: set[GraphDisplayResponseEdgeDTO] = set()

        for edge in edge_list:
            source, target = edge
            nodes.add(source)
            nodes.add(target)
            edges.add(GraphDisplayResponseEdgeDTO(source=source.id, target=target.id, id=f"{source.id}-{target.id}"))

        return cls(nodes=nodes, edges=edges)


"""
Competence SC DTOs
"""


class ModuleCompetenceDTO(BaseModel):
    """
    Module Competence DTO
    """
    name: str
    competences: list[str]


class WpfDTO(BaseModel):
    """
    WPF DTO
    """
    name: str
    semesters: Set[PositiveInt]
    modules: list[ModuleCompetenceDTO]


class PflichtmoduleDTO(BaseModel):
    """
    Pflichtmodule DTO
    """
    name: str
    semester: PositiveInt
    competences: list[str]


class CompetenceScDTO(BaseModel):
    """
    Competence Standard Curriculum DTO
    """

    WPF: list[WpfDTO]
    pflichtmodule: list[PflichtmoduleDTO]


class RichCPClusterCell(BaseModel):
    """
    This is a cell containing one Module/WPF inside the CPCluster
    """
    cp: float
    sem: PositiveInt
    name: str
    isWPF: bool

    cellId: str
    """
    ID referencing module_cell
    """


class RichCPCluster(BaseModel):
    """
    SC CP-Cluster enriched with the Module-Areas/Pflichtmodules that sit in it
    """
    cells: list[RichCPClusterCell]
    cp_note: int

    cp_cluster_id: str
    """
    ID referencing cp_cluster
    """


class CellDTO(BaseModel):
    """
    Cell DTO
    """
    contains_wpf: bool

    data: ModuleDTO | ModuleAreaDTO
    """
    If contains_wpf is true, this is a ModuleAreaDTO, otherwise a ModuleDTO
    """

class UpdateCPClusterCellDTO(BaseModel):
    isWPF: bool
    name: str
    cp: PositiveInt
    sem: PositiveInt
    cellId: Optional[str] = None

class UpdateCPClusterDTO(BaseModel):
    cells: list[UpdateCPClusterCellDTO]
    cp_note: int

    clusterId: str
    """
    ID referencing cp_cluster
    """