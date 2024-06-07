from neomodel import (StructuredNode, StringProperty, IntegerProperty, RelationshipTo, RelationshipFrom, ZeroOrMore, OneOrMore)

from models.module import Module


class MicroUnit(StructuredNode):
    name = StringProperty(required=True, unique=True)
    level = IntegerProperty(required=True)

    # connection to Module
    needs_from_module = RelationshipFrom(Module, 'NEEDS', cardinality=ZeroOrMore)
    provide_to_module = RelationshipTo(Module, 'PROVIDES', cardinality=OneOrMore)
