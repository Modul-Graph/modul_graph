from neomodel import StructuredNode, StringProperty, IntegerProperty, RelationshipTo, RelationshipFrom, ZeroOrMore, OneOrMore


class MicroUnit(StructuredNode):
    name = StringProperty(required=True, unique_index=True)
    level = IntegerProperty(required=True)
    assumes = RelationshipFrom('Module', 'ASSUMES', cardinality=ZeroOrMore)
    taughtBy = RelationshipTo('Module', 'TAUGHT BY', cardinality=OneOrMore)
