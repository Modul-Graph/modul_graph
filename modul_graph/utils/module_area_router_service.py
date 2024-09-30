from fastapi import HTTPException
from neomodel import db  # type: ignore

from modul_graph.DTOs import ModuleAreaDTO
from modul_graph.models.module import Module
from modul_graph.models.module_area import ModuleArea


class ModuleAreaRouterService:
    @staticmethod
    def get_module_area(mod_ar_name: str) -> ModuleAreaDTO:
        ret: ModuleArea = ModuleArea.nodes.get(name=mod_ar_name)
        if not ret or not ret.is_wpf:
            raise HTTPException(status_code=404, detail=f'Module area {mod_ar_name} not found')

        return ModuleAreaDTO(name=ret.name,
                             cp=ret.cp,
                             filled_by_module=[x.name for x in ret.filled_by_module.all()])

    @db.transaction
    def create_module_area(self, mod_ar: ModuleAreaDTO) -> None:

        # check if there is already a module area with the specified name
        area_exists_already: bool = True
        try:
            ModuleArea.nodes.get(name=mod_ar.name)
        except Exception:
            area_exists_already = False
        if area_exists_already:
            raise HTTPException(status_code=409, detail=f'A module area with the name {mod_ar.name} already exists')

        # create new ModuleArea
        mod_ar_to_save = ModuleArea()
        mod_ar_to_save.name = mod_ar.name
        mod_ar_to_save.cp = mod_ar.cp
        mod_ar_to_save.save()

        # connect modules to new module area
        for elem in mod_ar.filled_by_module:
            mod: Module = Module.nodes.get(name=elem)
            if not mod:
                raise HTTPException(status_code=404, detail=f'Module {elem} not found')
            mod_ar_to_save.filled_by_module.connect(mod)

    @staticmethod
    def delete_module_area(name: str) -> None:
        mod_ar: ModuleArea = ModuleArea.nodes.get(name=name)
        if not mod_ar:
            raise HTTPException(status_code=404, detail=f'Module area {name} not found')
        mod_ar.delete()

    @db.transaction
    def update_module_area(self, name, mod_ar) -> None:
        mod_ar_to_update: ModuleArea = ModuleArea.nodes.get(name=name)
        if not mod_ar_to_update:
            raise HTTPException(status_code=404, detail=f'Module area {name} not found')

        mod_ar_to_update.name = mod_ar.name
        mod_ar_to_update.cp = mod_ar.cp
        mod_ar_to_update.save()
        mod_ar_to_update.filled_by_module.disconnect_all()

        for elem in mod_ar.filled_by_module:
            mod: Module = Module.nodes.get(name=elem)
            if not mod:
                raise HTTPException(status_code=404, detail=f'Module {elem} not found')
            mod_ar_to_update.filled_by_module.connect(mod)
