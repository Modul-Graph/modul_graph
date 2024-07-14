"""
All DTOs needed for the REST-API are defined here.
"""
from enum import Enum

from pydantic import BaseModel


"""
Module DTOs
"""


class ModuleDTO(BaseModel):
    name: str
    description: str
    cp_plus_description: dict[int, str]
    summer: bool
    winter: bool
    

class ModuleRelationshipDTO(BaseModel):
    std_curr_name: str
    module_area_name: str
    needs_competences: str
    provides_competences: str
    needs_micro_units: str
    provides_micro_units: str


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
