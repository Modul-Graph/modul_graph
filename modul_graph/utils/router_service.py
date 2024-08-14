from fastapi import HTTPException

from models.competence import Competence
from models.micro_unit import MicroUnit
from models.module import Module
from models.module_area import ModuleArea
from models.standard_curriculum import StandardCurriculum
from modul_graph.DTOs import ModuleDTO
from neomodel import db # type: ignore
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
        self.__does_mod_exist__exists_already_exception(mod.name)
        self.__create_or_update_mod(Module(), mod)

    def delete_module(self, mod_name: str) -> None:
        self.__does_mod_exist__not_found_exception(mod_name)
        db.cypher_query('MATCH (m:Module {name:\'' + mod_name + '\'}) DETACH DELETE m')

    def update_module(self, identifier: str, mod_new: ModuleDTO) -> None:
        # the old name/identifier has to exist
        self.__does_mod_exist__not_found_exception(identifier)
        # the new name should not yet exist if it's different from the old one
        if identifier != mod_new.name:
            self.__does_mod_exist__exists_already_exception(mod_new.name)
        self.__create_or_update_mod(Module.nodes.get(name=identifier), mod_new)

    def __does_mod_exist(self, mod_name: str) -> bool:
        result = db.cypher_query('MATCH (m:Module {name:\'' + mod_name + '\'}) RETURN m')[0][0][0]
        return result

    def __does_mod_exist__not_found_exception(self, mod_name: str) -> None:
        if not self.__does_mod_exist(mod_name):
            raise HTTPException(status_code=404, detail='Module not found')

    def __does_mod_exist__exists_already_exception(self, mod_name: str) -> None:
        if self.__does_mod_exist(mod_name):
            raise HTTPException(status_code=422, detail='The chosen module name exists already.')

    def __create_or_update_mod(self, mod_db: Module, mod_new: ModuleDTO) -> None:
        mod_db.name = mod_new.name
        mod_db.description = mod_new.description
        mod_db.cp_plus_description = mod_new.cp_plus_description
        mod_db.summer = mod_new.summer
        mod_db.winter = mod_new.winter

        # disconnect std_curr
        for elem in mod_db.belongs_to_standard_curriculum:
            mod_db.belongs_to_standard_curriculum.disconnect(elem)
        # disconnect mod areas
        for elem in mod_db.fills_module_area:
            mod_db.fills_module_area.disconnect(elem)
        # disconnect needed comps
        for elem in mod_db.needs_competence:
            mod_db.needs_competence.disconnect(elem)
        # disconnect provided comps
        for elem in mod_db.provides_competence:
            mod_db.provides_competence.disconnect(elem)
        # disconnect needed micro units
        for elem in mod_db.needs_micro_unit:
            mod_db.needs_micro_unit.disconnect(elem)
        # disconnect provided micro units
        for elem in mod_db.provided_by_micro_unit:
            mod_db.provided_by_micro_unit.disconnect(elem)

        # connect std_curr
        for elem in mod_new.std_curr_name:
            node = StandardCurriculum.nodes.get(name=elem)
            mod_db.belongs_to_standard_curriculum.connect(node)
        # connect mod areas
        for elem in mod_new.module_areas:
            node = ModuleArea.nodes.get(name=elem)
            mod_db.fills_module_area.connect(node)
        # connect needed comps
        for elem in mod_new.needs_competences:
            node = Competence.nodes.get(name=elem)
            mod_db.needs_competence.connect(node)
        # connect provided comps
        for elem in mod_new.provides_competences:
            node = Competence.nodes.get(name=elem)
            mod_db.provides_competence.connect(node)
        # connect needed micro units
        for elem in mod_new.needs_micro_units:
            node = MicroUnit.nodes.get(name=elem)
            mod_db.needs_micro_unit.connect(node)
        # connect provided micro units
        for elem in mod_new.provides_micro_units:
            node = MicroUnit.nodes.get(name=elem)
            mod_db.provided_by_micro_unit.connect(node)

        mod_db.save()

        # todo: mit Postman testen


