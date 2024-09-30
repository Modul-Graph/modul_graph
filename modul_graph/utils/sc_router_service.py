from typing import List

from fastapi import HTTPException
from neomodel import db  # type: ignore

from modul_graph.models.semester import Semester
from modul_graph.models.standard_curriculum import StandardCurriculum


class ScRouterService:

    @db.transaction
    def update_semester_connections(self, sc: StandardCurriculum, semesters: List[int]) -> None:

        for sem in sc.specifies_semester.all():
            sc.specifies_semester.disconnect(sem)

        for sem in semesters:
            sem_node = Semester.nodes.get(number=sem)
            if not sem_node:
                raise HTTPException(status_code=404, detail="Semester not found")
            sc.specifies_semester.connect(sem_node)

        sc.save()
