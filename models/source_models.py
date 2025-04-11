"""
Source System Models

This module defines data models representing banking source systems and their metadata.
These models are used to catalog and interact with source systems during the data mapping process.
"""

from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class SourceSystemType(str, Enum):
    """Types of source systems in a banking environment."""
    CORE_BANKING = "CORE_BANKING"
    CRM = "CRM"
    DIGITAL_BANKING = "DIGITAL_BANKING"
    CARD_MANAGEMENT = "CARD_MANAGEMENT"
    LOAN_ORIGINATION = "LOAN_ORIGINATION"
    PAYMENTS = "PAYMENTS"
    WEALTH_MANAGEMENT = "WEALTH_MANAGEMENT"
    RISK_MANAGEMENT = "RISK_MANAGEMENT"
    COMPLIANCE = "COMPLIANCE"
    GENERAL_LEDGER = "GENERAL_LEDGER"
    DATA_WAREHOUSE = "DATA_WAREHOUSE"
    DATA_LAKE = "DATA_LAKE"
    EXTERNAL = "EXTERNAL"
    LEGACY = "LEGACY"
    OTHER = "OTHER"


class DataFrequency(str, Enum):
    """Data update frequency types."""
    REAL_TIME = "REAL_TIME"
    NEAR_REAL_TIME = "NEAR_REAL_TIME"
    HOURLY = "HOURLY"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    YEARLY = "YEARLY"
    AD_HOC = "AD_HOC"
    BATCH = "BATCH"


class DataQualityLevel(str, Enum):
    """Data quality level classification."""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    UNKNOWN = "UNKNOWN"


class AccessMethod(str, Enum):
    """Methods to access source system data."""
    API = "API"
    DIRECT_DB = "DIRECT_DB"
    FILE_TRANSFER = "FILE_TRANSFER"
    ETL_TOOL = "ETL_TOOL"
    MESSAGING = "MESSAGING"
    CDC = "CDC"
    REPLICATION = "REPLICATION"
    DATA_VIRTUALIZATION = "DATA_VIRTUALIZATION"
    MANUAL = "MANUAL"


class DatabaseType(str, Enum):
    """Types of databases used in source systems."""
    ORACLE = "ORACLE"
    SQL_SERVER = "SQL_SERVER"
    DB2 = "DB2"
    MYSQL = "MYSQL"
    POSTGRESQL = "POSTGRESQL"
    MONGODB = "MONGODB"
    CASSANDRA = "CASSANDRA"
    HADOOP = "HADOOP"
    SNOWFLAKE = "SNOWFLAKE"
    REDSHIFT = "REDSHIFT"
    BIGQUERY = "BIGQUERY"
    SYBASE = "SYBASE"
    TERADATA = "TERADATA"
    SAP_HANA = "SAP_HANA"
    OTHER = "OTHER"


class FileFormat(str, Enum):
    """File formats for file-based source systems."""
    CSV = "CSV"
    JSON = "JSON"
    XML = "XML"
    PARQUET = "PARQUET"
    AVRO = "AVRO"
    ORC = "ORC"
    EXCEL = "EXCEL"
    FIXED_WIDTH = "FIXED_WIDTH"
    DELIMITED = "DELIMITED"
    TEXT = "TEXT"
    PDF = "PDF"
    OTHER = "OTHER"


class ConnectionCredentials(BaseModel):
    """Credentials for connecting to a source system."""
    credential_id: str = Field(..., description="Unique identifier for the credentials")
    credential_type: str = Field(..., description="Type of credentials (username/password, API key, etc.)")
    connection_string: Optional[str] = Field(None, description="Database connection string, if applicable")
    username: Optional[str] = Field(None, description="Username, if applicable")
    password: Optional[str] = Field(None, description="Password placeholder - actual value stored securely")
    api_key: Optional[str] = Field(None, description="API key placeholder - actual value stored securely")
    api_token: Optional[str] = Field(None, description="API token placeholder - actual value stored securely")
    certificate_path: Optional[str] = Field(None, description="Path to certificate file, if applicable")
    key_path: Optional[str] = Field(None, description="Path to key file, if applicable")
    secret_manager_ref: Optional[str] = Field(None, description="Reference to secrets in secret manager")
    expiration_date: Optional[datetime] = Field(None, description="Expiration date for credentials")
    is_encrypted: bool = Field(True, description="Flag indicating if credentials are encrypted")

    class Config:
        """Pydantic model configuration."""
        # Extra security measure to ensure sensitive fields are not included in exports/logs
        schema_extra = {
            "sensitive_fields": ["password", "api_key", "api_token", "connection_string"]
        }


class ContactPerson(BaseModel):
    """Contact person information for a source system."""
    name: str = Field(..., description="Name of the contact person")
    role: str = Field(..., description="Role or title of the contact person")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    department: Optional[str] = Field(None, description="Department or team")
    is_primary: bool = Field(False, description="Flag indicating if this is the primary contact")


class DataRetentionPolicy(BaseModel):
    """Data retention policy information."""
    retention_period: str = Field(..., description="Period for which data is retained")
    archive_policy: Optional[str] = Field(None, description="Policy for archiving data")
    deletion_policy: Optional[str] = Field(None, description="Policy for deleting data")
    compliance_requirements: Optional[List[str]] = Field(None, description="Compliance requirements affecting retention")
    exceptions: Optional[List[str]] = Field(None, description="Exceptions to the retention policy")


class DataPrivacyInfo(BaseModel):
    """Data privacy information for a source system or table."""
    contains_pii: bool = Field(False, description="Flag indicating if contains personally identifiable information")
    contains_sensitive_data: bool = Field(False, description="Flag indicating if contains sensitive data")
    data_classification: str = Field("PUBLIC", description="Data classification (PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED)")
    compliance_regimes: List[str] = Field(default_factory=list, description="Applicable compliance regimes (GDPR, CCPA, etc.)")
    encryption_required: bool = Field(False, description="Flag indicating if encryption is required")
    masking_required: bool = Field(False, description="Flag indicating if data masking is required")
    access_restrictions: Optional[List[str]] = Field(None, description="Access restrictions for the data")


class SourceAttribute(BaseModel):
    """Attribute (column) in a source system table."""
    attribute_id: str = Field(..., description="Unique identifier for the attribute")
    name: str = Field(..., description="Name of the attribute")
    description: Optional[str] = Field(None, description="Description of the attribute")
    data_type: str = Field(..., description="Data type of the attribute")
    length: Optional[int] = Field(None, description="Length of the attribute, if applicable")
    precision: Optional[int] = Field(None, description="Precision for numeric types, if applicable")
    scale: Optional[int] = Field(None, description="Scale for numeric types, if applicable")
    is_nullable: bool = Field(True, description="Flag indicating if attribute can be null")
    is_primary_key: bool = Field(False, description="Flag indicating if attribute is part of primary key")
    is_foreign_key: bool = Field(False, description="Flag indicating if attribute is part of foreign key")
    foreign_key_reference: Optional[str] = Field(None, description="Reference for foreign key, if applicable")
    is_unique: bool = Field(False, description="Flag indicating if attribute has unique constraint")
    default_value: Optional[Any] = Field(None, description="Default value for the attribute")
    has_index: bool = Field(False, description="Flag indicating if attribute is indexed")
    sample_values: Optional[List[Any]] = Field(None, description="Sample values for the attribute")
    business_definition: Optional[str] = Field(None, description="Business definition of the attribute")
    privacy_info: Optional[DataPrivacyInfo] = Field(None, description="Privacy information for the attribute")
    data_quality_metrics: Optional[Dict[str, Any]] = Field(None, description="Data quality metrics for the attribute")
    domain_values: Optional[List[str]] = Field(None, description="Allowed domain values, if applicable")
    comments: Optional[str] = Field(None, description="Additional comments about the attribute")


class SourceTable(BaseModel):
    """Table or entity in a source system."""
    table_id: str = Field(..., description="Unique identifier for the table")
    name: str = Field(..., description="Name of the table")
    schema_name: Optional[str] = Field(None, description="Schema name, if applicable")
    database_name: Optional[str] = Field(None, description="Database name, if applicable")
    description: Optional[str] = Field(None, description="Description of the table")
    attributes: List[SourceAttribute] = Field(default_factory=list, description="Attributes (columns) in the table")
    primary_key: Optional[List[str]] = Field(None, description="Primary key attribute names")
    record_count: Optional[int] = Field(None, description="Approximate number of records in the table")
    size_in_mb: Optional[float] = Field(None, description="Approximate size of the table in MB")
    created_date: Optional[datetime] = Field(None, description="Date when the table was created")
    last_updated_date: Optional[datetime] = Field(None, description="Date when the table was last updated")
    update_frequency: Optional[DataFrequency] = Field(None, description="Frequency of table updates")
    data_owner: Optional[str] = Field(None, description="Business owner of the data")
    technical_owner: Optional[str] = Field(None, description="Technical owner of the table")
    is_view: bool = Field(False, description="Flag indicating if this is a view rather than a table")
    view_definition: Optional[str] = Field(None, description="SQL definition if this is a view")
    privacy_info: Optional[DataPrivacyInfo] = Field(None, description="Privacy information for the table")
    retention_policy: Optional[DataRetentionPolicy] = Field(None, description="Data retention policy for the table")
    business_entity: Optional[str] = Field(None, description="Business entity represented by this table")
    related_tables: Optional[List[str]] = Field(None, description="Related tables through relationships")
    sample_query: Optional[str] = Field(None, description="Sample query to retrieve data from this table")

    def get_primary_key_attributes(self) -> List[SourceAttribute]:
        """Get the attributes that form the primary key."""
        if not self.primary_key:
            return []

        return [attr for attr in self.attributes if attr.name in self.primary_key]

    def get_attribute_by_name(self, name: str) -> Optional[SourceAttribute]:
        """Get an attribute by name."""
        for attr in self.attributes:
            if attr.name == name:
                return attr
        return None

    def get_full_table_name(self) -> str:
        """Get the fully qualified table name."""
        parts = []
        if self.database_name:
            parts.append(self.database_name)
        if self.schema_name:
            parts.append(self.schema_name)
        parts.append(self.name)
        return ".".join(parts)


class SourceDatabase(BaseModel):
    """Database in a source system."""
    database_id: str = Field(..., description="Unique identifier for the database")
    name: str = Field(..., description="Name of the database")
    description: Optional[str] = Field(None, description="Description of the database")
    database_type: DatabaseType = Field(..., description="Type of database")
    version: Optional[str] = Field(None, description="Database version")
    tables: List[SourceTable] = Field(default_factory=list, description="Tables in the database")
    schemas: Optional[List[str]] = Field(None, description="Schemas in the database")
    host: Optional[str] = Field(None, description="Database host")
    port: Optional[int] = Field(None, description="Database port")
    connection_details: Optional[Dict[str, Any]] = Field(None, description="Connection details for the database")


class SourceSystem(BaseModel):
    """Source system containing data relevant to Customer 360."""
    system_id: str = Field(..., description="Unique identifier for the source system")
    name: str = Field(..., description="Name of the source system")
    description: Optional[str] = Field(None, description="Description of the source system")
    system_type: SourceSystemType = Field(..., description="Type of source system")
    vendor: Optional[str] = Field(None, description="Vendor of the system, if applicable")
    version: Optional[str] = Field(None, description="Version of the system")
    is_active: bool = Field(True, description="Flag indicating if system is currently active")
    access_method: AccessMethod = Field(..., description="Method to access the system's data")
    data_update_frequency: DataFrequency = Field(..., description="Frequency of data updates in the system")
    data_quality_level: DataQualityLevel = Field(DataQualityLevel.MEDIUM, description="Overall data quality level")
    databases: List[SourceDatabase] = Field(default_factory=list, description="Databases in the source system")
    file_formats: Optional[List[FileFormat]] = Field(None, description="File formats for file-based systems")
    api_endpoints: Optional[List[Dict[str, Any]]] = Field(None, description="API endpoints for API-based systems")
    credentials: Optional[ConnectionCredentials] = Field(None, description="Connection credentials")
    contacts: List[ContactPerson] = Field(default_factory=list, description="Contact persons for the system")
    documentation_links: Optional[List[str]] = Field(None, description="Links to system documentation")
    data_dictionary_link: Optional[str] = Field(None, description="Link to the data dictionary")
    onboarding_date: Optional[datetime] = Field(None, description="Date when system was onboarded")
    last_profiled_date: Optional[datetime] = Field(None, description="Date when system was last profiled")
    profiling_results: Optional[Dict[str, Any]] = Field(None, description="Results of data profiling")
    notes: Optional[str] = Field(None, description="Additional notes about the system")

    def get_tables(self) -> List[SourceTable]:
        """Get all tables across all databases in the source system."""
        tables = []
        for db in self.databases:
            tables.extend(db.tables)
        return tables

    def get_table_by_name(self, name: str, schema: Optional[str] = None, database: Optional[str] = None) -> Optional[SourceTable]:
        """Get a table by name, optionally filtered by schema and database."""
        for db in self.databases:
            if database and db.name != database:
                continue

            for table in db.tables:
                if table.name == name:
                    if schema is None or table.schema_name == schema:
                        return table
        return None

    def get_primary_contact(self) -> Optional[ContactPerson]:
        """Get the primary contact person for the system."""
        for contact in self.contacts:
            if contact.is_primary:
                return contact

        # If no primary contact is explicitly marked, return the first one
        return self.contacts[0] if self.contacts else None


class SourceSystemCatalog(BaseModel):
    """Catalog of all source systems relevant to Customer 360."""
    catalog_id: str = Field(..., description="Unique identifier for the catalog")
    name: str = Field(..., description="Name of the catalog")
    description: Optional[str] = Field(None, description="Description of the catalog")
    source_systems: List[SourceSystem] = Field(..., description="Source systems in the catalog")
    created_by: Optional[str] = Field(None, description="User who created the catalog")
    created_at: Optional[datetime] = Field(None, description="Timestamp when catalog was created")
    updated_by: Optional[str] = Field(None, description="User who last updated the catalog")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when catalog was last updated")

    def get_system_by_id(self, system_id: str) -> Optional[SourceSystem]:
        """Get a source system by its ID."""
        for system in self.source_systems:
            if system.system_id == system_id:
                return system
        return None

    def get_system_by_name(self, name: str) -> Optional[SourceSystem]:
        """Get a source system by its name."""
        for system in self.source_systems:
            if system.name == name:
                return system
        return None

    def get_tables_by_system_type(self, system_type: SourceSystemType) -> List[SourceTable]:
        """Get all tables from systems of a specific type."""
        tables = []
        for system in self.source_systems:
            if system.system_type == system_type:
                tables.extend(system.get_tables())
        return tables

    def get_systems_by_type(self, system_type: SourceSystemType) -> List[SourceSystem]:
        """Get all systems of a specific type."""
        return [system for system in self.source_systems if system.system_type == system_type]

    def get_systems_summary(self) -> Dict[str, Any]:
        """Get a summary of all source systems in the catalog."""
        summary = {
            "total_systems": len(self.source_systems),
            "active_systems": sum(1 for system in self.source_systems if system.is_active),
            "system_types": {},
            "total_tables": 0,
            "total_attributes": 0
        }

        for system in self.source_systems:
            # Count by system type
            system_type = system.system_type.value
            if system_type in summary["system_types"]:
                summary["system_types"][system_type] += 1
            else:
                summary["system_types"][system_type] = 1

            # Count tables and attributes
            tables = system.get_tables()
            summary["total_tables"] += len(tables)

            for table in tables:
                summary["total_attributes"] += len(table.attributes)

        return summary


class IncrementalLoadStrategy(str, Enum):
    """Strategies for incremental data loading from source systems."""
    TIMESTAMP_BASED = "TIMESTAMP_BASED"
    SEQUENCE_BASED = "SEQUENCE_BASED"
    CHANGE_DATA_CAPTURE = "CHANGE_DATA_CAPTURE"
    WATERMARK_BASED = "WATERMARK_BASED"
    LOG_BASED = "LOG_BASED"
    DIFF_BASED = "DIFF_BASED"
    PARTITION_BASED = "PARTITION_BASED"
    TRIGGER_BASED = "TRIGGER_BASED"
    HYBRID = "HYBRID"


class DataExtractionConfig(BaseModel):
    """Configuration for extracting data from a source system."""
    config_id: str = Field(..., description="Unique identifier for the configuration")
    source_system_id: str = Field(..., description="ID of the source system")
    extraction_method: AccessMethod = Field(..., description="Method for extracting data")
    incremental_strategy: Optional[IncrementalLoadStrategy] = Field(None, description="Strategy for incremental loads")
    incremental_key: Optional[str] = Field(None, description="Key attribute for incremental loads")
    batch_size: Optional[int] = Field(None, description="Batch size for extraction, if applicable")
    parallelism: Optional[int] = Field(None, description="Degree of parallelism for extraction")
    schedule: Optional[str] = Field(None, description="Schedule expression (cron or similar)")
    extraction_window: Optional[Dict[str, Any]] = Field(None, description="Time window for extraction")
    filter_conditions: Optional[List[str]] = Field(None, description="Filter conditions for extraction")
    target_tables: Optional[List[str]] = Field(None, description="Target tables to extract")
    include_deleted: bool = Field(False, description="Flag indicating if deleted records should be included")
    retry_settings: Optional[Dict[str, Any]] = Field(None, description="Settings for retry logic")
    timeout_seconds: Optional[int] = Field(None, description="Timeout in seconds")
    created_at: Optional[datetime] = Field(None, description="When the configuration was created")
    updated_at: Optional[datetime] = Field(None, description="When the configuration was last updated")
    created_by: Optional[str] = Field(None, description="User who created the configuration")
    custom_settings: Optional[Dict[str, Any]] = Field(None, description="Custom settings specific to extraction method")

    def get_extraction_window_description(self) -> str:
        """Get a human-readable description of the extraction window."""
        if not self.extraction_window:
            return "Full extraction (no time window specified)"

        if "days_back" in self.extraction_window:
            return f"Last {self.extraction_window['days_back']} days"

        if "start_time" in self.extraction_window and "end_time" in self.extraction_window:
            return f"From {self.extraction_window['start_time']} to {self.extraction_window['end_time']}"

        return "Custom extraction window"


class DataTransformationRule(BaseModel):
    """Rule for transforming data during the mapping process."""
    rule_id: str = Field(..., description="Unique identifier for the transformation rule")
    rule_name: str = Field(..., description="Name of the transformation rule")
    description: Optional[str] = Field(None, description="Description of what the rule does")
    rule_type: str = Field(..., description="Type of transformation rule")
    source_attribute: Optional[str] = Field(None, description="Source attribute name")
    target_attribute: str = Field(..., description="Target attribute name")
    transformation_logic: str = Field(..., description="Logic or expression for the transformation")
    execution_order: int = Field(0, description="Order in which the rule should be executed")
    condition: Optional[str] = Field(None, description="Condition for when this rule should apply")
    sample_input: Optional[Any] = Field(None, description="Sample input for testing")
    sample_output: Optional[Any] = Field(None, description="Expected output for the sample input")
    is_active: bool = Field(True, description="Flag indicating if rule is active")
    created_at: Optional[datetime] = Field(None, description="When the rule was created")
    created_by: Optional[str] = Field(None, description="User who created the rule")
    version: Optional[str] = Field(None, description="Version of the rule")
    tags: Optional[List[str]] = Field(None, description="Tags for the rule")


class DataMapping(BaseModel):
    """Mapping between source and target data models."""
    mapping_id: str = Field(..., description="Unique identifier for the mapping")
    mapping_name: str = Field(..., description="Name of the mapping")
    description: Optional[str] = Field(None, description="Description of the mapping")
    source_system_id: str = Field(..., description="ID of the source system")
    source_table: str = Field(..., description="Name of the source table")
    source_schema: Optional[str] = Field(None, description="Schema of the source table, if applicable")
    source_database: Optional[str] = Field(None, description="Database of the source table, if applicable")
    target_entity: str = Field(..., description="Name of the target entity in the Customer 360 model")
    target_entity_version: Optional[str] = Field(None, description="Version of the target entity")
    mapping_type: str = Field(..., description="Type of mapping (direct, derived, etc.)")
    attribute_mappings: List[Dict[str, Any]] = Field(..., description="Attribute-level mappings")
    transformation_rules: List[DataTransformationRule] = Field(default_factory=list, description="Transformation rules")
    filter_criteria: Optional[str] = Field(None, description="Filter criteria for the mapping")
    is_active: bool = Field(True, description="Flag indicating if mapping is active")
    created_at: Optional[datetime] = Field(None, description="When the mapping was created")
    updated_at: Optional[datetime] = Field(None, description="When the mapping was last updated")
    created_by: Optional[str] = Field(None, description="User who created the mapping")
    updated_by: Optional[str] = Field(None, description="User who last updated the mapping")
    validation_status: Optional[str] = Field(None, description="Validation status of the mapping")
    validation_messages: Optional[List[str]] = Field(None, description="Validation messages")
    tags: Optional[List[str]] = Field(None, description="Tags for the mapping")
    notes: Optional[str] = Field(None, description="Additional notes about the mapping")

    def get_source_attributes(self) -> List[str]:
        """Get all source attributes used in this mapping."""
        attributes = []
        for mapping in self.attribute_mappings:
            if "source_attribute" in mapping and mapping["source_attribute"]:
                attributes.append(mapping["source_attribute"])
        return attributes

    def get_target_attributes(self) -> List[str]:
        """Get all target attributes used in this mapping."""
        return [mapping["target_attribute"] for mapping in self.attribute_mappings if "target_attribute" in mapping]

    def get_direct_mappings(self) -> List[Dict[str, Any]]:
        """Get all direct (non-transformed) mappings."""
        return [mapping for mapping in self.attribute_mappings if mapping.get("mapping_type") == "direct"]

    def get_transformed_mappings(self) -> List[Dict[str, Any]]:
        """Get all mappings that involve transformations."""
        return [mapping for mapping in self.attribute_mappings if mapping.get("mapping_type") != "direct"]


class MappingCatalog(BaseModel):
    """Catalog of all data mappings for Customer 360."""
    catalog_id: str = Field(..., description="Unique identifier for the catalog")
    name: str = Field(..., description="Name of the catalog")
    description: Optional[str] = Field(None, description="Description of the catalog")
    mappings: List[DataMapping] = Field(..., description="Data mappings in the catalog")
    source_system_catalog_id: Optional[str] = Field(None, description="ID of the associated source system catalog")
    created_at: Optional[datetime] = Field(None, description="When the catalog was created")
    updated_at: Optional[datetime] = Field(None, description="When the catalog was last updated")
    created_by: Optional[str] = Field(None, description="User who created the catalog")
    updated_by: Optional[str] = Field(None, description="User who last updated the catalog")
    version: Optional[str] = Field(None, description="Version of the catalog")
    status: Optional[str] = Field(None, description="Status of the catalog (draft, approved, etc.)")

    def get_mapping_by_id(self, mapping_id: str) -> Optional[DataMapping]:
        """Get a mapping by its ID."""
        for mapping in self.mappings:
            if mapping.mapping_id == mapping_id:
                return mapping
        return None

    def get_mappings_by_source_system(self, source_system_id: str) -> List[DataMapping]:
        """Get all mappings for a specific source system."""
        return [mapping for mapping in self.mappings if mapping.source_system_id == source_system_id]

    def get_mappings_by_target_entity(self, target_entity: str) -> List[DataMapping]:
        """Get all mappings for a specific target entity."""
        return [mapping for mapping in self.mappings if mapping.target_entity == target_entity]

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the mapping catalog."""
        source_systems = set()
        target_entities = set()
        active_mappings = 0

        for mapping in self.mappings:
            source_systems.add(mapping.source_system_id)
            target_entities.add(mapping.target_entity)
            if mapping.is_active:
                active_mappings += 1

        return {
            "total_mappings": len(self.mappings),
            "active_mappings": active_mappings,
            "source_system_count": len(source_systems),
            "target_entity_count": len(target_entities),
            "updated_at": self.updated_at,
            "status": self.status
        }
