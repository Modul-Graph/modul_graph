from neomodel import StructuredNode, ZeroOrMore, StringProperty, RelationshipTo, RelationshipFrom, IntegerProperty  # type: ignore


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
    filled_by_module = RelationshipFrom('modul_graph.models.module.Module', 'FILLS', cardinality=ZeroOrMore)
    """
    Connection to module(s) which can be visited to fulfill this module area
    """

    # connection to ModuleCell
    fills_module_cell = RelationshipTo('modul_graph.models.module_cell.ModuleCell', 'FILLS', cardinality=ZeroOrMore)
    """
    Connection to module cell(s) in which it resides
    """

    cp = IntegerProperty(required=False)
    """
    Credit points of the module area. Is only set if the module area is a WPF!
    """

    # noinspection PyTypeChecker
    @property
    def is_wpf(self) -> bool:
        return len(self.filled_by_module) > 1

    def __hash__(self):
        return hash(self.name)
