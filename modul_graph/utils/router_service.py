from fastapi import HTTPException
from modul_graph.DTOs import ModuleDTO
from neomodel import db
from ast import literal_eval

from modul_graph.utils.analysis_DAO import da_get_provided_comps_per_module, da_get_needed_comps_for_module, \
    da_get_module_areas_for_module
from .std_curr import std_curr

"""
This service is at the moment only responsible for 'Module' information.
Since it's not a lot, it hasn't been separated into service, DAO and repo.
"""


class RouterService:

    def get_module(self, mod_name: str) -> ModuleDTO:
        result = db.cypher_query(
            'MATCH (m:Module {name:\'' + mod_name + '\'}) RETURN m.name, m.description, m.is_in_summer, m.is_in_winter, m.cp_plus_description')[
            0][0]
        if not result:
            raise HTTPException(status_code=404, detail='Module not found')
        provided_comps: list[str] = da_get_provided_comps_per_module(mod_name)
        needed_comps: list[str] = da_get_needed_comps_for_module(mod_name)
        ret: ModuleDTO = ModuleDTO(name=result[0], description=result[1], cp_plus_description=literal_eval(result[4]),
                                   winter=result[3], summer=result[2], needs_competences=needed_comps,
                                   provides_competences=provided_comps,
                                   # the last two aren't actually important here, but they are required attributes of ModuleDTO
                                   std_curr_name=std_curr.name, module_areas=da_get_module_areas_for_module(mod_name))
        return ret

    def create_module(self, mod: ModuleDTO) -> None:
        try:
            # if exception is thrown, module name is not yet used - good!
            self.__does_mod_exist(mod.name)
        except HTTPException:
            # if this statement is reached, the new module can be created because no other module with its name exists
            # todo: write to DB
            # ...
            pass
        raise HTTPException(status_code=422, detail='Module cannot be created, likely because the name already exists.')

    def delete_module(self, mod_name: str) -> None:
        self.__does_mod_exist(mod_name)
        db.cypher_query('MATCH (m:Module {name:\'' + mod_name + '\'}) DETACH DELETE m')

    def update_module(self, mod: ModuleDTO) -> None:
        self.__does_mod_exist(mod.name)
        # todo: write to DB
        # ...

    def __does_mod_exist(self, mod_name: str) -> None:
        result = db.cypher_query('MATCH (m:Module {name:\'' + mod_name + '\'}) RETURN m')[0][0][0]
        if not result:
            raise HTTPException(status_code=404, detail='Module not found')

