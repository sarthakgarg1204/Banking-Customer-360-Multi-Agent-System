# use_case_agent.py - Agent for interpreting business requirements
import json
import re
import ollama
from typing import Dict, List, Any

class UseCaseAgent:
    """
    The Use Case Agent interprets business requirements for Customer 360 views
    and extracts structured information about goals, KPIs, and needed attributes.
    """

    def __init__(self, model_name="gemma:2b"):
        """
        Initialize the Use Case Agent with the specified LLM model.

        Args:
            model_name (str): Name of the Ollama model to use
        """
        self.model_name = model_name
        self.system_prompt = """
        You are a specialized banking domain expert agent that interprets business requirements
        for Customer 360 data products. Your role is to analyze requirements text and extract:

        1. Primary business objectives
        2. Key use cases and their priorities
        3. Required customer attributes and data elements
        4. Compliance and regulatory requirements
        5. Key performance indicators

        Format your response as a structured JSON object.
        """

    def process_requirements(self, requirements_text: str) -> Dict[str, Any]:
        """
        Process business requirements text and extract structured information.

        Args:
            requirements_text (str): Raw business requirements document

        Returns:
            Dict[str, Any]: Structured requirements with key elements identified
        """
        # Clean and normalize the input text
        cleaned_text = self._preprocess_text(requirements_text)

        # Create prompt for the LLM
        prompt = f"""
        Based on the following business requirements for a banking Customer 360 data product,
        extract the key elements and structure them according to the categories below.

        BUSINESS REQUIREMENTS:
        {cleaned_text}

        Extract and structure the following information in JSON format:
        1. "businessObjective": The primary business goal of this Customer 360 initiative
        2. "primaryUseCase": The main way this data will be used
        3. "secondaryUseCases": List of additional ways the data will be used
        4. "keyAttributes": List of all required customer attributes mentioned
        5. "customerSegments": Any specific customer segments mentioned
        6. "complianceRequirements": Any regulatory or compliance considerations
        7. "stakeholders": The teams or roles that will use this data
        8. "kpis": Key performance indicators to measure success

        Respond only with valid JSON.
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
        result = self._extract_json_from_response(response["message"]["content"])

        # Add processing metadata
        result["processingInfo"] = {
            "model": self.model_name,
            "agent": "UseCase",
            "version": "1.0"
        }

        return result

    def _preprocess_text(self, text: str) -> str:
        """Clean and normalize input text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,;:?!()-]', '', text)
        return text.strip()

    def _extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """Extract and parse JSON from LLM response"""
        try:
            # Try to find JSON pattern in the response
            json_pattern = r'({.*})'
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
                "businessObjective": "Unknown - parsing error",
                "primaryUseCase": "Unknown - parsing error",
                "keyAttributes": []
            }

    def validate_requirements(self, structured_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the extracted requirements for completeness and clarity.

        Args:
            structured_requirements (Dict[str, Any]): The extracted requirements

        Returns:
            Dict[str, Any]: Validation results with any identified issues
        """
        issues = []

        # Check for minimum required fields
        required_fields = ["businessObjective", "primaryUseCase", "keyAttributes"]
        for field in required_fields:
            if field not in structured_requirements or not structured_requirements[field]:
                issues.append(f"Missing required field: {field}")

        # Check for minimum attributes
        if "keyAttributes" in structured_requirements and len(structured_requirements["keyAttributes"]) < 3:
            issues.append("Too few key attributes identified. Requirements may be incomplete.")

        # Check for compliance requirements in regulated industry
        if "complianceRequirements" not in structured_requirements or not structured_requirements.get("complianceRequirements"):
            issues.append("No compliance requirements identified. For banking, this is unusual.")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "requirements": structured_requirements
        }

    def generate_clarification_questions(self, structured_requirements: Dict[str, Any]) -> List[str]:
        """
        Generate clarification questions for incomplete or ambiguous requirements.

        Args:
            structured_requirements (Dict[str, Any]): The extracted requirements

        Returns:
            List[str]: List of clarification questions
        """
        prompt = f"""
        Based on the following structured requirements for a banking Customer 360 data product,
        generate 3-5 clarification questions that would help improve the requirements.

        STRUCTURED REQUIREMENTS:
        {json.dumps(structured_requirements, indent=2)}

        Generate questions that would help clarify:
        1. Any vague or ambiguous requirements
        2. Missing information about data attributes
        3. Unclear business goals or use cases
        4. Incomplete compliance requirements
        5. Undefined success metrics or KPIs

        Provide only the list of questions, numbered.
        """

        # Get response from Ollama
        response = ollama.chat(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract questions from response
        content = response["message"]["content"]
        questions = []

        # Extract numbered questions using regex
        question_pattern = r'(?:\d+\.|\-)\s*(.+?)(?=(?:\d+\.|\-)|$)'
        matches = re.finditer(question_pattern, content, re.DOTALL)

        for match in matches:
            question = match.group(1).strip()
            if question:
                questions.append(question)

        # If regex failed to extract questions, return the raw response
        if not questions:
            # Split by newlines and try to identify questions
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line and ('?' in line or re.match(r'^\d+\.', line)):
                    questions.append(line)

        return questions

if __name__ == "__main__":
    # Example usage
    requirements = """
    Business Requirement: Premium Customer 360 View

    We need a comprehensive view of our premium banking customers to support personalized
    service offerings and targeted marketing campaigns. The solution should integrate data
    from our core banking system, CRM, transaction history, and digital banking channels.

    Key objectives:
    1. Identify cross-sell and up-sell opportunities
    2. Improve retention of high-value customers
    3. Personalize digital banking experiences
    4. Enable relationship managers to provide tailored service

    Required customer attributes:
    - Complete demographic profile
    - Financial status (income, assets, liabilities)
    - Product holdings and usage patterns
    - Channel preferences and interaction history
    - Risk profile and investment preferences
    - Lifetime value and profitability metrics

    The solution must comply with all banking regulations and data privacy requirements.
    """

    agent = UseCaseAgent()
    result = agent.process_requirements(requirements)
    print(json.dumps(result, indent=2))

    # Validate the requirements
    validation = agent.validate_requirements(result)
    print("\nValidation results:")
    print(json.dumps(validation, indent=2))

    # Generate clarification questions
    questions = agent.generate_clarification_questions(result)
    print("\nClarification questions:")
    for i, question in enumerate(questions, 1):
        print(f"{i}. {question}")
