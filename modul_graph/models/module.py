from neomodel import JSONProperty, StructuredNode, StringProperty, RelationshipTo, ZeroOrMore, OneOrMore, RelationshipFrom, BooleanProperty

from models.competence import Competence
from models.micro_unit import MicroUnit
from models.module_area import ModuleArea
from models.study_exam_rules import StudyExamRules


class Module(StructuredNode):
    name = StringProperty(required=True, unique=True)
    module_description = StringProperty()
    cp_plus_description = JSONProperty()
    is_in_summer = BooleanProperty(required=True)
    is_in_winter = BooleanProperty(required=True)

    # connection to Competence
    needs_competence = RelationshipTo(Competence, 'NEEDS', cardinality=ZeroOrMore)
    provided_by_competence = RelationshipFrom(Competence, 'PROVIDES', cardinality=OneOrMore)

    # connection to MicroUnit
    needs_micro_unit = RelationshipTo(MicroUnit, 'NEEDS', cardinality=ZeroOrMore)
    provided_by_micro_unit = RelationshipFrom(MicroUnit, 'PROVIDES', cardinality=ZeroOrMore)

    # connection to StudyExamRules
    belongs_to_SER = RelationshipTo(StudyExamRules, 'BELONGS_TO', cardinality=OneOrMore)

    # connection to ModuleArea
    fills_module_area = RelationshipTo(ModuleArea, 'FILLS', cardinality=OneOrMore)