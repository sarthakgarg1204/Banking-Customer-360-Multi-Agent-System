"""
Mapping Prompts

This module contains prompt templates for the Mapping Agent to generate source-to-target
mappings for Customer 360 data products in retail banking.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class AttributeMapping(BaseModel):
    """Model representing a mapping between source and target attributes."""
    source_system: str = Field(..., description="Source system name")
    source_table: str = Field(..., description="Source table name")
    source_attribute: str = Field(..., description="Source attribute name")
    target_entity: str = Field(..., description="Target entity name")
    target_attribute: str = Field(..., description="Target attribute name")
    mapping_type: str = Field(..., description="Type of mapping (direct, transformed, derived, etc.)")
    transformation_rule: Optional[str] = Field(None, description="Transformation rule if applicable")
    condition: Optional[str] = Field(None, description="Condition for applying this mapping")
    priority: int = Field(1, description="Priority of this mapping when multiple sources exist")
    data_quality_threshold: Optional[float] = Field(None, description="Minimum data quality score required")
    notes: Optional[str] = Field(None, description="Additional notes about the mapping")


class EntityMapping(BaseModel):
    """Model representing a mapping between source tables and target entities."""
    target_entity: str = Field(..., description="Target entity name")
    source_systems: List[Dict[str, Any]] = Field(..., description="Source systems and tables")
    attribute_mappings: List[AttributeMapping] = Field(..., description="Attribute-level mappings")
    filter_conditions: Optional[Dict[str, str]] = Field(None, description="Filter conditions for source data")
    join_conditions: Optional[Dict[str, str]] = Field(None, description="Join conditions between source tables")
    update_strategy: str = Field(..., description="Strategy for updating the entity (merge, overwrite, etc.)")
    notes: Optional[str] = Field(None, description="Additional notes about the entity mapping")


# Prompt to analyze source systems and target model for mapping
ANALYZE_FOR_MAPPING_PROMPT = """
You are an expert data integration specialist focused on banking data.
Analyze the source systems and target data model to identify mapping opportunities and challenges.

Source Systems:
{source_systems_json}

Target Data Model:
{target_data_model_json}

Provide a comprehensive analysis with the following sections:

1. Source System Assessment
   - Evaluate each source system for data completeness
   - Identify systems of record for key data domains
   - Note data quality concerns in source systems
   - Highlight potential conflicts between sources
   - Document update frequencies and timing considerations

2. Attribute Coverage Analysis
   - For each target entity, assess attribute coverage from available sources
   - Identify attributes with multiple potential sources
   - Flag attributes with no clear source
   - Note attributes requiring transformation or derivation
   - Highlight critical path dependencies

3. Data Type Compatibility
   - Identify data type mismatches between sources and targets
   - Note format standardization needs
   - Highlight precision or scale issues
   - Document character set or encoding challenges

4. Data Transformation Needs
   - Catalog required transformations by complexity
   - Identify needed lookup operations or reference data
   - Document complex business rules requiring implementation
   - Note aggregation requirements
   - Highlight conditional logic needs

5. Incremental Update Considerations
   - Analyze change data capture capabilities of sources
   - Identify reliable timestamp or sequence columns
   - Document potential update conflict scenarios
   - Note history preservation requirements

6. Critical Challenges and Recommendations
   - Summarize the most significant mapping challenges
   - Recommend strategies for addressing gaps
   - Suggest prioritization approach
   - Outline any needed source system improvements

Format your response as a structured markdown document with clear sections and subsections.
Focus on providing actionable insights that will guide the detailed mapping design.
"""


# Prompt to generate entity-level mapping specification
GENERATE_ENTITY_MAPPING_PROMPT = """
You are an expert data integration specialist focused on banking data.
Generate a detailed mapping specification for the {target_entity} entity in the Customer 360 data model.

Source Systems Information:
{source_systems_json}

Target Entity Structure:
{target_entity_json}

Mapping Analysis:
{mapping_analysis}

Create a comprehensive entity mapping specification with:

1. Overview
   - Target entity purpose and context
   - Key business requirements driving this entity
   - Overall mapping strategy for this entity
   - Critical success factors

2. Source System Selection
   - Primary source systems for this entity
   - System of record designations by attribute group
   - Rationale for source system selections
   - Source data retrieval approach (full extract vs. incremental)

3. Detailed Attribute Mappings
   - For each target attribute:
     * Source system, table, and attribute
     * Mapping type (direct, transformed, derived, etc.)
     * Transformation logic when applicable
     * Handling of NULL values
     * Data type conversions
     * Business rules to apply
     * Validation requirements

4. Data Quality Controls
   - Quality thresholds for accepting source data
   - Fallback strategies for quality failures
   - Validation rules to apply during mapping
   - Error handling procedures

5. Special Considerations
   - Handling of history and temporal data
   - Record survivorship rules for conflicts
   - Performance optimization strategies
   - Privacy and security handling

Format your response as a structured JSON document following the EntityMapping model.
Include detailed notes and explanations for complex mapping decisions.
"""


# Prompt to generate transformation rules for complex mappings
GENERATE_TRANSFORMATION_RULES_PROMPT = """
You are an expert in data transformation and integration for banking systems.
Create detailed transformation rules for complex mappings identified for the Customer 360 data product.

Complex Mapping Requirements:
{complex_mapping_requirements}

For each complex transformation, generate:

1. Transformation Specification
   - Unique identifier for the transformation
   - Clear, descriptive name
   - Detailed explanation of the transformation purpose
   - Source and target context

2. Business Logic
   - Step-by-step logic flow
   - Decision points and conditional paths
   - Edge case handling
   - Validation rules

3. Implementation Details
   - Pseudo-code or SQL implementation
   - Required functions or procedures
   - Performance considerations
   - Dependencies on other transformations

4. Testing Approach
   - Test cases covering standard scenarios
   - Edge case test scenarios
   - Expected outcomes for verification
   - Validation queries

Format your response as a structured JSON document that can be used directly in ETL/ELT processes.
Include detailed documentation for each transformation to enable implementation by data engineers.
"""


# Prompt to generate SQL/code for implementing mappings
GENERATE_IMPLEMENTATION_CODE_PROMPT = """
You are an expert data engineer specializing in ETL/ELT implementations for banking data.
Create implementation code for the following entity mappings:

Entity Mapping Specification:
{entity_mapping_json}

Target Platform: {target_platform}

Please generate code to implement these mappings with:

1. Source Data Extraction
   - SQL queries or API calls to retrieve source data
   - Filtering conditions to apply during extraction
   - Join logic for multi-table sources
   - Error handling for extraction failures

2. Transformation Logic
   - Implementation of all transformation rules
   - Handling of NULL values and defaults
   - Data type conversions
   - Implementation of complex business rules

3. Loading Process
   - Target table creation/modification scripts
   - Data loading procedures
   - Update/merge strategy implementation
   - Error handling and logging

4. Quality Validation
   - Post-load validation queries
   - Data quality checks
   - Reconciliation with source data

Format your response with clearly commented code sections.
Ensure the implementation follows best practices for the target platform.
Include any initialization or setup code required.
"""


# Prompt to generate data lineage documentation
GENERATE_DATA_LINEAGE_PROMPT = """
You are a data governance specialist with expertise in data lineage documentation.
Create comprehensive data lineage documentation for the following Customer 360 entity:

Entity Mapping:
{entity_mapping_json}

Generate detailed data lineage documentation with:

1. Visual Lineage Representation
   - Source-to-target flow diagram (in mermaid notation)
   - Transformation points highlighted
   - Critical path identification

2. Attribute-Level Lineage
   - For each target attribute:
     * Complete lineage chain from origin to target
     * Intermediate transformations
     * Dependency graph

3. Process Lineage
   - ETL/ELT process dependencies
   - Execution sequence requirements
   - Timing constraints

4. Governance Metadata
   - Data stewardship assignments
   - Regulatory relevance
   - Privacy classifications
   - Retention requirements

5. Impact Analysis
   - Upstream dependency analysis
   - Downstream impact assessment
   - Change management considerations

Format your response as a structured markdown document with clear sections.
Include mermaid diagrams where appropriate for visual representation.
Ensure documentation is detailed enough for both technical and business stakeholders.
"""


class MappingAgent:
    """Main class for the Mapping Agent that orchestrates the mapping process."""

    def __init__(self, target_platform="snowflake"):
        """Initialize the Mapping Agent.

        Args:
            target_platform (str): Target platform for implementation code generation.
        """
        self.target_platform = target_platform
        # Add LLM and other dependencies initialization here

    def analyze_for_mapping(self, source_systems_json, target_data_model_json):
        """Analyze source systems and target model to identify mapping opportunities and challenges.

        Args:
            source_systems_json (str): JSON representation of source systems
            target_data_model_json (str): JSON representation of target data model

        Returns:
            str: Comprehensive mapping analysis
        """
        # Implement LLM call with ANALYZE_FOR_MAPPING_PROMPT
        prompt = ANALYZE_FOR_MAPPING_PROMPT.format(
            source_systems_json=source_systems_json,
            target_data_model_json=target_data_model_json
        )
        # Return LLM response
        pass

    def generate_entity_mapping(self, target_entity, source_systems_json, target_entity_json, mapping_analysis):
        """Generate entity-level mapping specification.

        Args:
            target_entity (str): Target entity name
            source_systems_json (str): JSON representation of source systems
            target_entity_json (str): JSON representation of target entity
            mapping_analysis (str): Analysis of mapping opportunities

        Returns:
            EntityMapping: Entity mapping specification
        """
        # Implement LLM call with GENERATE_ENTITY_MAPPING_PROMPT
        prompt = GENERATE_ENTITY_MAPPING_PROMPT.format(
            target_entity=target_entity,
            source_systems_json=source_systems_json,
            target_entity_json=target_entity_json,
            mapping_analysis=mapping_analysis
        )
        # Parse LLM response into EntityMapping model
        pass

    def generate_transformation_rules(self, complex_mapping_requirements):
        """Generate detailed transformation rules for complex mappings.

        Args:
            complex_mapping_requirements (str): Requirements for complex mappings

        Returns:
            dict: Detailed transformation rules
        """
        # Implement LLM call with GENERATE_TRANSFORMATION_RULES_PROMPT
        prompt = GENERATE_TRANSFORMATION_RULES_PROMPT.format(
            complex_mapping_requirements=complex_mapping_requirements
        )
        # Parse LLM response into transformation rules
        pass

    def generate_implementation_code(self, entity_mapping_json):
        """Generate implementation code for entity mappings.

        Args:
            entity_mapping_json (str): JSON representation of entity mapping

        Returns:
            str: Implementation code for the mappings
        """
        # Implement LLM call with GENERATE_IMPLEMENTATION_CODE_PROMPT
        prompt = GENERATE_IMPLEMENTATION_CODE_PROMPT.format(
            entity_mapping_json=entity_mapping_json,
            target_platform=self.target_platform
        )
        # Return LLM response
        pass

    def generate_data_lineage(self, entity_mapping_json):
        """Generate data lineage documentation for an entity.

        Args:
            entity_mapping_json (str): JSON representation of entity mapping

        Returns:
            str: Data lineage documentation
        """
        # Implement LLM call with GENERATE_DATA_LINEAGE_PROMPT
        prompt = GENERATE_DATA_LINEAGE_PROMPT.format(
            entity_mapping_json=entity_mapping_json
        )
        # Return LLM response
        pass

    def process_entity(self, target_entity, source_systems_json, target_data_model_json):
        """Process a target entity to generate complete mapping artifacts.

        Args:
            target_entity (str): Target entity name
            source_systems_json (str): JSON representation of source systems
            target_data_model_json (str): JSON representation of target data model

        Returns:
            dict: Complete mapping artifacts for the entity
        """
        # Extract target entity json from target data model
        target_entity_json = self._extract_target_entity(target_entity, target_data_model_json)

        # Generate mapping analysis
        mapping_analysis = self.analyze_for_mapping(source_systems_json, target_data_model_json)

        # Generate entity mapping
        entity_mapping = self.generate_entity_mapping(
            target_entity, source_systems_json, target_entity_json, mapping_analysis
        )

        # Identify complex mappings
        complex_mappings = self._identify_complex_mappings(entity_mapping)

        # Generate transformation rules for complex mappings
        transformation_rules = None
        if complex_mappings:
            transformation_rules = self.generate_transformation_rules(complex_mappings)

        # Generate implementation code
        implementation_code = self.generate_implementation_code(entity_mapping.json())

        # Generate data lineage
        data_lineage = self.generate_data_lineage(entity_mapping.json())

        # Return all artifacts
        return {
            "entity_mapping": entity_mapping,
            "transformation_rules": transformation_rules,
            "implementation_code": implementation_code,
            "data_lineage": data_lineage
        }

    def _extract_target_entity(self, target_entity, target_data_model_json):
        """Extract target entity JSON from target data model.

        Args:
            target_entity (str): Target entity name
            target_data_model_json (str): JSON representation of target data model

        Returns:
            str: JSON representation of target entity
        """
        # Implementation to extract specific entity from data model
        pass

    def _identify_complex_mappings(self, entity_mapping):
        """Identify complex mappings that require detailed transformation rules.

        Args:
            entity_mapping (EntityMapping): Entity mapping specification

        Returns:
            str: JSON representation of complex mapping requirements
        """
        # Implementation to identify complex mappings
        complex_mappings = []

        for mapping in entity_mapping.attribute_mappings:
            if mapping.mapping_type in ["transformed", "derived", "aggregated", "conditional"]:
                complex_mappings.append(mapping)

        # Format complex mappings as requirements
        return self._format_complex_mapping_requirements(complex_mappings)

    def _format_complex_mapping_requirements(self, complex_mappings):
        """Format complex mappings as requirements for transformation rule generation.

        Args:
            complex_mappings (List[AttributeMapping]): Complex attribute mappings

        Returns:
            str: Formatted complex mapping requirements
        """
        # Implementation to format complex mappings
        pass


# Example usage
if __name__ == "__main__":
    # Sample source systems and target data model
    source_systems_json = """
    {
        "systems": [
            {
                "name": "Core Banking System",
                "tables": [
                    {
                        "name": "CUSTOMER",
                        "attributes": [
                            {
                                "name": "CUST_ID",
                                "data_type": "VARCHAR(20)",
                                "description": "Unique customer identifier",
                                "primary_key": true
                            },
                            {
                                "name": "CUST_FIRST_NAME",
                                "data_type": "VARCHAR(50)",
                                "description": "Customer first name"
                            },
                            {
                                "name": "CUST_LAST_NAME",
                                "data_type": "VARCHAR(50)",
                                "description": "Customer last name"
                            },
                            {
                                "name": "CUST_DOB",
                                "data_type": "VARCHAR(8)",
                                "description": "Customer date of birth in YYYYMMDD format"
                            },
                            {
                                "name": "CUST_GENDER",
                                "data_type": "CHAR(1)",
                                "description": "Customer gender code (M/F/O)"
                            },
                            {
                                "name": "CUST_STATUS",
                                "data_type": "CHAR(1)",
                                "description": "Customer status (A=Active, I=Inactive, C=Closed)"
                            }
                        ]
                    },
                    {
                        "name": "CUSTOMER_ADDRESS",
                        "attributes": [
                            {
                                "name": "CUST_ID",
                                "data_type": "VARCHAR(20)",
                                "description": "Customer identifier",
                                "foreign_key": "CUSTOMER.CUST_ID"
                            },
                            {
                                "name": "ADDR_TYPE",
                                "data_type": "CHAR(1)",
                                "description": "Address type (H=Home, W=Work, M=Mailing)"
                            },
                            {
                                "name": "ADDR_LINE_1",
                                "data_type": "VARCHAR(100)",
                                "description": "Address line 1"
                            },
                            {
                                "name": "ADDR_LINE_2",
                                "data_type": "VARCHAR(100)",
                                "description": "Address line 2"
                            },
                            {
                                "name": "CITY",
                                "data_type": "VARCHAR(50)",
                                "description": "City"
                            },
                            {
                                "name": "STATE",
                                "data_type": "CHAR(2)",
                                "description": "State code"
                            },
                            {
                                "name": "ZIP",
                                "data_type": "VARCHAR(10)",
                                "description": "ZIP code"
                            },
                            {
                                "name": "COUNTRY",
                                "data_type": "CHAR(3)",
                                "description": "Country code (ISO)"
                            }
                        ]
                    }
                ]
            },
            {
                "name": "CRM System",
                "tables": [
                    {
                        "name": "CUSTOMER_PROFILE",
                        "attributes": [
                            {
                                "name": "CUSTOMER_ID",
                                "data_type": "VARCHAR(20)",
                                "description": "Unique customer identifier",
                                "primary_key": true
                            },
                            {
                                "name": "FIRST_NAME",
                                "data_type": "VARCHAR(50)",
                                "description": "Customer first name"
                            },
                            {
                                "name": "LAST_NAME",
                                "data_type": "VARCHAR(50)",
                                "description": "Customer last name"
                            },
                            {
                                "name": "EMAIL",
                                "data_type": "VARCHAR(100)",
                                "description": "Customer email address"
                            },
                            {
                                "name": "PHONE",
                                "data_type": "VARCHAR(20)",
                                "description": "Customer phone number"
                            },
                            {
                                "name": "SEGMENT",
                                "data_type": "VARCHAR(20)",
                                "description": "Customer segment (Mass, Affluent, High Net Worth)"
                            },
                            {
                                "name": "LAST_CONTACT_DATE",
                                "data_type": "DATE",
                                "description": "Date of last customer contact"
                            },
                            {
                                "name": "PREFERRED_CHANNEL",
                                "data_type": "VARCHAR(10)",
                                "description": "Preferred contact channel (Email, Phone, Mail, Branch)"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    """

    target_data_model_json = """
    {
        "entities": [
            {
                "name": "CustomerProfile",
                "description": "Core customer profile information",
                "attributes": [
                    {
                        "name": "customerId",
                        "data_type": "STRING",
                        "description": "Unique customer identifier",
                        "primary_key": true
                    },
                    {
                        "name": "firstName",
                        "data_type": "STRING",
                        "description": "Customer first name"
                    },
                    {
                        "name": "lastName",
                        "data_type": "STRING",
                        "description": "Customer last name"
                    },
                    {
                        "name": "fullName",
                        "data_type": "STRING",
                        "description": "Customer full name (derived)"
                    },
                    {
                        "name": "dateOfBirth",
                        "data_type": "DATE",
                        "description": "Customer date of birth"
                    },
                    {
                        "name": "gender",
                        "data_type": "STRING",
                        "description": "Customer gender"
                    },
                    {
                        "name": "email",
                        "data_type": "STRING",
                        "description": "Customer email address"
                    },
                    {
                        "name": "phone",
                        "data_type": "STRING",
                        "description": "Customer phone number"
                    },
                    {
                        "name": "customerStatus",
                        "data_type": "STRING",
                        "description": "Customer status"
                    },
                    {
                        "name": "customerSegment",
                        "data_type": "STRING",
                        "description": "Customer segment"
                    },
                    {
                        "name": "preferredContactMethod",
                        "data_type": "STRING",
                        "description": "Preferred contact method"
                    },
                    {
                        "name": "lastContactDate",
                        "data_type": "DATE",
                        "description": "Date of last contact"
                    },
                    {
                        "name": "customerAge",
                        "data_type": "INTEGER",
                        "description": "Customer age (derived)"
                    }
                ]
            },
            {
                "name": "CustomerAddress",
                "description": "Customer address information",
                "attributes": [
                    {
                        "name": "addressId",
                        "data_type": "STRING",
                        "description": "Unique address identifier",
                        "primary_key": true
                    },
                    {
                        "name": "customerId",
                        "data_type": "STRING",
                        "description": "Customer identifier",
                        "foreign_key": "CustomerProfile.customerId"
                    },
                    {
                        "name": "addressType",
                        "data_type": "STRING",
                        "description": "Address type"
                    },
                    {
                        "name": "addressLine1",
                        "data_type": "STRING",
                        "description": "Address line 1"
                    },
                    {
                        "name": "addressLine2",
                        "data_type": "STRING",
                        "description": "Address line 2"
                    },
                    {
                        "name": "city",
                        "data_type": "STRING",
                        "description": "City"
                    },
                    {
                        "name": "state",
                        "data_type": "STRING",
                        "description": "State"
                    },
                    {
                        "name": "zipCode",
                        "data_type": "STRING",
                        "description": "ZIP code"
                    },
                    {
                        "name": "country",
                        "data_type": "STRING",
                        "description": "Country"
                    },
                    {
                        "name": "formattedAddress",
                        "data_type": "STRING",
                        "description": "Formatted full address (derived)"
                    },
                    {
                        "name": "isPrimary",
                        "data_type": "BOOLEAN",
                        "description": "Indicates if this is the primary address"
                    }
                ]
            }
        ]
    }
    """

    # Create mapping agent
    mapping_agent = MappingAgent()

    # Process CustomerProfile entity
    customer_profile_artifacts = mapping_agent.process_entity(
        "CustomerProfile",
        source_systems_json,
        target_data_model_json
    )

    # Print artifacts
    print(customer_profile_artifacts)
