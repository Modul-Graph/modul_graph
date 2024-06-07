from neomodel import (StructuredNode, StringProperty, IntegerProperty, RelationshipTo, RelationshipFrom, ZeroOrMore, OneOrMore)


class MicroUnit(StructuredNode):
    name = StringProperty(required=True, unique_index=True)
    level = IntegerProperty(required=True)

    # connection to Module
    needs_from_module = RelationshipFrom('Module', 'NEEDS', cardinality=ZeroOrMore)
    provide_to_module = RelationshipTo('Module', 'PROVIDES', cardinality=OneOrMore)
