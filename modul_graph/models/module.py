from neomodel import JSONProperty, StructuredNode, StringProperty, RelationshipTo, ZeroOrMore, OneOrMore, \
    RelationshipFrom, BooleanProperty


class Module(StructuredNode):
    """
    A module is a concrete module that students can visit
    """

    name = StringProperty(required=True, unique=True)
    """
    Human readable name of the module
    """

    module_description = StringProperty()
    """
    Human readable description of the module
    """

    cp_plus_description = JSONProperty()
    """
    A dictionary of CP as key and a description of how to gain the amount of CP as value.
    Some modules have multiple possible CP constellations depending on certain things. 
    """

    is_in_summer = BooleanProperty(required=True)
    """
    Indicates that the module is available in the summer semester
    """

    is_in_winter = BooleanProperty(required=True)
    """
    Indicates that the module is available in the winter semester
    """

    # connection to Competence
    needs_competence = RelationshipTo('Competence', 'NEEDS', cardinality=ZeroOrMore)
    """
    Connection to competence node which is required by this module. Might be multiple connections
    """

    provided_by_competence = RelationshipFrom('Competence', 'PROVIDES', cardinality=OneOrMore)
    """
    Connection to competence which is provided by the module
    """


    # connection to MicroUnit
    needs_micro_unit = RelationshipTo('MicroUnit', 'NEEDS', cardinality=ZeroOrMore)
    provided_by_micro_unit = RelationshipFrom('MicroUnit', 'PROVIDES', cardinality=ZeroOrMore)

    # connection to StudyExamRules
    belongs_to_SER = RelationshipTo('StudyExamRules', 'BELONGS_TO', cardinality=OneOrMore)
    """
    Connection indicates in which SERs the module can be visited
    """

    # connection to ModuleArea
    fills_module_area = RelationshipTo('ModuleArea', 'FILLS', cardinality=OneOrMore)
    """
    Connection to module are if module can be visited as an elected subject
    """