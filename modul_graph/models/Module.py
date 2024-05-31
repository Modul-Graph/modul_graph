from neomodel import JSONProperty, StructuredNode, StringProperty, RelationshipTo, ZeroOrMore, OneOrMore, IntegerProperty, One, RelationshipFrom


class Module(StructuredNode):

    # attributes
    name = StringProperty()
    moduleDescription = StringProperty()
    cpPlusDescription = JSONProperty()

    # connection to Competence
    needs_competence = RelationshipTo('Competence', 'NEEDS', cardinality=ZeroOrMore)
    provided_by_competence = RelationshipFrom('Competence', 'PROVIDES', cardinality=OneOrMore)

    # connection to MicroUnit
    needs_micro_unit = RelationshipTo('MicroUnit', 'NEEDS', cardinality=ZeroOrMore)
    provided_by_micro_unit = RelationshipFrom('MicroUnit', 'PROVIDES', cardinality=ZeroOrMore)

    # connection to StudyExamRules

    # connection to ModuleArea