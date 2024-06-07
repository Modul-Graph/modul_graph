from neomodel import StructuredNode, OneOrMore, StringProperty, RelationshipTo, RelationshipFrom


class ModuleArea(StructuredNode):
    name = StringProperty(required=True, unique=True)

    # connection to Module
    filled_by_module = RelationshipFrom('Module', 'FILLS', cardinality=OneOrMore)

    # connection to ModuleCell
    fills_module_cell = RelationshipTo('ModuleCell', 'FILLS', cardinality=OneOrMore)