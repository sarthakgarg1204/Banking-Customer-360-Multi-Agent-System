"""
Data Designer Prompts

This module contains prompt templates for the Data Designer Agent to recommend
optimal data structures for Customer 360 data products in retail banking.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class EntityAttribute(BaseModel):
    """Model representing an attribute in a data entity."""
    name: str = Field(..., description="Name of the attribute")
    description: str = Field(..., description="Description of the attribute")
    data_type: str = Field(..., description="Data type of the attribute")
    is_required: bool = Field(False, description="Whether the attribute is required")
    is_pii: bool = Field(False, description="Whether the attribute contains PII")
    is_sensitive: bool = Field(False, description="Whether the attribute contains sensitive data")
    source_type: str = Field(..., description="Type of source (derived, direct, reference)")
    domain_values: Optional[List[str]] = Field(None, description="Allowed domain values if applicable")
    business_rules: Optional[List[str]] = Field(None, description="Business rules for the attribute")


class DataEntity(BaseModel):
    """Model representing a data entity in the Customer 360 model."""
    name: str = Field(..., description="Name of the entity")
    description: str = Field(..., description="Description of the entity")
    entity_type: str = Field(..., description="Type of entity (core, reference, transaction, etc.)")
    attributes: List[EntityAttribute] = Field(default_factory=list, description="Attributes in the entity")
    relationships: List[Dict[str, Any]] = Field(default_factory=list, description="Relationships to other entities")
    update_frequency: str = Field(..., description="Frequency of updates to this entity")
    business_owner: Optional[str] = Field(None, description="Business owner of the entity")
    data_steward: Optional[str] = Field(None, description="Data steward responsible for the entity")


class DataModel(BaseModel):
    """Model representing a complete data model for Customer 360."""
    model_name: str = Field(..., description="Name of the data model")
    description: str = Field(..., description="Description of the data model")
    version: str = Field(..., description="Version of the data model")
    entities: List[DataEntity] = Field(default_factory=list, description="Entities in the data model")
    created_by: str = Field(..., description="Creator of the data model")
    created_at: str = Field(..., description="Creation timestamp")


# Prompt to design a Customer 360 data model based on business requirements
DESIGN_CUSTOMER_360_MODEL_PROMPT = """
You are an expert data architect specializing in Customer 360 data models for retail banking.
Based on the provided business requirements, design an optimal data model for a Customer 360 data product.

Business Requirements:
{business_requirements}

Create a comprehensive data model with the following components:

1. Core Customer Entity
   - Define all essential customer attributes
   - Identify unique customer identifiers
   - Specify demographic and profile attributes
   - Include customer segmentation attributes
   - Add relationship attributes (households, related parties)
   - Define derived metrics and scores
   - Specify privacy and security classifications

2. Related Entities
   - Account information entities
   - Transaction history entities
   - Product ownership entities
   - Customer interaction entities
   - Customer preference entities
   - Risk and compliance entities
   - External data integration entities

3. For each entity:
   - Provide a clear name and description
   - Define the entity type (core, reference, transaction, etc.)
   - List all relevant attributes with data types
   - Specify relationships to other entities
   - Indicate update frequency
   - Note any special considerations

4. Data Model Architecture
   - Recommend an appropriate technical architecture (relational, document, graph, hybrid)
   - Suggest partitioning or sharding strategies if needed
   - Address historical data management
   - Consider data versioning requirements
   - Propose indexing strategies for common query patterns

5. Data Governance Considerations
   - Identify PII and sensitive attributes
   - Recommend data masking or encryption needs
   - Suggest retention policies
   - Outline lineage tracking requirements
   - Address data quality rules

Format your response as a structured JSON document describing the recommended data model.
Use industry best practices for retail banking data modeling and ensure the model supports all specified business requirements.
"""


# Prompt to refine a data model based on available source systems
REFINE_DATA_MODEL_PROMPT = """
You are an expert data architect specializing in Customer 360 data models for retail banking.
You've designed an initial data model, but now need to refine it based on available source systems.

Initial Data Model:
{initial_data_model_json}

Available Source Systems:
{source_systems_json}

Refine the data model with the following considerations:

1. Attribute Availability
   - Identify which attributes can be sourced directly
   - Flag attributes that may require derivation or alternative sources
   - Suggest modifications based on available data

2. Data Quality Considerations
   - Note attributes with potential quality issues
   - Recommend data quality rules or transformations
   - Suggest fallback strategies for low-quality data

3. Entity Completion
   - Assess completeness of each entity based on available sources
   - Identify gaps where source data may be insufficient
   - Suggest additional sources or derived attributes to fill gaps

4. Technical Feasibility
   - Assess feasibility of the proposed architecture given the sources
   - Recommend adjustments to accommodate source system constraints
   - Address integration challenges for diverse source systems

5. Implementation Phasing
   - Suggest a phased approach based on source system priorities
   - Identify quick wins with readily available high-quality data
   - Outline longer-term enhancements requiring additional work

Format your response as a structured JSON document describing the refined data model.
Include clear notations about changes made from the initial model and rationales for those changes.
"""


# Prompt to design domain-specific data structures
DESIGN_DOMAIN_MODEL_PROMPT = """
You are an expert data architect specializing in Customer 360 data models for retail banking.
Design a detailed data structure for the {domain_name} domain within the Customer 360 data product.

Business Context:
{business_context}

Design a comprehensive data structure for this domain with:

1. Key Entities
   - Core domain entities with clear descriptions
   - Entity relationships and cardinality
   - Entity hierarchies if applicable

2. Detailed Attributes
   - Essential attributes for each entity
   - Data types and formats
   - Business definitions
   - Default values if applicable
   - Constraints and validation rules
   - Derived attributes with calculation logic

3. Business Rules
   - Domain-specific business rules
   - Calculation methodologies
   - Aggregation requirements
   - Temporal considerations (effective dating, etc.)

4. Integration Points
   - Relationships to other domains
   - External reference data requirements
   - API considerations

5. Analytical Capabilities
   - Key metrics and KPIs
   - Aggregation dimensions
   - Common analytical patterns

6. Governance Requirements
   - Privacy classifications
   - Retention requirements
   - Masking or encryption needs
   - Audit requirements

Format your response as a structured JSON document describing the domain data model.
Ensure the design aligns with banking industry best practices and supports the specified business context.
"""


# Prompt to generate data dictionary for the designed model
GENERATE_DATA_DICTIONARY_PROMPT = """
You are an expert data architect specializing in Customer 360 data models for retail banking.
Create a comprehensive data dictionary for the designed Customer 360 data model.

Data Model:
{data_model_json}

Generate a complete data dictionary with the following details for each attribute:

1. Basic Information
   - Attribute name (technical name)
   - Business name (friendly name)
   - Parent entity
   - Detailed description
   - Data type and format
   - Required/Optional status

2. Technical Details
   - Primary key status
   - Foreign key relationships
   - Default values
   - Valid ranges or constraints
   - Uniqueness constraints
   - Indexing recommendations

3. Business Context
   - Business definition
   - Calculation logic (if derived)
   - Business rules
   - Domain values and meanings
   - Examples of valid values
   - Usage context

4. Governance Information
   - Data owner
   - Data steward
   - PII classification
   - Sensitivity classification
   - Masking requirements
   - Retention period
   - Regulatory relevance

5. Source Information
   - Originating system
   - Update frequency
   - Transformation rules
   - Quality metrics
   - Lineage information

Format your response as a structured markdown document with clear organization by entity.
Use tables, headings, and formatting to make the dictionary accessible and useful for both technical and business users.
"""


# Prompt to generate physical implementation recommendations
GENERATE_IMPLEMENTATION_RECOMMENDATIONS_PROMPT = """
You are an expert data architect specializing in Customer 360 data models for retail banking.
Provide detailed technical implementation recommendations for the designed Customer 360 data model.

Data Model:
{data_model_json}

Target Environment:
{target_environment}

Generate comprehensive implementation recommendations covering:

1. Storage Technology Selection
   - Recommended database platforms with rationale
   - Storage distribution strategies
   - Partitioning and sharding approaches
   - Considerations for different entity types

2. Physical Schema Design
   - Table design recommendations
   - Indexing strategy
   - Materialized view recommendations
   - Denormalization considerations
   - Time-based partitioning strategy

3. Performance Optimization
   - Caching recommendations
   - Query optimization strategies
   - Data distribution for parallel processing
   - Batch vs. real-time processing considerations

4. Data Access Patterns
   - API design recommendations
   - Query patterns to optimize for
   - Data virtualization considerations
   - Service layer recommendations

5. Security Implementation
   - Encryption recommendations
   - Access control implementation
   - Data masking strategies
   - Audit logging implementation

6. Operational Considerations
   - Backup and recovery strategy
   - High availability configuration
   - Monitoring recommendations
   - Disaster recovery approach

Format your response as a structured technical document with clear sections, diagrams (described textually), and implementation guidelines.
Include specific technology recommendations where appropriate, with alternatives and trade-offs clearly explained.
"""


def generate_design_model_prompt(business_requirements: str) -> str:
    """Generate a prompt to design a Customer 360 data model."""
    return DESIGN_CUSTOMER_360_MODEL_PROMPT.format(
        business_requirements=business_requirements
    )


def generate_refine_model_prompt(initial_data_model_json: str, source_systems_json: str) -> str:
    """Generate a prompt to refine a data model based on source systems."""
    return REFINE_DATA_MODEL_PROMPT.format(
        initial_data_model_json=initial_data_model_json,
        source_systems_json=source_systems_json
    )


def generate_domain_model_prompt(domain_name: str, business_context: str) -> str:
    """Generate a prompt to design a domain-specific data model."""
    return DESIGN_DOMAIN_MODEL_PROMPT.format(
        domain_name=domain_name,
        business_context=business_context
    )


def generate_data_dictionary_prompt(data_model_json: str) -> str:
    """Generate a prompt to create a data dictionary for a data model."""
    return GENERATE_DATA_DICTIONARY_PROMPT.format(
        data_model_json=data_model_json
    )


def generate_implementation_recommendations_prompt(data_model_json: str, target_environment: str) -> str:
    """Generate a prompt for implementation recommendations."""
    return GENERATE_IMPLEMENTATION_RECOMMENDATIONS_PROMPT.format(
        data_model_json=data_model_json,
        target_environment=target_environment
    )


# Additional specialized prompts for banking data models

CUSTOMER_PROFILE_ENTITY_DESIGN_PROMPT = """
You are a banking data architect specializing in retail customer data.
Design a comprehensive Customer Profile entity for a retail banking Customer 360 data product.

Business Requirements:
{business_requirements}

Design a detailed Customer Profile entity with:

1. Core Identifiers
   - Primary customer identifier
   - Source system identifiers
   - External identifiers (tax ID, national ID, etc.)
   - Digital identifiers (online/mobile banking)

2. Demographic Attributes
   - Personal information (name, date of birth, etc.)
   - Contact information (address, phone, email, etc.)
   - Employment information
   - Household information
   - Lifecycle information

3. Banking Relationship Attributes
   - Customer status (active, dormant, closed)
   - Customer since date
   - Relationship manager assignment
   - Service tier or segment
   - Channel preferences
   - Marketing preferences

4. Risk and Compliance Attributes
   - KYC status
   - Risk rating
   - Compliance flags
   - Regulatory classifications

5. Derived Metrics
   - Customer lifetime value
   - Profitability metrics
   - Engagement scores
   - Propensity scores
   - Churn risk indicators

6. Relationship Links
   - Household relationships
   - Business relationships
   - Authorized users and powers of attorney
   - Beneficiary relationships

For each attribute, include:
- Technical name
- Business definition
- Data type
- Sample values
- Privacy classification
- Source considerations
- Update frequency

Format your response as a structured entity specification document.
"""


ACCOUNT_ENTITY_DESIGN_PROMPT = """
You are a banking data architect specializing in retail banking.
Design comprehensive Account entities for a retail banking Customer 360 data product.

Business Requirements:
{business_requirements}

Design detailed Account entities with:

1. Account Types to Consider
   - Deposit accounts (checking, savings)
   - Loan accounts (mortgage, personal loans, lines of credit)
   - Investment accounts
   - Credit card accounts
   - Insurance products

2. Core Account Attributes
   - Account identifiers
   - Account type and subtype
   - Open and close dates
   - Status information
   - Ownership structure
   - Branch/channel of origination
   - Terms and conditions references

3. Financial Attributes
   - Balance information (current, available, etc.)
   - Credit limits
   - Interest rates
   - Payment information
   - Foreign currency details if applicable

4. Risk Attributes
   - Risk ratings
   - Delinquency information
   - Collections status
   - Credit score at origination
   - Collateral information if applicable

5. Service Attributes
   - Fee package information
   - Service level agreements
   - Feature enrollments
   - Statement preferences
   - Alert configurations

6. Relationship Attributes
   - Primary and joint owners
   - Authorized users
   - Relationship to other accounts
   - Household association

For each entity and attribute, include:
- Technical name
- Business definition
- Data type
- Sample values
- Privacy classification
- Source considerations
- Update frequency

Format your response as a structured entity specification document.
"""


TRANSACTION_ENTITY_DESIGN_PROMPT = """
You are a banking data architect specializing in retail banking.
Design comprehensive Transaction entities for a retail banking Customer 360 data product.

Business Requirements:
{business_requirements}

Design detailed Transaction entities with:

1. Transaction Types to Consider
   - Account deposits and withdrawals
   - Payments (bill payments, P2P, wire transfers)
   - Purchases (POS, online)
   - ATM transactions
   - Fee assessments
   - Interest postings
   - Loan disbursements and payments
   - Investment transactions

2. Core Transaction Attributes
   - Transaction identifiers
   - Transaction type and subtype
   - Transaction date and time
   - Posting date
   - Amount and currency
   - Source and destination accounts
   - Transaction status

3. Contextual Attributes
   - Channel of transaction
   - Location information
   - Device information
   - Merchant details
   - Reference numbers
   - Batch identifiers

4. Categorization Attributes
   - Transaction category
   - Purpose codes
   - MCC codes for card transactions
   - Internal classification
   - Customer-assigned categories

5. Risk and Compliance Attributes
   - Risk flags
   - Fraud indicators
   - AML screening results
   - Override information
   - Authorization details

6. Analytical Attributes
   - Running balances
   - Impact on available funds
   - Statement cycle assignment
   - Aggregation indicators

For each entity and attribute, include:
- Technical name
- Business definition
- Data type
- Sample values
- Privacy classification
- Source considerations
- Update frequency

Format your response as a structured entity specification document.
"""
