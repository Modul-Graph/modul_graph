from DTOs import ModuleDTO, AnalysisResponseDTO


class RouterService:

    def get_module(self, mod_name: str) -> ModuleDTO:
        pass

    def create_module(self, mod: ModuleDTO) -> AnalysisResponseDTO:
        pass

    def delete_module(self, mod_name: str) -> AnalysisResponseDTO:
        pass

    def update_module(self, mod: ModuleDTO) -> AnalysisResponseDTO:
        pass
