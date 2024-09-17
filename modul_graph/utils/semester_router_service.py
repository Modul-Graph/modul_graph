from modul_graph.models.standard_curriculum import StandardCurriculum
from modul_graph.models.semester import Semester
from fastapi import HTTPException
from neomodel import db, DoesNotExist  # type: ignore


class SemesterRouterService:

    @db.transaction
    def create_semester(self, number: int) -> None:
        try:
            Semester.nodes.get(number=number)
        except DoesNotExist:
            sem: Semester = Semester(number=number)
            sem.save()
            sem.specified_by_standard_curriculum.connect(StandardCurriculum.nodes[0])
            return
        raise HTTPException(status_code=409, detail=f'A semester with the number {number} already exists')

    def delete_semester(self, number: int) -> None:
        sem: Semester = Semester.nodes.get(number=number)
        if not sem:
            raise HTTPException(status_code=404, detail=f'Semester {number} not found')
        sem.delete()

