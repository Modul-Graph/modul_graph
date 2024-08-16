from fastapi import HTTPException

from modul_graph.models.competence import Competence
from modul_graph.models.micro_unit import MicroUnit
from modul_graph.models.module import Module
from modul_graph.models.module_area import ModuleArea
from modul_graph.models.standard_curriculum import StandardCurriculum
from modul_graph.DTOs import ModuleDTO
from neomodel import db # type: ignore
from ast import literal_eval

from modul_graph.utils.analysis_DAO import da_get_provided_comps_per_module, da_get_needed_comps_for_module, \
    da_get_module_areas_for_module
from .std_curr import std_curr, instantiate_std_curr_obj

"""
This service is at the moment only responsible for 'Module' information.
Since it's not a lot, it hasn't been separated into service, DAO and repo.
"""


class RouterService:

    def get_module(self, mod_name: str) -> ModuleDTO:
        # result = db.cypher_query(
        #     'MATCH (m:Module {name:\'' + mod_name + '\'}) RETURN m.name, m.description, m.is_in_summer, m.is_in_winter, m.cp_plus_description')[
        #     0][0]
        # if not result:
        #     raise HTTPException(status_code=404, detail='Module not found')
        # instantiate_std_curr_obj(std_curr_name)
        # provided_comps: list[str] = da_get_provided_comps_per_module(mod_name)
        # needed_comps: list[str] = da_get_needed_comps_for_module(mod_name)
        # ret: ModuleDTO = ModuleDTO(name=result[0], description=result[1], cp_plus_description=literal_eval(result[4]),
        #                            winter=result[3], summer=result[2], needs_competences=needed_comps,
        #                            provides_competences=provided_comps,
        #                            # the last two aren't actually important here, but they are required attributes of ModuleDTO
        #                            std_curr_names=std_curr.name, module_areas=da_get_module_areas_for_module(mod_name))

        self.__does_mod_exist__not_found_exception(mod_name)
        ret_mod: Module = Module.nodes.get(name=mod_name)

        print(f'Module areas: {ret_mod.fills_module_area.all()}')
        print(f'Standard curricula: {ret_mod.belongs_to_standard_curriculum.all()}')

        ret_mod_dto: ModuleDTO = ModuleDTO(name=ret_mod.name,
                                           description=ret_mod.module_description,
                                           cp_plus_description=ret_mod.cp_plus_description,
                                           summer=ret_mod.is_in_summer,
                                           winter=ret_mod.is_in_winter,
                                           needs_competences=[x.name for x in ret_mod.needs_competence.all()],
                                           provides_competences=[x.name for x in ret_mod.provides_competence.all()],
                                           std_curr_names=[x.name for x in ret_mod.belongs_to_standard_curriculum.all()],
                                           module_areas=[x.name for x in ret_mod.fills_module_area.all()])

        return ret_mod_dto

    def create_module(self, mod: ModuleDTO) -> None:
        self.__does_mod_exist__exists_already_exception(mod.name)
        self.__create_or_update_mod(Module(), mod)

    def delete_module(self, mod_name: str) -> None:
        self.__does_mod_exist__not_found_exception(mod_name)
        db.cypher_query('MATCH (m:Module {name:\'' + mod_name + '\'}) DETACH DELETE m')
        if self.__does_mod_exist(mod_name):
            raise HTTPException(status_code=422, detail=f'Deletion of module `{mod_name}` failed')

    def update_module(self, identifier: str, mod_new: ModuleDTO) -> None:
        # the old name/identifier has to exist
        self.__does_mod_exist__not_found_exception(identifier)
        # the new name should not yet exist if it's different from the old one
        if identifier != mod_new.name:
            self.__does_mod_exist__exists_already_exception(mod_new.name)
        self.__create_or_update_mod(Module.nodes.get(name=identifier), mod_new)

    def __does_mod_exist(self, mod_name: str) -> bool:
        result = db.cypher_query('MATCH (m:Module {name:\'' + mod_name + '\'}) RETURN m')
        return result[0]

    def __does_mod_exist__not_found_exception(self, mod_name: str) -> None:
        if not self.__does_mod_exist(mod_name):
            raise HTTPException(status_code=404, detail='Module not found')

    def __does_mod_exist__exists_already_exception(self, mod_name: str) -> None:
        if self.__does_mod_exist(mod_name):
            raise HTTPException(status_code=422, detail='The chosen module name exists already.')

    @db.transaction
    def __create_or_update_mod(self, mod_db: Module, mod_new: ModuleDTO) -> None:
        mod_db.name = mod_new.name
        mod_db.description = mod_new.description
        mod_db.cp_plus_description = mod_new.cp_plus_description
        mod_db.is_in_summer = mod_new.summer
        mod_db.is_in_winter = mod_new.winter

        mod_db.save()

        # update required connections (sadly it's not possible to first disconnect the old ones ------------------------
        # and then connect the new ones because of AttemptedCardinalityViolation) --------------------------------------

        if not mod_new.std_curr_names:
            raise HTTPException(status_code=404, detail='No standard curricula specified')
        if not mod_new.module_areas:
            raise HTTPException(status_code=404, detail='No modules areas specified')

        # connect new standard curricula
        for elem in mod_new.std_curr_names:
            # if elem is a valid standard curriculum and is not already connected
            if elem in [x.name for x in StandardCurriculum.nodes.all()] and elem not in [x.name for x in mod_db.belongs_to_standard_curriculum.all()]:
                node = StandardCurriculum.nodes.get(name=elem)
                mod_db.belongs_to_standard_curriculum.connect(node)
            elif elem not in [x.name for x in StandardCurriculum.nodes.all()]:
                raise HTTPException(status_code=404, detail=f'Standard curriculum `{elem}` not found')

        # disconnect old standard curricula which are no longer used (disconnect everything in [old connections minus new connections])
        for elem in set([x.name for x in mod_db.belongs_to_standard_curriculum.all()]) - set(mod_new.std_curr_names):
            mod_db.belongs_to_standard_curriculum.disconnect(elem)

        # connect new module areas
        for elem in mod_new.module_areas:
            # if elem is a valid module area and is not already connected
            if elem in [x.name for x in ModuleArea.nodes.all()] and elem not in [x.name for x in mod_db.fills_module_area.all()]:
                node = ModuleArea.nodes.get(name=elem)
                mod_db.fills_module_area.connect(node)
            elif elem not in [x.name for x in ModuleArea.nodes.all()]:
                raise HTTPException(status_code=404, detail=f'Module area `{elem}` not found')

        # disconnect old module areas which are no longer used (disconnect everything in [old module areas minus new module areas])
        for elem in set([x.name for x in mod_db.fills_module_area.all()]) - set(mod_new.module_areas):
            mod_db.fills_module_area.disconnect(elem)

        '''
        # connect std_curr (required connection)
        if not mod_new.std_curr_names:
            raise HTTPException(status_code=404, detail='No standard curricula specified')
        else:
            for elem in mod_new.std_curr_names:
                if elem in [x.name for x in StandardCurriculum.nodes.all()]:
                    node = StandardCurriculum.nodes.get(name=elem)
                    mod_db.belongs_to_standard_curriculum.connect(node)
                else:
                    raise HTTPException(status_code=404, detail=f'Standard curriculum `{elem}` not found')
        # connect mod areas (required connection)
        if not mod_new.module_areas:
            raise HTTPException(status_code=404, detail='No modules areas specified')
        else:
            for elem in mod_new.module_areas:
                if elem in [x.name for x in ModuleArea.nodes.all()]:
                    node = ModuleArea.nodes.get(name=elem)
                    mod_db.fills_module_area.connect(node)
                else:
                    raise HTTPException(status_code=404, detail=f'Module area `{elem}` not found')

        # disconnect std_curr
        for elem in mod_db.belongs_to_standard_curriculum:
            if elem.name not in mod_new.std_curr_names:
                mod_db.belongs_to_standard_curriculum.disconnect(elem)
        # disconnect mod areas
        for elem in mod_db.fills_module_area:
            if elem.name not in mod_new.module_areas:
                mod_db.fills_module_area.disconnect(elem)
        '''

        # disconnect & connect not required attributes -----------------------------------------------------------------

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

        # connect needed comps
        if mod_new.needs_competences:
            for elem in mod_new.needs_competences:
                if elem in [x.name for x in Competence.nodes.all()]:
                    node = Competence.nodes.get(name=elem)
                    mod_db.needs_competence.connect(node)
                else:
                    raise HTTPException(status_code=404, detail=f'Competence `{elem}` found')
        # connect provided comps (required connection according to Module model, but not according to ModuleDTO)
        if mod_new.provides_competences:
            for elem in mod_new.provides_competences:
                if elem in [x.name for x in Competence.nodes.all()]:
                    node = Competence.nodes.get(name=elem)
                    mod_db.provides_competence.connect(node)
                else:
                    raise HTTPException(status_code=404, detail=f'Competence `{elem}` not found')
        # connect needed micro units
        if mod_new.needs_micro_units:
            for elem in mod_new.needs_micro_units:
                if elem in [x.name for x in MicroUnit.nodes.all()]:
                    node = MicroUnit.nodes.get(name=elem)
                    mod_db.needs_micro_unit.connect(node)
                else:
                    raise HTTPException(status_code=404, detail=f'Micro unit `{elem}` not found')
        # connect provided micro units
        if mod_new.provides_micro_units:
            for elem in mod_new.provides_micro_units:
                if elem in [x.name for x in MicroUnit.nodes.all()]:
                    node = MicroUnit.nodes.get(name=elem)
                    mod_db.provided_by_micro_unit.connect(node)
                else:
                    raise HTTPException(status_code=404, detail=f'Micro unit `{elem}` not found')


