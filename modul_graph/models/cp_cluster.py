from neomodel import RelationshipManager, StructuredNode, OneOrMore, StringProperty, RelationshipTo, IntegerProperty, \
    RelationshipFrom

from .module_cell import ModuleCell
from .semester import Semester


class CpCluster(StructuredNode):
    """
    CP Cluster is a node connecting semester and module cells.

    A CP Cluster might span multiple semesters and thus might be connected to multiple semesters
    In order to successfully "finish" a CP Cluster all connected module cells must be finished and enough module cells
    must be finished with a grade (not a "schein") to fulfill the cp_number requirement
    """
    identifier = StringProperty(required=True, unique=True)
    """
    Unique identifier. Used for internal purposes
    """

    cp_number = IntegerProperty()
    """
    Minimum Number of CPs to write with a grade
    """

    cp_number_grade = IntegerProperty

    # connection to ModuleCell
    # should be TwoOrMore but that doesn't exist
    consists_of_module_cell = RelationshipTo(ModuleCell, 'CONSISTS_OF', cardinality=OneOrMore)
    """
    Connection to ModuleCell
    """

    # connection to Semester
    is_component_of_semester = RelationshipFrom(Semester, 'CONSISTS_OF', cardinality=OneOrMore)
    """
    Connection to a semester
    """
