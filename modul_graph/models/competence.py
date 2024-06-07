from neomodel import StructuredNode, StringProperty, RelationshipTo, ZeroOrMore, OneOrMore, IntegerProperty, One, RelationshipFrom
import unstructured_entry

class Competence(StructuredNode):
    #attribute
    name = StringProperty(required=True, unique=True)
    #relationships
    is_needed_by = RelationshipFrom('Module', 'NEEDS', cardinality=ZeroOrMore)
    is_provided_by = RelationshipTo('Module', 'PROVIDES', cardinality=OneOrMore)
