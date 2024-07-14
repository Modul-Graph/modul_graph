from fastapi import HTTPException
from modul_graph.DTOs import ModuleDTO, AnalysisResponseDTO, ModuleRelationshipDTO
from neomodel import db
from ast import literal_eval

"""
This service is at the moment only responsible for 'Module' information.
Since it's not a lot, it hasn't been separated into service, DAO and repo.
"""


class RouterService:

    def get_module(self, mod_name: str) -> ModuleDTO:
        result = self.__get_from_db(mod_name)
        cp_plus_desc: dict[int, str] = literal_eval(result['cp_plus_description'])
        ret: ModuleDTO = ModuleDTO(name=result['name'], description=result['module_description'], cp_plus_description=cp_plus_desc, winter=result['is_in_winter'], summer=result['is_in_summer'])
        return ret

    def create_module(self, mod: ModuleDTO, mod_rels: ModuleRelationshipDTO) -> AnalysisResponseDTO:
        # 422
        pass

    def delete_module(self, mod_name: str) -> AnalysisResponseDTO:
        # assert that the module exists
        self.__get_from_db(mod_name)

    def update_module(self, mod: ModuleDTO, mod_rels: ModuleRelationshipDTO) -> AnalysisResponseDTO:
        # assert that the module exists
        self.__get_from_db(mod.name)

    def __get_from_db(self, mod_name):
        result = db.cypher_query('MATCH (m:Module {name:\'' + mod_name + '\'}) RETURN m')[0][0][0]
        if not result:
            raise HTTPException(status_code=404, detail='Module not found')
        return result