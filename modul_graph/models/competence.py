from neomodel import StructuredNode, StringProperty, RelationshipTo, ZeroOrMore, OneOrMore, IntegerProperty, One, RelationshipFrom

from models.module import Module


class Competence(StructuredNode):
    name = StringProperty(required=True, unique=True)

    # connection to Module
    is_needed_by = RelationshipFrom(Module, 'NEEDS', cardinality=ZeroOrMore)
    is_provided_by = RelationshipTo(Module, 'PROVIDES', cardinality=OneOrMore)
