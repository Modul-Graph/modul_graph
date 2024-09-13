from neomodel import (StructuredNode, StringProperty, IntegerProperty, RelationshipTo, RelationshipFrom, ZeroOrMore)  # type: ignore


class MicroUnit(StructuredNode):
    name = StringProperty(required=True, unique=True)
    level = IntegerProperty(required=True)

    # connection to Module
    needs_from_module = RelationshipFrom('modul_graph.models.module.Module', 'NEEDS', cardinality=ZeroOrMore)
    provide_to_module = RelationshipTo('modul_graph.models.module.Module', 'PROVIDES', cardinality=ZeroOrMore)
