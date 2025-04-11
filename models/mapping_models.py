"""
Mapping Models

This module defines the data models used for source-to-target mappings
in the Customer 360 data integration pipeline.
"""

from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum


class DataType(str, Enum):
    """Enumeration of supported data types for mapping."""
    STRING = "STRING"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    DECIMAL = "DECIMAL"
    BOOLEAN = "BOOLEAN"
    DATE = "DATE"
    DATETIME = "DATETIME"
    TIMESTAMP = "TIMESTAMP"
    ARRAY = "ARRAY"
    STRUCT = "STRUCT"
    MAP = "MAP"
    VARIANT = "VARIANT"
    BINARY = "BINARY"

    @classmethod
    def from_source_type(cls, source_type: str, source_system: str) -> "DataType":
        """Map source system type to standardized data type."""
        # Mapping for core banking types
        core_banking_map = {
            "VARCHAR": cls.STRING,
            "CHAR": cls.STRING,
            "NUMBER": cls.DECIMAL,
            "INT": cls.INTEGER,
            "SMALLINT": cls.INTEGER,
            "FLOAT": cls.FLOAT,
            "DECIMAL": cls.DECIMAL,
            "NUMERIC": cls.DECIMAL,
            "DATE": cls.DATE,
            "TIMESTAMP": cls.TIMESTAMP,
            "BOOLEAN": cls.BOOLEAN,
            "BINARY": cls.BINARY
        }

        # Mapping for CRM system types
        crm_map = {
            "Text": cls.STRING,
            "Number": cls.DECIMAL,
            "Integer": cls.INTEGER,
            "Date": cls.DATE,
            "DateTime": cls.DATETIME,
            "Boolean": cls.BOOLEAN,
            "PickList": cls.STRING,
            "MultiPickList": cls.ARRAY,
            "LongText": cls.STRING,
            "Email": cls.STRING,
            "Phone": cls.STRING,
            "URL": cls.STRING,
            "Currency": cls.DECIMAL
        }

        # Standardize type based on source system
        source_type_upper = source_type.upper()
        if source_system.upper() in ["CORE BANKING", "CBS", "LEGACY"]:
            return core_banking_map.get(source_type_upper, cls.STRING)
        elif source_system.upper() in ["CRM", "SALESFORCE", "DYNAMICS"]:
            return crm_map.get(source_type, cls.STRING)

        # Default mapping for unknown systems
        default_map = {
            "VARCHAR": cls.STRING,
            "STRING": cls.STRING,
            "TEXT": cls.STRING,
            "INT": cls.INTEGER,
            "INTEGER": cls.INTEGER,
            "NUMBER": cls.DECIMAL,
            "FLOAT": cls.FLOAT,
            "DOUBLE": cls.FLOAT,
            "DECIMAL": cls.DECIMAL,
            "BOOL": cls.BOOLEAN,
            "BOOLEAN": cls.BOOLEAN,
            "DATE": cls.DATE,
            "DATETIME": cls.DATETIME,
            "TIMESTAMP": cls.TIMESTAMP,
            "ARRAY": cls.ARRAY,
            "LIST": cls.ARRAY,
            "STRUCT": cls.STRUCT,
            "OBJECT": cls.STRUCT,
            "MAP": cls.MAP,
            "BINARY": cls.BINARY
        }

        return default_map.get(source_type_upper, cls.STRING)


class TransformationType(str, Enum):
    """Types of transformations that can be applied to data."""
    DIRECT_MAPPING = "DIRECT_MAPPING"
    TYPE_CONVERSION = "TYPE_CONVERSION"
    VALUE_MAPPING = "VALUE_MAPPING"
    CONCATENATION = "CONCATENATION"
    SUBSTRING = "SUBSTRING"
    MATHEMATICAL_OPERATION = "MATHEMATICAL_OPERATION"
    DATE_TRANSFORMATION = "DATE_TRANSFORMATION"
    CONDITIONAL_LOGIC = "CONDITIONAL_LOGIC"
    AGGREGATION = "AGGREGATION"
    CUSTOM_FUNCTION = "CUSTOM_FUNCTION"
    LOOKUP = "LOOKUP"
    DEFAULT_VALUE = "DEFAULT_VALUE"
    NULL_HANDLING = "NULL_HANDLING"
    FORMAT_STANDARDIZATION = "FORMAT_STANDARDIZATION"


class MappingStatus(str, Enum):
    """Status of the attribute mapping."""
    DRAFT = "DRAFT"
    REVIEWED = "REVIEWED"
    APPROVED = "APPROVED"
    IMPLEMENTED = "IMPLEMENTED"
    DEPRECATED = "DEPRECATED"
    ERROR = "ERROR"


class DataQualityIssue(str, Enum):
    """Types of data quality issues that can affect mappings."""
    MISSING_VALUES = "MISSING_VALUES"
    INCONSISTENT_FORMAT = "INCONSISTENT_FORMAT"
    OUT_OF_RANGE = "OUT_OF_RANGE"
    DUPLICATE_RECORDS = "DUPLICATE_RECORDS"
    INVALID_VALUES = "INVALID_VALUES"
    DATA_TYPE_MISMATCH = "DATA_TYPE_MISMATCH"
    REFERENTIAL_INTEGRITY = "REFERENTIAL_INTEGRITY"
    CHARACTER_ENCODING = "CHARACTER_ENCODING"
    BUSINESS_RULE_VIOLATION = "BUSINESS_RULE_VIOLATION"


class SourceAttributeMetadata(BaseModel):
    """Metadata for a source attribute."""
    system_name: str = Field(..., description="Name of the source system")
    database_name: Optional[str] = Field(None, description="Name of the database")
    schema_name: Optional[str] = Field(None, description="Name of the schema")
    table_name: str = Field(..., description="Name of the table or entity")
    attribute_name: str = Field(..., description="Name of the attribute or column")
    data_type: str = Field(..., description="Original data type in source system")
    nullable: bool = Field(True, description="Flag indicating if attribute can be null")
    primary_key: bool = Field(False, description="Flag indicating if attribute is part of primary key")
    description: Optional[str] = Field(None, description="Description of the attribute")
    sample_values: Optional[List[Any]] = Field(None, description="Sample values for the attribute")

    @property
    def full_path(self) -> str:
        """Return the fully qualified path to the attribute."""
        parts = []
        if self.database_name:
            parts.append(self.database_name)
        if self.schema_name:
            parts.append(self.schema_name)
        parts.append(self.table_name)
        parts.append(self.attribute_name)
        return ".".join(parts)


class TargetAttributeMetadata(BaseModel):
    """Metadata for a target attribute in the Customer 360 model."""
    entity_name: str = Field(..., description="Name of the target entity")
    attribute_path: str = Field(..., description="Path to the attribute within the entity")
    data_type: DataType = Field(..., description="Data type in the target schema")
    nullable: bool = Field(True, description="Flag indicating if attribute can be null")
    description: Optional[str] = Field(None, description="Description of the attribute")
    business_definition: Optional[str] = Field(None, description="Business definition of the attribute")
    validation_rules: Optional[List[str]] = Field(None, description="Validation rules for the attribute")

    @property
    def full_path(self) -> str:
        """Return the fully qualified path to the attribute."""
        return f"{self.entity_name}.{self.attribute_path}"


class ValueMappingRule(BaseModel):
    """Rule for mapping source values to target values."""
    source_value: Any = Field(..., description="Value in the source system")
    target_value: Any = Field(..., description="Corresponding value in the target system")
    description: Optional[str] = Field(None, description="Description of the mapping")


class TransformationRule(BaseModel):
    """Rule for transforming data from source to target."""
    transformation_type: TransformationType = Field(..., description="Type of transformation")
    transformation_logic: str = Field(..., description="Logic or expression for the transformation")
    description: Optional[str] = Field(None, description="Description of the transformation")
    value_mappings: Optional[List[ValueMappingRule]] = Field(None, description="Value mapping rules, if applicable")

    def to_sql(self) -> str:
        """Convert the transformation logic to SQL syntax."""
        # This is a simplified implementation
        return self.transformation_logic


class DataQualityCheck(BaseModel):
    """Data quality check for a mapping."""
    check_type: DataQualityIssue = Field(..., description="Type of data quality issue to check for")
    check_logic: str = Field(..., description="Logic or expression for the check")
    severity: str = Field("ERROR", description="Severity of the issue (ERROR, WARNING, INFO)")
    description: Optional[str] = Field(None, description="Description of the check")
    remediation: Optional[str] = Field(None, description="Remediation strategy for issues found")

    def to_sql(self) -> str:
        """Convert the check logic to SQL syntax."""
        # This is a simplified implementation
        return self.check_logic


class AttributeMapping(BaseModel):
    """Mapping between source and target attributes."""
    mapping_id: str = Field(..., description="Unique identifier for the mapping")
    source_attribute: SourceAttributeMetadata
    target_attribute: TargetAttributeMetadata
    transformation_rule: TransformationRule
    data_quality_checks: List[DataQualityCheck] = Field(default_factory=list)
    status: MappingStatus = Field(MappingStatus.DRAFT, description="Status of the mapping")
    created_by: Optional[str] = Field(None, description="User who created the mapping")
    created_at: Optional[str] = Field(None, description="Timestamp when mapping was created")
    updated_by: Optional[str] = Field(None, description="User who last updated the mapping")
    updated_at: Optional[str] = Field(None, description="Timestamp when mapping was last updated")
    comments: Optional[str] = Field(None, description="Comments on the mapping")

    def to_sql(self) -> str:
        """Generate SQL for the mapping transformation."""
        source_path = self.source_attribute.full_path
        target_path = self.target_attribute.full_path
        transform_sql = self.transformation_rule.to_sql()

        # Simple SQL generation - would be more complex in real implementation
        if self.transformation_rule.transformation_type == TransformationType.DIRECT_MAPPING:
            return f"{target_path} = {source_path}"
        else:
            return f"{target_path} = {transform_sql}"


class MappingSet(BaseModel):
    """Collection of related attribute mappings."""
    mapping_set_id: str = Field(..., description="Unique identifier for the mapping set")
    name: str = Field(..., description="Name of the mapping set")
    description: Optional[str] = Field(None, description="Description of the mapping set")
    source_systems: List[str] = Field(..., description="Source systems involved in the mapping set")
    target_entities: List[str] = Field(..., description="Target entities in the mapping set")
    mappings: List[AttributeMapping] = Field(..., description="List of attribute mappings")
    status: MappingStatus = Field(MappingStatus.DRAFT, description="Status of the mapping set")
    created_by: Optional[str] = Field(None, description="User who created the mapping set")
    created_at: Optional[str] = Field(None, description="Timestamp when mapping set was created")
    updated_by: Optional[str] = Field(None, description="User who last updated the mapping set")
    updated_at: Optional[str] = Field(None, description="Timestamp when mapping set was last updated")

    def to_sql(self) -> str:
        """Generate SQL for the entire mapping set."""
        sql_parts = []
        for mapping in self.mappings:
            sql_parts.append(mapping.to_sql())

        return ";\n".join(sql_parts)

    def get_source_tables(self) -> List[str]:
        """Get list of all source tables used in the mapping set."""
        tables = set()
        for mapping in self.mappings:
            source = mapping.source_attribute
            tables.add(f"{source.system_name}.{source.table_name}")

        return list(tables)

    def get_mapping_statistics(self) -> Dict[str, Any]:
        """Get statistics about the mapping set."""
        stats = {
            "total_mappings": len(self.mappings),
            "status_counts": {},
            "source_system_counts": {},
            "target_entity_counts": {},
            "transformation_type_counts": {}
        }

        # Count by status
        for mapping in self.mappings:
            # Status counts
            status = mapping.status.value
            if status in stats["status_counts"]:
                stats["status_counts"][status] += 1
            else:
                stats["status_counts"][status] = 1

            # Source system counts
            source_system = mapping.source_attribute.system_name
            if source_system in stats["source_system_counts"]:
                stats["source_system_counts"][source_system] += 1
            else:
                stats["source_system_counts"][source_system] = 1

            # Target entity counts
            target_entity = mapping.target_attribute.entity_name
            if target_entity in stats["target_entity_counts"]:
                stats["target_entity_counts"][target_entity] += 1
            else:
                stats["target_entity_counts"][target_entity] = 1

            # Transformation type counts
            transform_type = mapping.transformation_rule.transformation_type.value
            if transform_type in stats["transformation_type_counts"]:
                stats["transformation_type_counts"][transform_type] += 1
            else:
                stats["transformation_type_counts"][transform_type] = 1

        return stats


class MappingProject(BaseModel):
    """Project containing multiple mapping sets for a Customer 360 implementation."""
    project_id: str = Field(..., description="Unique identifier for the project")
    name: str = Field(..., description="Name of the project")
    description: Optional[str] = Field(None, description="Description of the project")
    business_owner: Optional[str] = Field(None, description="Business owner of the project")
    technical_owner: Optional[str] = Field(None, description="Technical owner of the project")
    status: str = Field("ACTIVE", description="Status of the project")
    mapping_sets: List[MappingSet] = Field(default_factory=list)
    start_date: Optional[str] = Field(None, description="Start date of the project")
    target_completion_date: Optional[str] = Field(None, description="Target completion date")
    actual_completion_date: Optional[str] = Field(None, description="Actual completion date")
    created_by: Optional[str] = Field(None, description="User who created the project")
    created_at: Optional[str] = Field(None, description="Timestamp when project was created")
    updated_by: Optional[str] = Field(None, description="User who last updated the project")
    updated_at: Optional[str] = Field(None, description="Timestamp when project was last updated")

    def get_completion_percentage(self) -> float:
        """Calculate the completion percentage of the project."""
        if not self.mapping_sets:
            return 0.0

        total_mappings = 0
        completed_mappings = 0

        for mapping_set in self.mapping_sets:
            total_mappings += len(mapping_set.mappings)
            for mapping in mapping_set.mappings:
                if mapping.status in [MappingStatus.APPROVED, MappingStatus.IMPLEMENTED]:
                    completed_mappings += 1

        if total_mappings == 0:
            return 0.0

        return (completed_mappings / total_mappings) * 100.0

    def get_mapping_summary(self) -> Dict[str, Any]:
        """Get a summary of all mappings in the project."""
        summary = {
            "total_mapping_sets": len(self.mapping_sets),
            "total_mappings": 0,
            "source_systems": set(),
            "target_entities": set(),
            "status_summary": {
                "DRAFT": 0,
                "REVIEWED": 0,
                "APPROVED": 0,
                "IMPLEMENTED": 0,
                "DEPRECATED": 0,
                "ERROR": 0
            }
        }

        for mapping_set in self.mapping_sets:
            summary["total_mappings"] += len(mapping_set.mappings)
            summary["source_systems"].update(mapping_set.source_systems)
            summary["target_entities"].update(mapping_set.target_entities)

            for mapping in mapping_set.mappings:
                status = mapping.status.value
                if status in summary["status_summary"]:
                    summary["status_summary"][status] += 1

        # Convert sets to lists for JSON serialization
        summary["source_systems"] = list(summary["source_systems"])
        summary["target_entities"] = list(summary["target_entities"])

        return summary


class DependencyType(str, Enum):
    """Types of dependencies between mappings."""
    SOURCE_DEPENDENCY = "SOURCE_DEPENDENCY"  # Target depends on source being available
    TRANSFORMATION_DEPENDENCY = "TRANSFORMATION_DEPENDENCY"  # Transformation depends on another attribute
    BUSINESS_RULE_DEPENDENCY = "BUSINESS_RULE_DEPENDENCY"  # Business rule dependency
    TECHNICAL_DEPENDENCY = "TECHNICAL_DEPENDENCY"  # Technical implementation dependency


class MappingDependency(BaseModel):
    """Dependency between attribute mappings."""
    dependency_id: str = Field(..., description="Unique identifier for the dependency")
    mapping_id: str = Field(..., description="ID of the mapping that has a dependency")
    dependent_mapping_id: str = Field(..., description="ID of the mapping that is depended upon")
    dependency_type: DependencyType = Field(..., description="Type of dependency")
    description: Optional[str] = Field(None, description="Description of the dependency")
    is_blocking: bool = Field(True, description="Flag indicating if this is a blocking dependency")


class DataProfileMetrics(BaseModel):
    """Data profiling metrics for a source attribute."""
    attribute_id: str = Field(..., description="ID of the source attribute")
    row_count: int = Field(..., description="Total number of rows")
    null_count: int = Field(..., description="Number of null values")
    null_percentage: float = Field(..., description="Percentage of null values")
    distinct_count: int = Field(..., description="Number of distinct values")
    distinct_percentage: float = Field(..., description="Percentage of distinct values")
    min_value: Optional[Any] = Field(None, description="Minimum value")
    max_value: Optional[Any] = Field(None, description="Maximum value")
    avg_value: Optional[float] = Field(None, description="Average value (for numeric attributes)")
    std_dev: Optional[float] = Field(None, description="Standard deviation (for numeric attributes)")
    min_length: Optional[int] = Field(None, description="Minimum length (for string attributes)")
    max_length: Optional[int] = Field(None, description="Maximum length (for string attributes)")
    avg_length: Optional[float] = Field(None, description="Average length (for string attributes)")
    pattern_analysis: Optional[Dict[str, int]] = Field(None, description="Count of different patterns found")
    top_values: Optional[List[Dict[str, Any]]] = Field(None, description="Most common values and their frequencies")
    histogram_data: Optional[List[Dict[str, Any]]] = Field(None, description="Histogram data points")
    last_profiled_at: Optional[str] = Field(None, description="Timestamp when profiling was last run")


class DataLineage(BaseModel):
    """Data lineage information for target attributes."""
    target_attribute_id: str = Field(..., description="ID of the target attribute")
    source_path: List[Dict[str, Any]] = Field(..., description="Path through source systems")
    transformations: List[Dict[str, Any]] = Field(..., description="Transformations applied")
    data_quality_impact: Optional[Dict[str, Any]] = Field(None, description="Impact on data quality")
    lineage_graph_data: Optional[Dict[str, Any]] = Field(None, description="Graph data for visualization")


class ValidationResult(BaseModel):
    """Results of validation checks for a mapping."""
    mapping_id: str = Field(..., description="ID of the mapping being validated")
    validation_timestamp: str = Field(..., description="Timestamp when validation was performed")
    validation_status: str = Field(..., description="Overall status (PASSED, FAILED, WARNING)")
    validation_checks: List[Dict[str, Any]] = Field(..., description="Individual validation checks")
    source_row_count: Optional[int] = Field(None, description="Number of source rows processed")
    target_row_count: Optional[int] = Field(None, description="Number of target rows produced")
    row_count_match: Optional[bool] = Field(None, description="Flag indicating if row counts match expectations")
    data_quality_issues: List[Dict[str, Any]] = Field(default_factory=list, description="Data quality issues found")
    performance_metrics: Optional[Dict[str, Any]] = Field(None, description="Performance metrics for the validation")


class MappingTemplate(BaseModel):
    """Template for common mapping patterns."""
    template_id: str = Field(..., description="Unique identifier for the template")
    name: str = Field(..., description="Name of the template")
    description: Optional[str] = Field(None, description="Description of the template")
    source_pattern: Dict[str, Any] = Field(..., description="Pattern for matching source attributes")
    target_pattern: Dict[str, Any] = Field(..., description="Pattern for matching target attributes")
    transformation_template: Dict[str, Any] = Field(..., description="Template for transformation logic")
    applicable_systems: List[str] = Field(default_factory=list, description="Systems where this template applies")
    examples: Optional[List[Dict[str, Any]]] = Field(None, description="Example applications of the template")
    created_by: Optional[str] = Field(None, description="User who created the template")
    created_at: Optional[str] = Field(None, description="Timestamp when template was created")
    usage_count: Optional[int] = Field(0, description="Count of how many times template has been used")

    def matches_source(self, source_attribute: SourceAttributeMetadata) -> bool:
        """Check if a source attribute matches this template's pattern."""
        # Implementation would check if the attribute matches the pattern
        # This is a placeholder implementation
        return True

    def matches_target(self, target_attribute: TargetAttributeMetadata) -> bool:
        """Check if a target attribute matches this template's pattern."""
        # Implementation would check if the attribute matches the pattern
        # This is a placeholder implementation
        return True

    def generate_transformation(self, source: SourceAttributeMetadata, target: TargetAttributeMetadata) -> TransformationRule:
        """Generate a transformation rule based on the template."""
        # Implementation would generate a transformation rule
        # This is a placeholder implementation
        return TransformationRule(
            transformation_type=TransformationType.DIRECT_MAPPING,
            transformation_logic=f"{source.attribute_name}"
        )


class MappingExample(BaseModel):
    """Example mapping for documentation and reference."""
    example_id: str = Field(..., description="Unique identifier for the example")
    name: str = Field(..., description="Name of the example")
    description: Optional[str] = Field(None, description="Description of the example")
    source_attribute: SourceAttributeMetadata
    target_attribute: TargetAttributeMetadata
    transformation_rule: TransformationRule
    comments: Optional[str] = Field(None, description="Comments explaining the example")
    tags: List[str] = Field(default_factory=list, description="Tags for categorizing the example")
    complexity: str = Field("MEDIUM", description="Complexity level (SIMPLE, MEDIUM, COMPLEX)")

    class Config:
        schema_extra = {
            "example": {
                "example_id": "EX-001",
                "name": "Basic Customer Name Mapping",
                "description": "Demonstrates mapping of customer names from core banking to Customer 360",
                "source_attribute": {
                    "system_name": "Core Banking",
                    "table_name": "CUSTOMER_MASTER",
                    "attribute_name": "CUST_FIRST_NAME",
                    "data_type": "VARCHAR",
                    "nullable": False,
                    "primary_key": False
                },
                "target_attribute": {
                    "entity_name": "DemographicProfile",
                    "attribute_path": "name.first_name",
                    "data_type": "STRING",
                    "nullable": False,
                    "description": "Customer's first name"
                },
                "transformation_rule": {
                    "transformation_type": "FORMAT_STANDARDIZATION",
                    "transformation_logic": "INITCAP(TRIM(CUST_FIRST_NAME))",
                    "description": "Standardize name format with initial capital letter and trimmed spaces"
                },
                "complexity": "SIMPLE",
                "tags": ["Name", "Core Banking", "Standardization"]
            }
        }
