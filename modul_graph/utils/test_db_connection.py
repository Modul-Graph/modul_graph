from neomodel import db
# Funktionen in __main__.py schreiben (nach Dateneintrag in DB)
# console: python -m modul_graph


def test_db_connection() -> bool:
    result, meta = db.cypher_query('MATCH p=(:Module)-[r:PROVIDES]->(:Competence) RETURN p', resolve_objects=True)
    if len(result) > 1:
        return False
    return True