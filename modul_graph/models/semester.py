from neomodel import StructuredNode, OneOrMore, RelationshipTo, ZeroOrMore, IntegerProperty, One, RelationshipFrom


class Semester(StructuredNode):
    number = IntegerProperty(required=True, unique_index=True)

    # connection to CpCluster
    consists_of_cp_cluster = RelationshipTo('CpCluster', 'CONSISTS_OF', ZeroOrMore)

    # connection to ModuleCell
    contains_module_cell = RelationshipFrom('ModuleCell', 'IS_IN', OneOrMore)

    # connection to StudyExamRules
    specified_by_SER = RelationshipFrom('StudyExamRules', 'SPECIFIES', One)