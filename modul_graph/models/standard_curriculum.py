from neomodel import StructuredNode, StringProperty, ZeroOrMore, RelationshipTo, RelationshipFrom, \
    BooleanProperty  # type: ignore


class StandardCurriculum(StructuredNode):
    """
    Neomodel class representing a standard curriculum
    """
    name = StringProperty(required=True, unique=True)
    start_winter = BooleanProperty()

    # connection to Module
    has_module = RelationshipFrom('modul_graph.models.module.Module', 'BELONGS_TO', cardinality=ZeroOrMore)

    # connection to Semester
    specifies_semester = RelationshipTo('modul_graph.models.semester.Semester', 'SPECIFIES', cardinality=ZeroOrMore)
