from neomodel import StructuredNode, StringProperty, RelationshipTo, IntegerProperty, RelationshipFrom , ZeroOrMore  # type: ignore


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

    cp_number_grade = IntegerProperty()

    # connection to ModuleCell
    # should be TwoOrMore but that doesn't exist
    consists_of_module_cell = RelationshipTo('modul_graph.models.module_cell.ModuleCell', 'CONSISTS_OF',
                                             cardinality=ZeroOrMore)
    """
    Connection to ModuleCell
    """

    # connection to Semester
    is_component_of_semester = RelationshipFrom('modul_graph.models.semester.Semester', 'CONSISTS_OF',
                                                cardinality=ZeroOrMore)
    """
    Connection to a semester
    """

    def __hash__(self):
        return hash(self.identifier)

    def __eq__(self, other):
        if not isinstance(other, CpCluster):
            return False
        else:
            return self.identifier == other.identifier
