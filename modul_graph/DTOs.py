"""
All DTOs needed for the REST-API are defined here.
"""
from enum import Enum

from pydantic import BaseModel
from typing import Optional


"""
Module DTOs
"""


class ModuleDTO(BaseModel):
    name: str
    description: Optional[str] = None
    cp_plus_description: Optional[dict[int, str]] = None
    summer: bool
    winter: bool

    # connections:
    std_curr_names: list[str]
    module_areas: list[str]
    needs_competences: Optional[list[str]] = None
    provides_competences: Optional[list[str]] = None
    needs_micro_units: Optional[list[str]] = None
    provides_micro_units: Optional[list[str]] = None


"""
Standard Curriculum DTOs
"""


class StandardCurriculumDTO(BaseModel):
    """
    Intermediate transfer object used in the REST-API endpoints
    """
    name: str
    start_winter: bool


"""
Analysis DTOs
"""


class AnalysisStatus(str, Enum):
    """
    Enum for status string constraints
    """
    success = "success"
    info = "info"
    error = "error"
    warning = "warning"


class AnalysisResponseDTO(BaseModel):
    """
    Generic analysis response class. Other analysis respond classes might inherit this class
    """
    status: AnalysisStatus
    message: str
