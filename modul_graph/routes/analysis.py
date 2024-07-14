from fastapi import APIRouter, HTTPException

from modul_graph.DTOs import AnalysisResponseDTO, AnalysisStatus
from modul_graph.utils.controller import is_feasible

from modul_graph.i18n import _

router = APIRouter(prefix="/analysis")


@router.get("/doability")
def get_doability(sc: str) -> AnalysisResponseDTO:
    """
    Return do
    :param sc: Standard curriculum to get the doability for
    :raises HTTPException 400: if standard curriculum doesn't exist
    :return: analysis result
    """

    try:
        is_ok: bool = is_feasible(sc)
    except ValueError as e:
        raise HTTPException(400, "standard curriculum doesn't exist")

    res: AnalysisResponseDTO
    if is_ok:
        res = AnalysisResponseDTO(status=AnalysisStatus.success, message=_("Doability success message"))

    else:
        res = AnalysisResponseDTO(status=AnalysisStatus.error, message=_("Doability error message"))

    return res
