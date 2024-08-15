from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Body
from loguru import logger

from modul_graph.DTOs import AnalysisResponseDTO, AnalysisStatus, SuggestionRequestDTO, SuggestionResponseDTO
from modul_graph.utils.controller import is_feasible

from modul_graph.i18n import _

router = APIRouter(prefix="/analysis")


@router.get("/doability/{sc}")
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


@router.put("/suggestion")
def get_curriculum_suggestion(
    req: SuggestionRequestDTO) -> SuggestionResponseDTO:
    """
    Get a suggestion for a standard curriculum
    :param req: request DTO
    :return: analysis result
    """

    logger.info(f"{req}")


    return SuggestionResponseDTO(nodes=[], edges=[])
