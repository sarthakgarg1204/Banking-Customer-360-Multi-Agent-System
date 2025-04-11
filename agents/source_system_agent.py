# source_system_agent.py - Agent for identifying data sources
import json
import re
import ollama
from typing import Dict, List, Any

class SourceSystemAgent:
    """
    The Source System Agent identifies and catalogs relevant data sources
    for Customer 360 view creation in banking systems.
    """

    def __init__(self, model_name="gemma:2b"):
        """
        Initialize the Source System Agent with the specified LLM model.

        Args:
            model_name (str): Name of the Ollama model to use
        """
        self.model_name = model_name
        self.system_prompt = """
        You are a specialized banking data systems expert agent that identifies and catalogs
        data sources for Customer 360 data products. Your role is to:

        1. Identify relevant source systems that contain customer data
        2. Catalog key tables and attributes within those systems
        3. Assess data quality, update frequency, and accessibility
        4. Determine systems of record for different data domains
        5. Consider integration points and data retrieval methods

        Focus on typical banking systems including core banking, CRM, digital channels,
        risk systems, and marketing platforms.
        """

        # Known banking systems for reference
        self.known_systems = {
            "Core Banking System": {
                "description": "Primary system of record for customer accounts and transactions",
                "typical_tables": ["CUSTOMER_MASTER", "ACCOUNT_MASTER", "TRANSACTION_HISTORY", "PRODUCT_CATALOG"],
                "data_domains": ["customer demographics", "account details", "transaction history", "product holdings"],
                "update_frequency": "Real-time or daily batch"
            },
            "CRM System": {
                "description": "Customer relationship management system for sales and service",
                "typical_tables": ["CUSTOMER_INTERACTIONS", "SERVICE_REQUESTS", "OPPORTUNITIES", "CAMPAIGNS"],
                "data_domains": ["customer interactions", "service history", "sales pipeline", "campaign responses"],
                "update_frequency": "Real-time"
            },
            "Digital Banking": {
                "description": "Online and mobile banking platforms",
                "typical_tables": ["LOGIN_HISTORY", "FEATURE_USAGE", "APP_INTERACTIONS", "DEVICE_INFO"],
                "data_domains": ["digital behavior", "channel preferences", "feature adoption", "login patterns"],
                "update_frequency": "Real-time"
            },
            "Credit Risk System": {
                "description": "Credit scoring and risk assessment platform",
                "typical_tables": ["CREDIT_SCORES", "RISK_ASSESSMENTS", "DEFAULT_HISTORY", "LIMIT_MANAGEMENT"],
                "data_domains": ["credit scores", "risk ratings", "default history", "credit limits"],
                "update_frequency": "Daily or weekly"
            },
            "Marketing Automation": {
                "description": "Platform for campaign management and customer communications",
                "typical_tables": ["CAMPAIGN_HISTORY", "CUSTOMER_SEGMENTS", "COMMUNICATION_PREFERENCES", "RESPONSE_TRACKING"],
                "data_domains": ["marketing segments", "campaign history", "communication preferences", "offer responses"],
                "update_frequency": "Daily"
            },
            "Card Management System": {
                "description": "System managing credit and debit card issuance and transactions",
                "typical_tables": ["CARD_MASTER", "CARD_TRANSACTIONS", "REWARDS", "FRAUD_ALERTS"],
                "data_domains": ["card details", "card transactions", "rewards points", "fraud incidents"],
                "update_frequency": "Real-time or daily"
            },
            "Wealth Management System": {
                "description": "Platform for investment accounts and portfolio management",
                "typical_tables": ["INVESTMENT_ACCOUNTS", "PORTFOLIO_HOLDINGS", "ADVISORY_RELATIONSHIPS", "INVESTMENT_TRANSACTIONS"],
                "data_domains": ["investment portfolios", "financial advisor relationships", "investment transactions", "wealth metrics"],
                "update_frequency": "Daily"
            },
            "Loan Origination System": {
                "description": "System for processing and approving loan applications",
                "typical_tables": ["LOAN_APPLICATIONS", "UNDERWRITING_DECISIONS", "COLLATERAL", "PAYMENT_SCHEDULES"],
                "data_domains": ["loan applications", "credit decisions", "collateral valuations", "payment terms"],
                "update_frequency": "Daily"
            }
        }

    def identify_data_sources(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identify relevant data sources based on business requirements.

        Args:
            requirements (Dict[str, Any]): Structured requirements from Use Case Agent

        Returns:
            Dict[str, Any]: Catalog of identified data sources and their attributes
        """
        # Create prompt for LLM using the requirements
        prompt = f"""
        Identify the most relevant banking data sources for this Customer 360 use case:

        {json.dumps(requirements, indent=2)}

        For each relevant source system:
        1. List the key tables containing customer data
        2. Specify the update frequency (real-time, daily, weekly)
        3. Assess the typical data quality (high, medium, low)
        4. Identify what customer attributes would come from this source

        Focus on these common banking systems:
        - Core Banking System
        - CRM System
        - Digital Banking platforms
        - Card Management Systems
        - Credit Risk Systems
        - Marketing Automation
        - Wealth Management Systems (if relevant)
        - Loan Origination Systems (if relevant)

        Respond with a JSON object where each key is a source system name and the value contains
        details about that source (tables, update frequency, data quality, etc.).
        """

        # Get response from Ollama
        response = ollama.chat(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract JSON from response
        sources = self._extract_json_from_response(response["message"]["content"])

        # Add metadata
        sources["_metadata"] = {
            "model": self.model_name,
            "agent": "SourceSystem",
            "version": "1.0",
            "generatedFrom": requirements.get("businessObjective", "Unknown Business Objective")
        }

        return sources

    def _extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """Extract and parse JSON from LLM response"""
        try:
            # Try to find JSON pattern in the response
            json_pattern = r'({[\s\S]*})'
            json_match = re.search(json_pattern, response_text, re.DOTALL)

            if json_match:
                json_str = json_match.group(1)
                return json.loads(json_str)

            # If no JSON pattern found, try parsing the whole response
            return json.loads(response_text)
        except json.JSONDecodeError:
            # If JSON parsing fails, return a basic structure with error
            return {
                "error": "Failed to parse response as JSON",
                "rawResponse": response_text,
                "Core Banking System": {
                    "tables": ["CUSTOMER_MASTER", "ACCOUNT_MASTER"],
                    "update_frequency": "Daily",
                    "data_quality": "High"
                },
                "CRM System": {
                    "tables": ["CUSTOMER_INTERACTIONS"],
                    "update_frequency": "Real-time",
                    "data_quality": "Medium"
                }
            }

    def analyze_data_coverage(self, data_sources: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze how well identified data sources cover the required schema.

        Args:
            data_sources (Dict[str, Any]): Identified data sources
            schema (Dict[str, Any]): Target schema from Data Designer Agent

        Returns:
            Dict[str, Any]: Analysis of data coverage with gaps and recommendations
        """
        prompt = f"""
        Analyze how well these identified data sources cover the required schema for the Customer 360 view:

        TARGET SCHEMA:
        {json.dumps(schema, indent=2)}

        IDENTIFIED DATA SOURCES:
        {json.dumps(data_sources, indent=2)}

        Provide a coverage analysis including:
        1. For each entity in the schema, identify which source system(s) would provide the data
        2. Identify any gaps where schema attributes have no clear source
        3. Assess overall coverage percentage
        4. Recommend additional sources for any missing data elements

        Format your response as a JSON object with:
        - "entityCoverage": Object mapping each schema entity to source systems
        - "attributeGaps": Array of schema attributes with no identified source
        - "coveragePercentage": Estimated percentage of schema covered by sources
        - "recommendations": Array of recommended additional sources or actions
        """

        # Get response from Ollama
        response = ollama.chat(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract JSON from response
        coverage_analysis = self._extract_json_from_response(response["message"]["content"])

        # Add metadata
        coverage_analysis["_metadata"] = {
            "model": self.model_name,
            "agent": "SourceSystem",
            "version": "1.0",
            "analysisType": "DataCoverage"
        }

        return coverage_analysis

    # Continuing source_system_agent.py from where we left off
    def generate_source_documentation(self, data_sources: Dict[str, Any]) -> str:
        """
        Generate human-readable documentation for identified data sources.

        Args:
            data_sources (Dict[str, Any]): Identified data sources

        Returns:
            str: Markdown documentation describing the sources
        """
        prompt = f"""
        Create clear, human-readable documentation for these banking data sources:

        {json.dumps(data_sources, indent=2)}

        Generate markdown documentation that includes:
        1. Overview of each source system and its role in the Customer 360 view
        2. Key tables and their primary contents
        3. Data quality considerations and update frequencies
        4. Integration considerations for each system

        Format the documentation with proper markdown headings, tables, and bullet points.
        """

        # Get response from Ollama
        response = ollama.chat(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        # Return the markdown content
        return response["message"]["content"]

    def estimate_integration_complexity(self, data_sources: Dict[str, Any]) -> Dict[str, Any]:
        """
        Estimate the integration complexity for each identified source system.

        Args:
            data_sources (Dict[str, Any]): Identified data sources

        Returns:
            Dict[str, Any]: Complexity assessment for each source
        """
        prompt = f"""
        Estimate the integration complexity for each of these banking data sources:

        {json.dumps(data_sources, indent=2)}

        For each source system, assess:
        1. Integration complexity (High, Medium, Low)
        2. Expected integration method (API, batch file, database connection, etc.)
        3. Anticipated integration challenges
        4. Recommended integration approach

        Respond with a JSON object where each key is a source system name and the value
        contains the integration complexity assessment for that system.
        """

        # Get response from Ollama
        response = ollama.chat(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract JSON from response
        complexity_assessment = self._extract_json_from_response(response["message"]["content"])

        # Add metadata
        complexity_assessment["_metadata"] = {
            "model": self.model_name,
            "agent": "SourceSystem",
            "version": "1.0",
            "analysisType": "IntegrationComplexity"
        }

        return complexity_assessment


if __name__ == "__main__":
    # Example usage
    sample_requirements = {
        "businessObjective": "Create comprehensive view of premium banking customers",
        "primaryUseCase": "Personalized service and targeted marketing",
        "keyAttributes": [
            "demographics",
            "financial_status",
            "product_holdings",
            "channel_preferences",
            "risk_profile",
            "lifetime_value"
        ],
        "complianceRequirements": ["banking_regulations", "data_privacy"]
    }

    sample_schema = {
        "Customer": {
            "customerId": "STRING",
            "customerSegment": "STRING",
            "onboardingDate": "DATE",
            "relationshipManager": "STRING"
        },
        "DemographicProfile": {
            "name": "STRUCT<firstName:STRING, lastName:STRING>",
            "contactInfo": "STRUCT<email:STRING, phone:STRING, preferredContact:STRING>",
            "demographics": "STRUCT<age:INT, gender:STRING, occupation:STRING>"
        },
        "FinancialProfile": {
            "incomeDetails": "STRUCT<annualIncome:DECIMAL, incomeSource:STRING>",
            "wealthIndicators": "STRUCT<totalAssets:DECIMAL, totalLiabilities:DECIMAL>",
            "riskProfile": "STRUCT<creditScore:INT, riskCategory:STRING>"
        }
    }

    agent = SourceSystemAgent()

    # Identify data sources
    sources = agent.identify_data_sources(sample_requirements)
    print(json.dumps(sources, indent=2))

    # Analyze coverage
    coverage = agent.analyze_data_coverage(sources, sample_schema)
    print("\nCoverage Analysis:")
    print(json.dumps(coverage, indent=2))

    # Generate documentation
    docs = agent.generate_source_documentation(sources)
    print("\nSource Documentation:")
    print(docs)
