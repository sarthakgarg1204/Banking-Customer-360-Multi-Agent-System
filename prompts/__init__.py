"""Prompts package for Banking Customer 360 solution.

This package contains all prompt templates for:
- Use case analysis and requirements gathering
- Data model and entity relationship design
- Field mapping and transformation logic
"""

from .use_case_prompts import (
    USE_CASE_PROMPT,
    REQUIREMENTS_PROMPT
)
from .data_designer_prompts import (
    DATA_MODEL_PROMPT,
    ENTITY_PROMPT
)
from .mapping_prompts import (
    FIELD_MAPPING_PROMPT,
    TRANSFORMATION_PROMPT
)

__all__ = [
    'USE_CASE_PROMPT',
    'REQUIREMENTS_PROMPT',
    'DATA_MODEL_PROMPT',
    'ENTITY_PROMPT',
    'FIELD_MAPPING_PROMPT',
    'TRANSFORMATION_PROMPT'
]
