from neomodel import StructuredNode, OneOrMore, RelationshipTo, ZeroOrMore, IntegerProperty, One, RelationshipFrom # type: ignore


class Semester(StructuredNode):
    number = IntegerProperty(required=True, unique=True)

    # connection to CpCluster
    consists_of_cp_cluster = RelationshipTo('modul_graph.models.cp_cluster.CpCluster', 'CONSISTS_OF', ZeroOrMore)

    # connection to ModuleCell
    contains_module_cell = RelationshipFrom('modul_graph.models.module_cell.ModuleCell', 'IS_IN', OneOrMore)

    # connection to StandardCurriculum
    specified_by_standard_curriculum = RelationshipFrom('modul_graph.models.standard_curriculum.StandardCurriculum', 'SPECIFIES', One)

    def __hash__(self):
        return hash(self.number)