from neomodel import StructuredNode, StringProperty, RelationshipTo, ZeroOrMore, IntegerProperty, One, RelationshipFrom


class Competence(StructuredNode):
    name = StringProperty(required=True, unique_index=True)
    is_part_of = RelationshipTo('Competence', 'IS_PART_OF', cardinality=ZeroOrMore)
# lalala

class Requirement(StructuredNode):
    semester = IntegerProperty(required=True)
    name = StringProperty(required=True)


class Module(StructuredNode):
    name = StringProperty(required=True, unique_index=True)
    needs = RelationshipTo(Competence, 'NEEDS')
    provides = RelationshipTo(Competence, 'PROVIDES')
    fulfills = RelationshipTo(Requirement, 'FULFILLS', cardinality=ZeroOrMore)
    requires = RelationshipFrom(Requirement, 'REQUIRES')
