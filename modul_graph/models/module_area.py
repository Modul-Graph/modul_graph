from neomodel import StructuredNode, OneOrMore, StringProperty, RelationshipTo, RelationshipFrom


class ModuleArea(StructuredNode):
    """
    Module ares are used to depict elective subjects they can be connected to a module cell to indicate that this
    module cell is an elective subject
    """

    name = StringProperty(required=True, unique=True)
    """
    Name of the module area e.g.: WPF Informatik (5CP)
    """

    # connection to Module
    filled_by_module = RelationshipFrom('Module', 'FILLS', cardinality=OneOrMore)
    """
    Connection to module(s) which can be visited to fulfill this module area
    """

    # connection to ModuleCell
    fills_module_cell = RelationshipTo('ModuleCell', 'FILLS', cardinality=OneOrMore)
    """
    Connection to module cell(s) in which it resides
    """