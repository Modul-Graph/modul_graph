from neomodel import StructuredNode, OneOrMore, RelationshipTo, ZeroOrMore, IntegerProperty, One, RelationshipFrom


class Semester(StructuredNode):
    number = IntegerProperty(required=True, unique=True)

    # connection to CpCluster
    consists_of_cp_cluster = RelationshipTo('modul_graph.models.cp_cluster.CpCluster', 'CONSISTS_OF', ZeroOrMore)

    # connection to ModuleCell
    contains_module_cell = RelationshipFrom('modul_graph.models.module_cell.ModuleCell', 'IS_IN', OneOrMore)

    # connection to StudyExamRules
    specified_by_SER = RelationshipFrom('modul_graph.models.study_exam_rules.StudyExamRules', 'SPECIFIES', One)