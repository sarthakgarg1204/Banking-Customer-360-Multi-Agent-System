# data_designer_agent.py - Data Designer Agent for Banking Customer 360 Demo
# This agent creates optimal data schemas for Customer 360 views

import json
import re
import os
from typing import Dict, List, Any, Optional
import ollama

class DataDesignerAgent:
    """
    Data Designer Agent analyzes business requirements and creates
    an optimal data schema for Customer 360 views.
    """

    def __init__(self, model_name: str = "gemma2b"):
        """
        Initialize the Data Designer Agent.

        Args:
            model_name: The name of the Ollama model to use
        """
        self.model_name = model_name
        self.schema = {}
        self.system_prompt = """
        You are a Data Designer Agent specialized in banking data modeling.
        Your task is to analyze business requirements and create an optimal data schema
        for Customer 360 views in retail banking. Focus on:

        1. Creating logical entity structures based on banking domain knowledge
        2. Defining appropriate data types and relationships
        3. Ensuring the schema covers all required business attributes
        4. Following banking industry best practices for data modeling
        5. Supporting compliance with banking regulations

        Respond with a JSON schema definition that follows modern data mesh principles.
        """

    def _call_ollama(self, prompt: str) -> str:
        """
        Call the Ollama API with the given prompt.

        Args:
            prompt: The prompt to send to the model

        Returns:
            The response from the model
        """
        try:
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                system=self.system_prompt,
                stream=False
            )
            return response.get('response', '')
        except Exception as e:
            print(f"Error calling Ollama API: {e}")
            return ""

    def _extract_json_from_text(self, text: str) -> Dict:
        """
        Extract JSON from text response.

        Args:
            text: Text that might contain JSON

        Returns:
            Parsed JSON as dictionary
        """
        # Try to find JSON pattern in the text
        json_pattern = r'```(?:json)?\s*({[\s\S]*?})\s*```'
        match = re.search(json_pattern, text)

        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass

        # If no match with code blocks, try to find just a JSON object
        json_pattern = r'({[\s\S]*?})'
        match = re.search(json_pattern, text)

        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass

        # If everything fails, return empty dict
        return {}

    def analyze_requirements(self, requirements: str) -> Dict:
        """
        Analyze business requirements to extract key data elements.

        Args:
            requirements: Business requirements text

        Returns:
            Dictionary of key data elements extracted from requirements
        """
        prompt = f"""
        Analyze the following banking customer 360 requirements and extract key data elements
        that should be included in the data schema:

        {requirements}

        Return your analysis as a structured JSON with key data elements grouped by category.
        """

        response = self._call_ollama(prompt)
        return self._extract_json_from_text(response)

    def create_schema(self, requirements: str, existing_schema: Optional[Dict] = None) -> Dict:
        """
        Create a data schema based on business requirements.

        Args:
            requirements: Business requirements text
            existing_schema: Optional existing schema to enhance

        Returns:
            A comprehensive data schema for the Customer 360 view
        """
        # First analyze the requirements to get key data elements
        data_elements = self.analyze_requirements(requirements)

        # Now create a schema based on these elements
        schema_prompt = f"""
        Create a comprehensive data schema for a Banking Customer 360 view based on these
        requirements and extracted data elements:

        Requirements:
        {requirements}

        Extracted Data Elements:
        {json.dumps(data_elements, indent=2)}

        If applicable, enhance this existing schema:
        {json.dumps(existing_schema, indent=2) if existing_schema else "No existing schema."}

        The schema should follow this structure:
        {{
          "Customer": {{
            "customerId": "STRING",
            "customerSegment": "STRING",
            "onboardingDate": "DATE",
            ...
          }},
          "DemographicProfile": {{
            "name": "STRUCT<firstName:STRING, lastName:STRING>",
            ...
          }},
          ...
        }}

        Use appropriate data types including: STRING, INT, FLOAT, DECIMAL, DATE, TIMESTAMP, BOOLEAN, ARRAY, STRUCT.
        For complex types, use the format: ARRAY<TYPE> or STRUCT<field:TYPE, field:TYPE>.
        Make sure all required attributes from the business requirements are included.
        """

        response = self._call_ollama(schema_prompt)
        schema = self._extract_json_from_text(response)

        # Save the schema for later use
        self.schema = schema

        return schema

    def generate_entity_relationships(self) -> Dict:
        """
        Generate entity relationship definitions for the data schema.

        Returns:
            Dictionary describing entity relationships
        """
        if not self.schema:
            return {}

        prompt = f"""
        Generate entity relationships for this Customer 360 data schema:

        {json.dumps(self.schema, indent=2)}

        Return a JSON object describing the relationships between entities, including:
        1. Primary keys
        2. Foreign keys
        3. Relationship types (one-to-one, one-to-many, many-to-many)
        4. Cardinality
        """

        response = self._call_ollama(prompt)
        return self._extract_json_from_text(response)

    def suggest_optimizations(self) -> List[str]:
        """
        Suggest optimizations for the current schema.

        Returns:
            List of optimization suggestions
        """
        if not self.schema:
            return []

        prompt = f"""
        Analyze this Customer 360 data schema and suggest optimizations:

        {json.dumps(self.schema, indent=2)}

        Consider:
        1. Query performance for common banking use cases
        2. Storage efficiency
        3. Data access patterns
        4. Regulatory compliance requirements

        Return a JSON array of optimization suggestions.
        """

        response = self._call_ollama(prompt)
        suggestions = self._extract_json_from_text(response)

        if isinstance(suggestions, dict) and "suggestions" in suggestions:
            return suggestions["suggestions"]
        elif isinstance(suggestions, list):
            return suggestions
        else:
            return []

    def save_schema(self, filepath: str) -> None:
        """
        Save the current schema to a file.

        Args:
            filepath: Path to save the schema JSON file
        """
        if not self.schema:
            return

        try:
            with open(filepath, 'w') as f:
                json.dump(self.schema, f, indent=2)
        except Exception as e:
            print(f"Error saving schema to {filepath}: {e}")

    def load_schema(self, filepath: str) -> Dict:
        """
        Load a schema from a file.

        Args:
            filepath: Path to the schema JSON file

        Returns:
            The loaded schema
        """
        try:
            with open(filepath, 'r') as f:
                self.schema = json.load(f)
            return self.schema
        except Exception as e:
            print(f"Error loading schema from {filepath}: {e}")
            return {}
