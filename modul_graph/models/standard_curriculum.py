from neomodel import StructuredNode, StringProperty, OneOrMore, RelationshipTo, RelationshipFrom, BooleanProperty  # type: ignore

from modul_graph.DTOs import StandardCurriculumDTO


class StandardCurriculum(StructuredNode):
    """
    Neomodel class representing a standard curriculum
    """
    name = StringProperty(required=True, unique=True)
    start_winter = BooleanProperty()

    # connection to Module
    has_module = RelationshipFrom('modul_graph.models.module.Module', 'BELONGS_TO', cardinality=OneOrMore)

    # connection to Semester
    specifies_semester = RelationshipTo('modul_graph.models.semester.Semester', 'SPECIFIES', cardinality=OneOrMore)

    @property
    def serialize(self) -> StandardCurriculumDTO:
        """
        Serialize instance to JSON encodable dictionary
        :return:
        """
        return StandardCurriculumDTO(name=self.name, start_winter=self.start_winter)
