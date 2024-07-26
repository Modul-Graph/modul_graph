from fastapi import HTTPException
from modul_graph.DTOs import ModuleDTO
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

    def create_module(self, mod: ModuleDTO) -> None:
        # todo: write to DB
        # ...
        raise HTTPException(status_code=422, detail='Module cannot be created, likely because the name already exists.')

    def delete_module(self, mod_name: str) -> None:
        self.__does_mod_exist(mod_name)
        # todo: write to DB
        # ...

    def update_module(self, mod: ModuleDTO) -> None:
        self.__does_mod_exist(mod.name)
        # todo: write to DB
        # ...

    def __get_from_db(self, mod_name) -> ModuleDTO:   # name, cp_plus_description, description, summer, winter, provided & needed comps
        result = db.cypher_query('MATCH (m:Module {name:\'' + mod_name + '\'}) RETURN m')[0][0][0]
        if not result:
            raise HTTPException(status_code=404, detail='Module not found')
        # todo: make moduleDto out of result properties
        # ...
        return result

    def __does_mod_exist(self, mod_name: str) -> None:
        result = db.cypher_query('MATCH (m:Module {name:\'' + mod_name + '\'}) RETURN m')[0][0][0]
        if not result:
            raise HTTPException(status_code=404, detail='Module not found')

