"""Models package for Banking Customer 360 solution.

This package contains all data models and schemas:
- CustomerSchema: Defines the core customer data structure
- Mapping Models: Field mappings between systems
- Source Models: Source system data structures
"""

from .customer_schema import CustomerSchema
from .mapping_models import MappingModel, FieldMapping
from .source_models import SourceSystemModel

__all__ = [
    'CustomerSchema',
    'MappingModel',
    'FieldMapping',
    'SourceSystemModel'
]
