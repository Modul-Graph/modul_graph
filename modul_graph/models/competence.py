from neomodel import StructuredNode, StringProperty, RelationshipTo, ZeroOrMore, OneOrMore, IntegerProperty, One, RelationshipFrom
import unstructured_entry

class Competence(StructuredNode):
    """
    A competence is the binding unit for connecting modules
    """

    name = StringProperty(required=True, unique=True)
    """
    Human readable name of the competence
    """


    # connection to Module
    is_needed_by = RelationshipFrom('Module', 'NEEDS', cardinality=ZeroOrMore)
    """
    Connection to module which needs this competence
    """

    is_provided_by = RelationshipFrom('Module', 'PROVIDES', cardinality=OneOrMore)
    """
    Connection to model which provides this competence
    """
