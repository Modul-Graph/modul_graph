from neomodel import StructuredNode, StringProperty, OneOrMore, RelationshipTo, ZeroOrMore, IntegerProperty, One, RelationshipFrom


class StudyExamRules(StructuredNode):
    name = StringProperty(required=True, unique=True)

    # connection to Module
    has_module = RelationshipFrom('modul_graph.models.module.Module', 'BELONGS_TO', cardinality=OneOrMore)

    # connection to Semester
    specifies_semester = RelationshipTo('modul_graph.models.semester.Semester', 'SPECIFIES', cardinality=OneOrMore)