"""
Use Case Prompts

This module contains prompt templates for the Use Case Agent to interpret business requirements
and generate structured specifications for Customer 360 data products.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class BusinessRequirement(BaseModel):
    """Model representing a parsed business requirement."""
    requirement_id: str = Field(..., description="Unique identifier for the requirement")
    description: str = Field(..., description="Full text description of the requirement")
    category: str = Field(..., description="Category of the requirement (marketing, risk, etc.)")
    priority: str = Field(..., description="Priority level (high, medium, low)")
    stakeholders: List[str] = Field(default_factory=list, description="Stakeholders for this requirement")
    data_needs: List[str] = Field(default_factory=list, description="Data elements needed to satisfy requirement")
    metrics: List[str] = Field(default_factory=list, description="Metrics or KPIs associated with requirement")
    source: str = Field(..., description="Source of the requirement (document, interview, etc.)")


class BusinessUseCase(BaseModel):
    """Model representing a business use case extracted from requirements."""
    use_case_id: str = Field(..., description="Unique identifier for the use case")
    name: str = Field(..., description="Name of the use case")
    description: str = Field(..., description="Description of the use case")
    business_objective: str = Field(..., description="Primary business objective")
    requirements: List[BusinessRequirement] = Field(default_factory=list, description="Related requirements")
    success_criteria: List[str] = Field(default_factory=list, description="Success criteria for the use case")
    data_categories: List[str] = Field(default_factory=list, description="Categories of data needed")
    primary_stakeholders: List[str] = Field(default_factory=list, description="Primary stakeholders")
    expected_benefits: List[str] = Field(default_factory=list, description="Expected business benefits")


# Base prompt for the Use Case Agent to extract requirements from documents
EXTRACT_REQUIREMENTS_PROMPT = """
You are an expert banking business analyst responsible for extracting business requirements for a Customer 360 data product.
Your task is to analyze the provided document and identify clear, structured business requirements.

Document Title: {document_title}
Document Content:
{document_content}

For each business requirement you identify, provide the following details:
1. A unique identifier (REQ-xxx)
2. A clear description of the requirement
3. The category it belongs to (Marketing, Risk, Customer Service, Compliance, etc.)
4. Priority level (High, Medium, Low)
5. Key stakeholders mentioned
6. Specific data needs mentioned
7. Any metrics or KPIs mentioned
8. Source within the document (section, page, etc.)

Focus on requirements that are relevant to a Customer 360 data product in the retail banking context.
Format each requirement as a structured JSON object.
"""


# Prompt to classify and prioritize the extracted requirements
CLASSIFY_REQUIREMENTS_PROMPT = """
You are an expert banking business analyst responsible for classifying and prioritizing requirements for a Customer 360 data product.
Review the extracted requirements below and organize them into cohesive business use cases.

Extracted Requirements:
{requirements_json}

For each business use case you identify:
1. Assign a unique identifier (UC-xxx)
2. Provide a descriptive name
3. Write a concise description of the use case
4. Identify the primary business objective
5. List the relevant requirements (by ID)
6. Define clear success criteria
7. List the categories of data needed
8. Identify primary stakeholders
9. Describe expected business benefits

Consider typical retail banking use cases such as:
- Customer segmentation and targeting
- Cross-selling and upselling opportunities
- Churn prediction and prevention
- Customer journey optimization
- Risk assessment and management
- Personalized service delivery
- Regulatory compliance
- Fraud detection and prevention

Format your response as a structured JSON array of business use cases.
"""


# Prompt to generate clarifying questions for stakeholders
GENERATE_QUESTIONS_PROMPT = """
You are an expert banking business analyst working on a Customer 360 data product.
You've extracted the following business use cases but need additional clarity from stakeholders.

Business Use Cases:
{use_cases_json}

Generate a set of clarifying questions for stakeholders to better understand the requirements.
For each question:
1. Specify which use case or requirement it relates to (by ID)
2. Explain why this information is needed
3. Suggest possible answers or options if applicable
4. Indicate the stakeholder who might best answer this question

Focus on questions that will help:
- Clarify ambiguous requirements
- Fill gaps in the data needs
- Validate assumptions
- Define success criteria more precisely
- Understand prioritization better
- Identify potential constraints or challenges

Format your response as a structured list of questions, organized by use case.
"""


# Prompt to structure the final requirements document
STRUCTURE_REQUIREMENTS_DOCUMENT_PROMPT = """
You are an expert banking business analyst finalizing a requirements document for a Customer 360 data product.
Based on the use cases, requirements, and stakeholder feedback provided, create a structured requirements document.

Use Cases:
{use_cases_json}

Requirements:
{requirements_json}

Stakeholder Feedback:
{stakeholder_feedback}

Create a comprehensive requirements document with the following sections:
1. Executive Summary
   - Brief overview of the Customer 360 initiative
   - Key business objectives
   - Expected benefits

2. Business Context
   - Industry trends driving the need for Customer 360
   - Current challenges in retail banking customer data
   - Strategic alignment within the organization

3. Business Use Cases
   - Detailed description of each use case
   - Prioritization and dependencies
   - Success criteria and metrics

4. Functional Requirements
   - Data requirements by business domain
   - Analytical capabilities needed
   - Integration requirements
   - Access and delivery requirements

5. Non-Functional Requirements
   - Performance expectations
   - Security and privacy requirements
   - Compliance requirements
   - Operational requirements

6. Implementation Considerations
   - Phasing recommendations
   - Dependencies and prerequisites
   - Risks and mitigation strategies

7. Appendices
   - Glossary of terms
   - Stakeholder list
   - Reference materials

Format your response as a well-structured markdown document. Use formatting, bullet points, tables, and other elements to enhance readability.
"""


def generate_extraction_prompt(document_title: str, document_content: str) -> str:
    """Generate a prompt to extract requirements from a document."""
    return EXTRACT_REQUIREMENTS_PROMPT.format(
        document_title=document_title,
        document_content=document_content
    )


def generate_classification_prompt(requirements_json: str) -> str:
    """Generate a prompt to classify requirements into use cases."""
    return CLASSIFY_REQUIREMENTS_PROMPT.format(
        requirements_json=requirements_json
    )


def generate_questions_prompt(use_cases_json: str) -> str:
    """Generate a prompt to create clarifying questions for stakeholders."""
    return GENERATE_QUESTIONS_PROMPT.format(
        use_cases_json=use_cases_json
    )


def generate_document_structure_prompt(
    use_cases_json: str,
    requirements_json: str,
    stakeholder_feedback: str
) -> str:
    """Generate a prompt to structure the final requirements document."""
    return STRUCTURE_REQUIREMENTS_DOCUMENT_PROMPT.format(
        use_cases_json=use_cases_json,
        requirements_json=requirements_json,
        stakeholder_feedback=stakeholder_feedback
    )


# Additional specialized prompts for banking use cases

RETAIL_BANKING_CUSTOMER_SEGMENTATION_PROMPT = """
You are a banking business analyst focusing on customer segmentation for retail banking.
Analyze the provided customer requirements and identify the key segmentation dimensions that should be included in the Customer 360 data product.

Customer Requirements:
{customer_requirements}

Focus on identifying segmentation dimensions that are:
1. Relevant to retail banking customer behavior
2. Measurable using typical banking data sources
3. Actionable for marketing, risk, or service personalization
4. Compliant with banking regulations and privacy concerns

For each segmentation dimension:
- Provide a clear name and description
- List the data attributes needed to calculate it
- Suggest how it could be used in business decisions
- Identify any challenges in implementing it

Common segmentation dimensions in retail banking include:
- Wealth/asset tiers
- Life stage (student, family formation, retirement, etc.)
- Banking behavior (transactor, borrower, saver, investor)
- Channel preference (branch, digital, mixed)
- Product utilization
- Risk profile
- Profitability and potential value

Format your response as a structured document describing the recommended segmentation approach for the Customer 360 data product.
"""


CUSTOMER_JOURNEY_MAPPING_PROMPT = """
You are a banking business analyst specializing in customer journey mapping.
Based on the provided retail banking context, identify the key customer journeys that should be captured in the Customer 360 data product.

Banking Context:
{banking_context}

For each significant customer journey:
1. Provide a name and description
2. Map out the typical stages
3. Identify the touchpoints involved
4. List the data elements needed to track this journey
5. Suggest metrics to measure journey effectiveness
6. Highlight potential pain points to monitor

Consider common retail banking journeys such as:
- New account opening
- Loan application and approval
- Credit card acquisition and activation
- Mobile/online banking enrollment and activation
- Service issue resolution
- Financial planning consultation
- Product inquiry to purchase
- Fraud incident resolution

Format your response as a structured document describing how these customer journeys should be represented in the Customer 360 data product.
"""


REGULATORY_COMPLIANCE_REQUIREMENTS_PROMPT = """
You are a banking compliance expert helping to define requirements for a Customer 360 data product.
Based on the provided compliance context, identify the key regulatory requirements that must be addressed in the data product design.

Compliance Context:
{compliance_context}

For each regulatory consideration:
1. Identify the relevant regulation (e.g., GDPR, CCPA, AML, KYC)
2. Explain how it impacts a Customer 360 data product
3. Specify data elements that require special handling
4. Outline necessary controls or limitations
5. Suggest documentation requirements
6. Identify stakeholders responsible for compliance

Address key areas such as:
- Data privacy and protection
- Right to access, correction, and deletion
- Consent management
- Data retention policies
- Sensitive attribute handling
- Audit trail requirements
- Cross-border data transfer constraints
- Regulatory reporting capabilities

Format your response as a structured document describing how regulatory compliance should be addressed in the Customer 360 data product.
"""
