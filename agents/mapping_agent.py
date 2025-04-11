# mapping_agent.py - Agent for creating source-to-target data mappings
import json
import re
import ollama
from typing import Dict, List, Any

class MappingAgent:
    """
    The Mapping Agent creates source-to-target attribute mappings and
    defines transformation logic for Customer 360 data products.
    """

    def __init__(self, model_name="gemma:2b"):
        """
        Initialize the Mapping Agent with the specified LLM model.

        Args:
            model_name (str): Name of the Ollama model to use
        """
        self.model_name = model_name
        self.system_prompt = """
        You are a specialized data mapping expert agent for banking. Your role is to create
        source-to-target mappings for Customer 360 data products by:

        1. Identifying appropriate source attributes for each target attribute
        2. Creating transformation logic when needed (format conversions, calculations, etc.)
        3. Handling complex mappings that may require multiple source attributes
        4. Documenting data type conversions and validations
        5. Understanding banking-specific data transformations

        Create clear, implementable mapping specifications following best practices.
        """

    def generate_mappings(self, schema: Dict[str, Any], data_sources: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate source-to-target mappings based on schema and data sources.

        Args:
            schema (Dict[str, Any]): Target schema from Data Designer Agent
            data_sources (Dict[str, Any]): Source systems from Source System Agent

        Returns:
            List[Dict[str, Any]]: List of mapping specifications
        """
        prompt = f"""
        Create detailed source-to-target mappings for a banking Customer 360 view based on:

        TARGET SCHEMA:
        {json.dumps(schema, indent=2)}

        SOURCE SYSTEMS:
        {json.dumps(data_sources, indent=2)}

        Generate specific mappings for key attributes, including:
        1. Source system and table/attribute names
        2. Target entity and attribute names
        3. Transformation logic where needed
        4. Data type conversions

        For example:
        {{
          "sourceSystem": "Core Banking System",
          "sourceTable": "CUSTOMER_MASTER",
          "sourceAttribute": "CUST_ANNUAL_INCOME",
          "targetEntity": "FinancialProfile",
          "targetAttribute": "incomeDetails.annualIncome",
          "transformationLogic": "CAST(CUST_ANNUAL_INCOME AS DECIMAL(12,2))"
        }}

        Create at least 5-10 different mappings covering different target entities.
        Return the mappings as a JSON array of mapping objects.
        """

        # Get response from Ollama
        response = ollama.chat(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract JSON array from response
        mapping_list = self._extract_json_array_from_response(response["message"]["content"])

        # Add metadata to each mapping
        for mapping in mapping_list:
            mapping["_metadata"] = {
                "generatedBy": "MappingAgent",
                "version": "1.0",
                "model": self.model_name
            }

        return mapping_list

    def _extract_json_array_from_response(self, response_text: str) -> List[Dict[str, Any]]:
        """Extract and parse JSON array from LLM response"""
        try:
            # Try to find JSON array pattern in the response
            json_pattern = r'(\[[\s\S]*\])'
            json_match = re.search(json_pattern, response_text, re.DOTALL)

            if json_match:
                json_str = json_match.group(1)
                return json.loads(json_str)

            # If no JSON array pattern found, try parsing the whole response
            return json.loads(response_text)
        except json.JSONDecodeError:
            # If JSON parsing fails, return a basic mapping list
            return [
                {
                    "sourceSystem": "Core Banking System",
                    "sourceTable": "CUSTOMER_MASTER",
                    "sourceAttribute": "CUST_ID",
                    "targetEntity": "Customer",
                    "targetAttribute": "customerId",
                    "transformationLogic": "CAST(CUST_ID AS STRING)",
                    "error": "Failed to parse response as JSON",
                    "rawResponse": response_text
                }
            ]

    def generate_transformation_logic(self, mapping_item: Dict[str, Any]) -> str:
        """
        Generate detailed transformation logic for a specific mapping.

        Args:
            mapping_item (Dict[str, Any]): A single mapping specification

        Returns:
            str: Detailed transformation SQL or pseudocode
        """
        prompt = f"""
        Create detailed transformation logic for this source-to-target mapping:

        {json.dumps(mapping_item, indent=2)}

        Provide the transformation as executable SQL or pseudocode that handles:
        1. Data type conversions
        2. Format standardization
        3. Default values for nulls
        4. Validation rules
        5. Business logic (if applicable)

        The transformation should be detailed enough to implement in an ETL tool or SQL procedure.
        """

        # Get response from Ollama
        response = ollama.chat(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        # Return transformation logic
        return response["message"]["content"].strip()

    def validate_mappings(self, mappings: List[Dict[str, Any]], schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate generated mappings against the target schema.

        Args:
            mappings (List[Dict[str, Any]]): Generated mappings
            schema (Dict[str, Any]): Target schema

        Returns:
            Dict[str, Any]: Validation results including coverage and issues
        """
        # Extract all target entities and attributes from schema
        target_entities = {}
        for entity_name, entity_def in schema.items():
            if entity_name.startswith("_"):  # Skip metadata
                continue

            target_entities[entity_name] = []
            for attr_name in entity_def.keys():
                target_entities[entity_name].append(attr_name)

                # Handle struct types to get nested attributes
                attr_type = entity_def.get(attr_name, "")
                if isinstance(attr_type, str) and "STRUCT<" in attr_type:
                    struct_attrs = attr_type.split("STRUCT<")[1].split(">")[0].split(",")
                    for struct_attr in struct_attrs:
                        struct_name = struct_attr.split(":")[0] if ":" in struct_attr else struct_attr
                        target_entities[entity_name].append(f"{attr_name}.{struct_name}")

        # Track which attributes are mapped
        mapped_attributes = {}
        for entity in target_entities:
            mapped_attributes[entity] = []

        # Check each mapping against target schema
        mapping_issues = []
        for idx, mapping in enumerate(mappings):
            target_entity = mapping.get("targetEntity")
            target_attr = mapping.get("targetAttribute")

            if target_entity not in target_entities:
                mapping_issues.append(f"Mapping #{idx+1}: Target entity '{target_entity}' not found in schema")
                continue

            # Handle base attributes and nested attributes
            if "." in target_attr:  # Nested attribute
                base_attr = target_attr.split(".")[0]
                if base_attr not in target_entities[target_entity]:
                    mapping_issues.append(f"Mapping #{idx+1}: Base attribute '{base_attr}' not found in entity '{target_entity}'")
                else:
                    mapped_attributes[target_entity].append(target_attr)
            else:  # Direct attribute
                if target_attr not in target_entities[target_entity]:
                    mapping_issues.append(f"Mapping #{idx+1}: Attribute '{target_attr}' not found in entity '{target_entity}'")
                else:
                    mapped_attributes[target_entity].append(target_attr)

        # Calculate coverage
        total_attributes = sum(len(attrs) for attrs in target_entities.values())
        total_mapped = sum(len(attrs) for attrs in mapped_attributes.values())
        coverage_percentage = (total_mapped / total_attributes * 100) if total_attributes > 0 else 0

        # Find unmapped attributes
        unmapped_attributes = {}
        for entity, attrs in target_entities.items():
            unmapped = [attr for attr in attrs if attr not in mapped_attributes.get(entity, [])]
            if unmapped:
                unmapped_attributes[entity] = unmapped

        # Create validation result
        validation_result = {
            "totalAttributes": total_attributes,
            "mappedAttributes": total_mapped,
            "coveragePercentage": round(coverage_percentage, 2),
            "unmappedAttributes": unmapped_attributes,
            "mappingIssues": mapping_issues,
            "validationPassed": len(mapping_issues) == 0 and coverage_percentage >= 80
        }

        return validation_result

    def generate_mapping_documentation(self, mappings: List[Dict[str, Any]]) -> str:
        """
        Generate human-readable documentation for the mappings.

        Args:
            mappings (List[Dict[str, Any]]): Generated mappings

        Returns:
            str: Markdown documentation describing the mappings
        """
        prompt = f"""
        Create clear, human-readable documentation for these Customer 360 data mappings:

        {json.dumps(mappings, indent=2)}

        Generate markdown documentation that includes:
        1. Overview of the mapping approach
        2. Source-to-target mapping tables organized by target entity
        3. Explanation of key transformations
        4. Notes on special cases or complex mappings

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

if __name__ == "__main__":
    # Example usage
    sample_schema = {
        "Customer": {
            "customerId": "STRING",
            "customerSegment": "STRING"
        },
        "FinancialProfile": {
            "incomeDetails": "STRUCT<annualIncome:DECIMAL, incomeSource:STRING>",
            "riskProfile": "STRUCT<creditScore:INT, riskCategory:STRING>"
        }
    }

    sample_sources = {
        "Core Banking System": {
            "tables": ["CUSTOMER_MASTER", "ACCOUNT_MASTER"],
            "update_frequency": "Daily",
            "data_quality": "High"
        },
        "Credit Risk System": {
            "tables": ["CREDIT_SCORES", "RISK_ASSESSMENTS"],
            "update_frequency": "Weekly",
            "data_quality": "High"
        }
    }

    agent = MappingAgent()

    # Generate mappings
    mappings = agent.generate_mappings(sample_schema, sample_sources)
    print(json.dumps(mappings, indent=2))

    # Validate mappings
    validation = agent.validate_mappings(mappings, sample_schema)
    print("\nMapping Validation:")
    print(json.dumps(validation, indent=2))

    # Generate documentation
    if mappings:
        docs = agent.generate_mapping_documentation(mappings)
        print("\nMapping Documentation:")
        print(docs)
