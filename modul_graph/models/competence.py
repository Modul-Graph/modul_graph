from neomodel import StructuredNode, StringProperty, ZeroOrMore, RelationshipFrom # type: ignore


class Competence(StructuredNode):
    """
    A competence is the binding unit for connecting modules
    """

    name = StringProperty(required=True, unique=True)
    """
    Human readable name of the competence
    """

    # connection to Module
    is_needed_by = RelationshipFrom('modul_graph.models.module.Module', 'NEEDS', cardinality=ZeroOrMore)
    """
    Connection to module which needs this competence
    """

    is_provided_by = RelationshipFrom('modul_graph.models.module.Module', 'PROVIDES', cardinality=ZeroOrMore)
    """
    Connection to model which provides this competence
    """
