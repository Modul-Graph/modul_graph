from modul_graph.DTOs import AnalysisResponseDTO, AnalysisStatus


class GraphException(Exception):

    def __init__(self, msg: str):
        super().__init__()
        self.dto = AnalysisResponseDTO(status=AnalysisStatus.error, message=msg)

    def __str__(self):
        return f'{self.dto.status.value}: {self.dto.message}'