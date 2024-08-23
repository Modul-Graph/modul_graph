from fastapi import HTTPException

from modul_graph.models.competence import Competence
from modul_graph.models.micro_unit import MicroUnit
from modul_graph.models.module import Module
from modul_graph.models.module_area import ModuleArea
from modul_graph.models.standard_curriculum import StandardCurriculum
from modul_graph.DTOs import ModuleDTO
from neomodel import db  # type: ignore

"""
This service is at the moment only responsible for 'Module' information.
Since it's not a lot, it hasn't been separated into service, DAO and repo.
"""


class ModuleRouterService:

    def get_module(self, mod_name: str) -> ModuleDTO:

        self.__does_mod_exist__not_found_exception(mod_name)
        ret_mod: Module = Module.nodes.get(name=mod_name)

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
        self.__create_module(mod)

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
        self.__update_mod(Module.nodes.get(name=identifier), mod_new)

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
    def __create_module(self, moduleDTO: ModuleDTO) -> None:
        # this method is almost a duplicate of the update method
        # but the update method can't be used to create modules
        # because the check "elem not in [x.name for x in mod_db.belongs_to_standard_curriculum.all()]"
        # accesses the connection "belongs_to_standard_curriculum" which has a cardinality of OneOrMore
        # for a new module, it would raise an exception that there aren't any connections

        module = Module()

        module.name = moduleDTO.name
        module.description = moduleDTO.description
        module.cp_plus_description = moduleDTO.cp_plus_description
        module.is_in_summer = moduleDTO.summer
        module.is_in_winter = moduleDTO.winter

        module.save()

        # connect standard curricula
        for elem in moduleDTO.std_curr_names:
            # if elem is a valid standard curriculum
            if elem in [x.name for x in StandardCurriculum.nodes.all()]:
                node = StandardCurriculum.nodes.get(name=elem)
                module.belongs_to_standard_curriculum.connect(node)
            elif elem not in [x.name for x in StandardCurriculum.nodes.all()]:
                raise HTTPException(status_code=404, detail=f'Standard curriculum `{elem}` not found')

        # connect module areas
        for elem in moduleDTO.module_areas:
            # if elem is a valid module area and is not already connected
            if elem in [x.name for x in ModuleArea.nodes.all()]:
                node = ModuleArea.nodes.get(name=elem)
                module.fills_module_area.connect(node)
            elif elem not in [x.name for x in ModuleArea.nodes.all()]:
                raise HTTPException(status_code=404, detail=f'Module area `{elem}` not found')

        # connect needed comps
        if moduleDTO.needs_competences:
            for elem in moduleDTO.needs_competences:
                if elem in [x.name for x in Competence.nodes.all()]:
                    node = Competence.nodes.get(name=elem)
                    module.needs_competence.connect(node)
                else:
                    raise HTTPException(status_code=404, detail=f'Competence `{elem}` found')
        # connect provided comps (required connection according to Module model, but not according to ModuleDTO)
        if moduleDTO.provides_competences:
            for elem in moduleDTO.provides_competences:
                if elem in [x.name for x in Competence.nodes.all()]:
                    node = Competence.nodes.get(name=elem)
                    module.provides_competence.connect(node)
                else:
                    raise HTTPException(status_code=404, detail=f'Competence `{elem}` not found')
        # connect needed micro units
        if moduleDTO.needs_micro_units:
            for elem in moduleDTO.needs_micro_units:
                if elem in [x.name for x in MicroUnit.nodes.all()]:
                    node = MicroUnit.nodes.get(name=elem)
                    module.needs_micro_unit.connect(node)
                else:
                    raise HTTPException(status_code=404, detail=f'Micro unit `{elem}` not found')
        # connect provided micro units
        if moduleDTO.provides_micro_units:
            for elem in moduleDTO.provides_micro_units:
                if elem in [x.name for x in MicroUnit.nodes.all()]:
                    node = MicroUnit.nodes.get(name=elem)
                    module.provided_by_micro_unit.connect(node)
                else:
                    raise HTTPException(status_code=404, detail=f'Micro unit `{elem}` not found')


    @db.transaction
    def __update_mod(self, mod_db: Module, mod_new: ModuleDTO) -> None:
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


