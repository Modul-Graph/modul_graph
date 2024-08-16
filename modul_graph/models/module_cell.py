from neomodel import StructuredNode, StringProperty, RelationshipTo, ZeroOrMore, OneOrMore, One, RelationshipFrom # type: ignore


class ModuleCell(StructuredNode):
    """
    The module cell is the binding node between a CP Cluster and a module area. It describes a single entry
    inside a standard curriculum and always resides in a specific semester
    """

    identifier = StringProperty(required=True, unique=True)
    """
    Unique identifier used for internal purposes
    """

    # connection to ModuleArea
    filled_by_module_area = RelationshipFrom('modul_graph.models.module_area.ModuleArea', 'FILLS', cardinality=OneOrMore)
    """
    Connection to the module area which resides in the module cell. This is the content of the module cell. In terms 
    of the standard curriculum it would be "WPF Informatik" or "Mathe I" 
    """

    # connection to Semester
    is_in_semester = RelationshipTo('modul_graph.models.semester.Semester', 'IS_IN', cardinality=One)
    """
    Connection to the semester in which the module cell resides
    """

    # connection to CpCluster
    is_component_of_cp_cluster = RelationshipFrom('modul_graph.models.cp_cluster.CpCluster', 'CONSISTS_OF', cardinality=ZeroOrMore)
    """
    Connection to the CP Cluster where the module cell is part of
    """
