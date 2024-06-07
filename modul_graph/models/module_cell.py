from neomodel import StructuredNode, StringProperty, RelationshipTo, ZeroOrMore, OneOrMore, One, RelationshipFrom

from models.cp_cluster import CpCluster
from models.module_area import ModuleArea
from models.semester import Semester


class ModuleCell(StructuredNode):
    identifier = StringProperty(required=True, unique=True)

    # connection to ModuleArea
    filled_by_module_area = RelationshipFrom(ModuleArea, 'FILLS', cardinality=OneOrMore)

    # connection to Semester
    is_in_semester = RelationshipTo(Semester, 'IS_IN', cardinality=One)

    # connection to CpCluster
    is_component_of_cp_cluster = RelationshipFrom(CpCluster, 'CONSISTS_OF', cardinality=ZeroOrMore)