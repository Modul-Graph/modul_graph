from fastapi import HTTPException

from modul_graph.models.module_cell import ModuleCell
from modul_graph.models.competence import Competence
from modul_graph.models.micro_unit import MicroUnit
from modul_graph.models.module import Module
from modul_graph.models.module_area import ModuleArea
from modul_graph.models.standard_curriculum import StandardCurriculum
from modul_graph.DTOs import ModuleDTO, ModuleAreaDTO
from neomodel import db  # type: ignore
from modul_graph.utils.module_area_router_service import ModuleAreaRouterService

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
        # [this is an old comment, cardinalities of OneOrMore don't exist anymore]
        # todo: rewrite code to fit new cardinality (ModuleAreas can be connected in the method __connect_optional_relationships)
        # parts of this method are almost a duplicate of the update method
        # but the update method can't be used to create modules
        # because the check "elem not in [x.name for x in mod_db.belongs_to_standard_curriculum.all()]"
        # accesses the connection "belongs_to_standard_curriculum" of the Module entity, which has a cardinality of OneOrMore
        # for a newly created module, it would raise an exception that there aren't any connections

        module: Module = self.__assign_attributes(Module(), moduleDTO)
        module.save()

        # connect required relationships:
        # connect standard curricula
        if moduleDTO.std_curr_names:
            for elem in moduleDTO.std_curr_names:
                # if elem is a valid standard curriculum
                if elem in [x.name for x in StandardCurriculum.nodes.all()]:
                    node = StandardCurriculum.nodes.get(name=elem)
                    module.belongs_to_standard_curriculum.connect(node)
                elif elem not in [x.name for x in StandardCurriculum.nodes.all()]:
                    raise HTTPException(status_code=404, detail=f'Standard curriculum `{elem}` not found')
        # connect module areas
        if moduleDTO.module_areas:
            for elem in moduleDTO.module_areas:
                # if elem is a valid module area and is not already connected
                if elem in [x.name for x in ModuleArea.nodes.all()]:
                    node = ModuleArea.nodes.get(name=elem)
                    module.fills_module_area.connect(node)
                elif elem not in [x.name for x in ModuleArea.nodes.all()]:
                    raise HTTPException(status_code=404, detail=f'Module area `{elem}` not found')

        self.__connect_optional_relationships(module, moduleDTO)

    @db.transaction
    def __update_mod(self, mod_db: Module, mod_new: ModuleDTO) -> None:

        self.__assign_attributes(mod_db, mod_new)

        mod_db.save()

        # update required connections (it's not possible to first disconnect the old ones and then connect the new ones
        # because of AttemptedCardinalityViolation):

        # if no standard curriculum was specified -> invalid request
        if not mod_new.std_curr_names:
            raise HTTPException(status_code=404, detail='No standard curricula specified')

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
            mod_db.belongs_to_standard_curriculum.disconnect(StandardCurriculum.nodes.get(name=elem))

        # connect new module areas
        if mod_new.module_areas:
            for elem in mod_new.module_areas:
                # if elem is a valid module area and is not already connected
                if elem in [x.name for x in ModuleArea.nodes.all()] and elem not in [x.name for x in mod_db.fills_module_area.all()]:
                    node = ModuleArea.nodes.get(name=elem)
                    mod_db.fills_module_area.connect(node)
                elif elem not in [x.name for x in ModuleArea.nodes.all()]:
                    raise HTTPException(status_code=404, detail=f'Module area `{elem}` not found')

        # disconnect old module areas which are no longer used (disconnect everything in [old module areas minus new module areas])
        if not mod_new.module_areas:
            mod_new.module_areas = []
        for elem in set([x.name for x in mod_db.fills_module_area.all()]) - set(mod_new.module_areas):
            mod_db.fills_module_area.disconnect(ModuleArea.nodes.get(name=elem))

        # disconnect optional relationships
        for elem in mod_db.needs_competence:
            mod_db.needs_competence.disconnect(Competence.nodes.get(name=elem))
        for elem in mod_db.provides_competence:
            mod_db.provides_competence.disconnect(Competence.nodes.get(name=elem))
        for elem in mod_db.needs_micro_unit:
            mod_db.needs_micro_unit.disconnect(MicroUnit.nodes.get(name=elem))
        for elem in mod_db.provided_by_micro_unit:
            mod_db.provided_by_micro_unit.disconnect(MicroUnit.nodes.get(name=elem))

        self.__connect_optional_relationships(mod_db, mod_new)

    def __assign_attributes(self, module: Module, moduleDTO: ModuleDTO) -> Module:
        module.name = moduleDTO.name
        module.module_description = moduleDTO.description
        module.cp_plus_description = moduleDTO.cp_plus_description
        module.is_in_summer = moduleDTO.summer
        module.is_in_winter = moduleDTO.winter

        return module

    def __connect_optional_relationships(self, module: Module, moduleDTO: ModuleDTO):
        # connect needed comps
        if moduleDTO.needs_competences:
            for elem in moduleDTO.needs_competences:
                if elem in [x.name for x in Competence.nodes.all()]:
                    node = Competence.nodes.get(name=elem)
                    module.needs_competence.connect(node)
                else:
                    raise HTTPException(status_code=404, detail=f'Competence `{elem}` found')
        # connect provided comps
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

    def create_required_module(self, module: ModuleDTO) -> None:

        # check if ModuleArea and ModuleCell with name/identifier = module.name already exist
        mod_ar_exists_already: bool = True
        try:
            ModuleArea.nodes.get(name=module.name)
        except Exception:
            mod_ar_exists_already = False

        cell_exists_already: bool = True
        try:
            ModuleCell.nodes.get(identifier=module.name)
        except Exception:
            cell_exists_already = False

        if mod_ar_exists_already or cell_exists_already:
            raise HTTPException(status_code=409, detail='A module area or cell with the name ' + module.name + ' already exists')

        # create Module
        self.create_module(module)

        # link it to new ModuleArea
        ModuleAreaRouterService().create_module_area(ModuleAreaDTO(name=module.name, filled_by_module=[module.name]))

        # link ModuleArea to new ModuleCell
        cell = ModuleCell()
        cell.identifier = module.name
        cell.save()
        cell.filled_by_module_area.connect(ModuleArea.nodes.get(name=module.name))

    @db.transaction
    def delete_required_module(self, name: str):
        # delete module area and cell
        db.cypher_query('MATCH (m:ModuleCell)<-[:FILLS]-(r:ModuleArea)<-[:FILLS]-(mod:Module {name:\'' + name + '\'}) DETACH DELETE m, r')
        # delete module
        self.delete_module(name)

