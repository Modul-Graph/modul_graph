from neomodel import StructuredNode, OneOrMore, RelationshipTo, ZeroOrMore, IntegerProperty, One, RelationshipFrom

from .cp_cluster import CpCluster
from .module_cell import ModuleCell
from .study_exam_rules import StudyExamRules


class Semester(StructuredNode):
    number = IntegerProperty(required=True, unique=True)

    # connection to CpCluster
    consists_of_cp_cluster = RelationshipTo(CpCluster, 'CONSISTS_OF', ZeroOrMore)

    # connection to ModuleCell
    contains_module_cell = RelationshipFrom(ModuleCell, 'IS_IN', OneOrMore)

    # connection to StudyExamRules
    specified_by_SER = RelationshipFrom(StudyExamRules, 'SPECIFIES', One)