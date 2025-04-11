# certification_agent.py - Agent for validating and certifying data products
import json
import re
import ollama
from typing import Dict, List, Any

class CertificationAgent:
    """
    The Certification Agent validates data products against governance standards
    and ensures compliance with banking regulations and quality standards.
    """

    def __init__(self, model_name="gemma:2b"):
        """
        Initialize the Certification Agent with the specified LLM model.

        Args:
            model_name (str): Name of the Ollama model to use
        """
        self.model_name = model_name
        self.system_prompt = """
        You are a specialized data governance and compliance expert agent for banking. Your role is to:

        1. Validate data products against governance standards
        2. Ensure compliance with regulatory requirements
        3. Assess data quality and completeness
        4. Verify privacy protection measures
        5. Document certification results

        Be thorough in your assessments and provide clear, actionable recommendations.
        """

        # Known banking regulations and standards
        self.regulations = {
            "GDPR": {
                "description": "General Data Protection Regulation",
                "key_requirements": [
                    "Legal basis for processing personal data",
                    "Data minimization",
                    "Purpose limitation",
                    "Right to access and erasure"
                ]
            },
            "CCPA": {
                "description": "California Consumer Privacy Act",
                "key_requirements": [
                    "Disclosure of data collection and use",
                    "Right to opt-out of data sales",
                    "Right to deletion"
                ]
            },
            "GLBA": {
                "description": "Gramm-Leach-Bliley Act",
                "key_requirements": [
                    "Privacy notices",
                    "Opt-out provisions",
                    "Safeguarding customer data"
                ]
            },
            "PCI DSS": {
                "description": "Payment Card Industry Data Security Standard",
                "key_requirements": [
                    "Secure cardholder data",
                    "Encryption of data transmission",
                    "Access control measures"
                ]
            }
        }

    def certify_data_product(self, requirements: Dict[str, Any], schema: Dict[str, Any],
                             mappings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Certify a Customer 360 data product based on requirements, schema, and mappings.

        Args:
            requirements (Dict[str, Any]): Business requirements
            schema (Dict[str, Any]): Target data schema
            mappings (List[Dict[str, Any]]): Source-to-target mappings

        Returns:
            Dict[str, Any]: Certification results including scores and recommendations
        """
        prompt = f"""
        Certify this Customer 360 data product for banking based on:

        BUSINESS REQUIREMENTS:
        {json.dumps(requirements, indent=2)}

        TARGET SCHEMA:
        {json.dumps(schema, indent=2)}

        DATA MAPPINGS:
        {json.dumps(mappings[:5], indent=2)}
        ... (additional mappings omitted for brevity)

        Perform a comprehensive certification including:
        1. Data quality assessment
        2. Regulatory compliance check (GDPR, GLBA, etc.)
        3. Privacy assessment
        4. Data coverage evaluation
        5. Completeness verification

        For the certification, assign scores (0-100) in key areas and provide specific
        findings and recommendations. Format your response as a JSON object with these components:

        - dataQualityScore: Overall score (0-100)
        - complianceStatus: "Approved", "Conditionally Approved", or "Rejected"
        - privacyAssessment: Text describing privacy compliance
        - dataCoverage: Percentage of required attributes that are mapped
        - missingElements: Array of missing data elements
        - recommendations: Array of specific recommendations
        - findings: Detailed findings in each certification area
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
        certification = self._extract_json_from_response(response["message"]["content"])

        # Add metadata
        certification["_metadata"] = {
            "model": self.model_name,
            "agent": "Certification",
            "version": "1.0",
            "certificationDate": "2025-04-11",  # Using current date from instructions
            "certificationId": f"CERT-{hash(str(requirements) + str(schema)) % 10000:04d}"
        }

        return certification

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
                "dataQualityScore": 0,
                "complianceStatus": "Rejected",
                "privacyAssessment": "Unable to assess due to parsing error",
                "dataCoverage": 0,
                "missingElements": ["Entire assessment due to parsing error"],
                "recommendations": ["Retry certification process"]
            }

    def perform_privacy_impact_assessment(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform a detailed privacy impact assessment on the data schema.

        Args:
            schema (Dict[str, Any]): Target data schema

        Returns:
            Dict[str, Any]: Privacy impact assessment results
        """
        prompt = f"""
        Perform a detailed privacy impact assessment on this banking Customer 360 schema:

        {json.dumps(schema, indent=2)}

        Consider these privacy regulations relevant to banking:
        - GDPR (General Data Protection Regulation)
        - GLBA (Gramm-Leach-Bliley Act)
        - CCPA (California Consumer Privacy Act)
        - Data protection and banking secrecy laws

        For the assessment:
        1. Identify all PII (Personally Identifiable Information) in the schema
        2. Classify attributes by sensitivity level (High, Medium, Low)
        3. Assess compliance risks
        4. Recommend privacy protection measures

        Format your response as a JSON object with the following structure:
        - piiAttributes: Array of PII attributes found in the schema
        - sensitivityClassification: Object mapping attributes to sensitivity levels
        - complianceRisks: Array of identified compliance risks
        - protectionRecommendations: Array of recommended protection measures
        - overallRiskLevel: "High", "Medium", or "Low"
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
        assessment = self._extract_json_from_response(response["message"]["content"])

        # Add metadata
        assessment["_metadata"] = {
            "model": self.model_name,
            "agent": "Certification",
            "version": "1.0",
            "assessmentType": "PrivacyImpact",
            "assessmentDate": "2025-04-11"  # Using current date from instructions
        }

        return assessment

    def generate_certification_document(self, certification_results: Dict[str, Any]) -> str:
        """
        Generate a formal certification document based on certification results.

        Args:
            certification_results (Dict[str, Any]): Results from certify_data_product

        Returns:
            str: Markdown certification document
        """
        prompt = f"""
        Create a formal certification document for this banking Customer 360 data product based on:

        {json.dumps(certification_results, indent=2)}

        Generate a professional markdown document that includes:
        1. Executive summary with certification decision
        2. Detailed findings in each assessment area
        3. Compliance status with specific regulations
        4. Required actions for conditional approval (if applicable)
        5. Recommendations for improvement
        6. Certification details (ID, date, approver)

        Format the document with proper markdown headings, tables, and bullet points.
        Make it suitable for presentation to data governance teams and regulators.
        """

        # Get response from Ollama
        response = ollama.chat(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        # Return the markdown document
        return response["message"]["content"]

    def generate_governance_metadata(self, schema: Dict[str, Any], certification: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate governance metadata for the certified data product.

        Args:
            schema (Dict[str, Any]): Target data schema
            certification (Dict[str, Any]): Certification results

        Returns:
            Dict[str, Any]: Governance metadata for the data product
        """
        prompt = f"""
        Create comprehensive governance metadata for this certified Customer 360 data product:

        SCHEMA:
        {json.dumps(schema, indent=2)}

        CERTIFICATION:
        {json.dumps(certification, indent=2)}

        Generate metadata that includes:
        1. Data ownership information
        2. Privacy classification for each entity/attribute
        3. Data retention policies
        4. Access control recommendations
        5. Data lineage summary
        6. Audit requirements

        Format your response as a JSON object with appropriate sections and details.
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
        governance_metadata = self._extract_json_from_response(response["message"]["content"])

        # Add metadata
        governance_metadata["_metadata"] = {
            "model": self.model_name,
            "agent": "Certification",
            "version": "1.0",
            "metadataType": "Governance",
            "generationDate": "2025-04-11"  # Using current date from instructions
        }

        return governance_metadata

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
            "customerSegment": "STRING"
        },
        "DemographicProfile": {
            "name": "STRUCT<firstName:STRING, lastName:STRING>",
            "contactInfo": "STRUCT<email:STRING, phone:STRING, preferredContact:STRING>"
        },
        "FinancialProfile": {
            "incomeDetails": "STRUCT<annualIncome:DECIMAL, incomeSource:STRING>",
            "riskProfile": "STRUCT<creditScore:INT, riskCategory:STRING>"
        }
    }

    sample_mappings = [
        {
            "sourceSystem": "Core Banking System",
            "sourceTable": "CUSTOMER_MASTER",
            "sourceAttribute": "CUST_ANNUAL_INCOME",
            "targetEntity": "FinancialProfile",
            "targetAttribute": "incomeDetails.annualIncome",
            "transformationLogic": "CAST(CUST_ANNUAL_INCOME AS DECIMAL(12,2))"
        },
        {
            "sourceSystem": "Core Banking System",
            "sourceTable": "CUSTOMER_MASTER",
            "sourceAttribute": "CUSTOMER_SEGMENT",
            "targetEntity": "Customer",
            "targetAttribute": "customerSegment",
            "transformationLogic": "CASE WHEN CUSTOMER_SEGMENT = 'P' THEN 'Premium' ELSE 'Standard' END"
        }
    ]

    agent = CertificationAgent()

    # Certify data product
    certification = agent.certify_data_product(sample_requirements, sample_schema, sample_mappings)
    print(json.dumps(certification, indent=2))

    # Perform privacy impact assessment
    privacy_assessment = agent.perform_privacy_impact_assessment(sample_schema)
    print("\nPrivacy Impact Assessment:")
    print(json.dumps(privacy_assessment, indent=2))

    # Generate certification document
    certification_doc = agent.generate_certification_document(certification)
    print("\nCertification Document:")
    print(certification_doc)
