from neomodel import RelationshipManager, StructuredNode, OneOrMore, StringProperty, RelationshipTo, IntegerProperty, RelationshipFrom


class TwoOrMore (RelationshipManager):
    """
    A relationship to two or more nodes
    todo: implement
    """
    pass

class CpCluster(StructuredNode):
    identifier = StringProperty(required=True, unique_index=True)
    cp_number = IntegerProperty()
    cp_number_grade = IntegerProperty

    # connection to ModuleCell
    consists_of_module_cell = RelationshipTo('ModuleCell', 'CONSISTS_OF', cardinality=TwoOrMore)

    # connection to Semester
    is_component_of_semester = RelationshipFrom('Semester', 'CONSISTS_OF', cardinality=OneOrMore)