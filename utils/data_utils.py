# data_utils.py - Data manipulation and schema utilities

import pandas as pd
import json
import re
from collections import defaultdict

class DataSchemaUtils:
    """
    Utilities for working with data schemas, mappings and transformations
    for the Customer 360 Multi-Agent System.
    """

    @staticmethod
    def validate_schema(schema):
        """
        Validates a proposed schema for completeness and consistency.

        Args:
            schema (dict): Schema definition

        Returns:
            tuple: (is_valid, list of issues)
        """
        issues = []

        # Check for missing required entities
        required_entities = ["Customer", "DemographicProfile", "FinancialProfile"]
        missing_entities = [entity for entity in required_entities if entity not in schema]
        if missing_entities:
            issues.append(f"Missing required entities: {', '.join(missing_entities)}")

        # Check data types
        for entity, attributes in schema.items():
            for attr_name, attr_type in attributes.items():
                # Check for valid types
                valid_base_types = ["STRING", "INT", "FLOAT", "DECIMAL", "BOOLEAN", "DATE",
                                   "TIMESTAMP", "ARRAY", "STRUCT"]

                base_type = attr_type.split("<")[0] if "<" in attr_type else attr_type
                if base_type not in valid_base_types:
                    issues.append(f"Invalid data type {attr_type} for {entity}.{attr_name}")

                # Check complex types have proper format
                if "ARRAY" in attr_type and "<" not in attr_type:
                    issues.append(f"ARRAY type needs element type specification for {entity}.{attr_name}")
                if "STRUCT" in attr_type and "<" not in attr_type:
                    issues.append(f"STRUCT type needs field specifications for {entity}.{attr_name}")

        return (len(issues) == 0, issues)

    @staticmethod
    def validate_mapping(mapping_list, source_systems, target_schema):
        """
        Validates data mappings against source systems and target schema.

        Args:
            mapping_list (list): List of mapping dictionaries
            source_systems (dict): Source system definitions
            target_schema (dict): Target schema definition

        Returns:
            tuple: (is_valid, list of issues)
        """
        issues = []

        for mapping in mapping_list:
            # Check source system exists
            if mapping["sourceSystem"] not in source_systems:
                issues.append(f"Unknown source system: {mapping['sourceSystem']}")

            # Check target entity exists
            if mapping["targetEntity"] not in target_schema:
                issues.append(f"Unknown target entity: {mapping['targetEntity']}")
            else:
                # Check target attribute exists in entity
                target_path = mapping["targetAttribute"].split(".")
                entity = target_schema[mapping["targetEntity"]]

                if len(target_path) == 1:
                    if target_path[0] not in entity:
                        issues.append(f"Unknown attribute {target_path[0]} in entity {mapping['targetEntity']}")
                else:
                    # Handle nested attributes
                    parent_attr = target_path[0]
                    if parent_attr not in entity:
                        issues.append(f"Unknown attribute {parent_attr} in entity {mapping['targetEntity']}")
                    elif "STRUCT" not in entity[parent_attr]:
                        issues.append(f"Attribute {parent_attr} is not a STRUCT type")

        return (len(issues) == 0, issues)

    @staticmethod
    def analyze_schema_coverage(requirements, schema):
        """
        Analyzes how well a schema covers the business requirements.

        Args:
            requirements (str): Business requirements text
            schema (dict): Proposed schema

        Returns:
            dict: Coverage analysis
        """
        # Extract key terms from requirements
        req_text = requirements.lower()
        key_terms = [
            "demographic", "profile", "income", "assets", "liabilities",
            "product", "holdings", "transaction", "risk", "channel",
            "interaction", "lifetime value", "profitability"
        ]

        term_presence = {}
        for term in key_terms:
            term_presence[term] = term in req_text

        # Check schema coverage
        coverage = {}
        for term in key_terms:
            if not term_presence[term]:
                coverage[term] = "Not required"
                continue

            found = False
            for entity, attributes in schema.items():
                entity_name = entity.lower()
                if term in entity_name:
                    found = True
                    coverage[term] = f"Covered in entity {entity}"
                    break

                # Check attribute names
                for attr_name in attributes.keys():
                    if term in attr_name.lower():
                        found = True
                        coverage[term] = f"Covered in {entity}.{attr_name}"
                        break

                if found:
                    break

            if not found:
                coverage[term] = "Not covered in schema"

        # Calculate coverage percentage
        required_terms = [term for term, present in term_presence.items() if present]
        covered_terms = [term for term in required_terms
                         if coverage.get(term, "").startswith("Covered")]

        coverage_percentage = round(len(covered_terms) / max(len(required_terms), 1) * 100)

        return {
            "coverage_percentage": coverage_percentage,
            "term_coverage": coverage,
            "missing_terms": [term for term in required_terms if not coverage.get(term, "").startswith("Covered")]
        }

    @staticmethod
    def generate_sample_data(schema, rows=5):
        """
        Generates sample data based on schema definition.

        Args:
            schema (dict): Schema definition
            rows (int): Number of sample rows to generate

        Returns:
            dict: Entity-based sample data
        """
        import random
        from datetime import datetime, timedelta

        sample_data = {}

        for entity, attributes in schema.items():
            entity_data = []

            for _ in range(rows):
                row = {}

                for attr_name, attr_type in attributes.items():
                    # Handle basic types
                    if attr_type == "STRING":
                        row[attr_name] = f"Sample{random.randint(1000, 9999)}"
                    elif attr_type == "INT":
                        row[attr_name] = random.randint(1, 1000)
                    elif attr_type == "FLOAT" or attr_type == "DECIMAL":
                        row[attr_name] = round(random.uniform(1, 1000), 2)
                    elif attr_type == "BOOLEAN":
                        row[attr_name] = random.choice([True, False])
                    elif attr_type == "DATE":
                        days = random.randint(0, 365)
                        date = datetime.now() - timedelta(days=days)
                        row[attr_name] = date.strftime("%Y-%m-%d")
                    # Handle complex types (simplified)
                    elif "STRUCT" in attr_type:
                        row[attr_name] = {"field1": "Sample value", "field2": random.randint(1, 100)}
                    elif "ARRAY" in attr_type:
                        row[attr_name] = [f"Item{i}" for i in range(1, random.randint(2, 5))]
                    else:
                        row[attr_name] = "Sample data"

                entity_data.append(row)

            sample_data[entity] = entity_data

        return sample_data

    @staticmethod
    def parse_transformation_logic(logic_text):
        """
        Parses and validates transformation logic expressions.

        Args:
            logic_text (str): Transformation logic expression

        Returns:
            tuple: (is_valid, parsed_components)
        """
        # Basic validation for SQL-like transformation expressions
        if not logic_text or logic_text.strip() == "":
            return (False, {"error": "Empty transformation logic"})

        # Extract function calls
        function_pattern = r'([A-Za-z_]+)\s*\('
        functions = re.findall(function_pattern, logic_text)

        # Extract column references
        column_pattern = r'([A-Za-z_][A-Za-z0-9_]*)'
        potential_columns = re.findall(column_pattern, logic_text)

        # Remove functions from potential columns
        columns = [col for col in potential_columns if col not in functions
                  and col not in ["AS", "AND", "OR", "NOT", "NULL", "IN",
                                 "BETWEEN", "LIKE", "CASE", "WHEN", "THEN", "ELSE", "END"]]

        # Check for conditional logic
        has_conditional = any(term in logic_text.upper()
                             for term in ["CASE", "WHEN", "IF(", "IIF("])

        # Check for aggregation
        has_aggregation = any(fn.upper() in ["SUM", "AVG", "MIN", "MAX", "COUNT"]
                             for fn in functions)

        return (True, {
            "functions": functions,
            "columns": columns,
            "has_conditional": has_conditional,
            "has_aggregation": has_aggregation,
            "original_logic": logic_text
        })

    @staticmethod
    def generate_mapping_dataframe(mappings):
        """
        Converts mapping dictionary list to a pandas DataFrame with added analysis.

        Args:
            mappings (list): List of mapping dictionaries

        Returns:
            pandas.DataFrame: DataFrame with mapping analysis
        """
        if not mappings:
            return pd.DataFrame()

        df = pd.DataFrame(mappings)

        # Add mapping complexity column
        def assess_complexity(row):
            logic = row.get('transformationLogic', '')
            if not logic or logic == '':
                return 'Simple'
            elif 'CASE' in logic or 'WHEN' in logic:
                return 'Complex'
            elif any(fn in logic for fn in ['CAST', 'CONVERT', 'UPPER', 'LOWER']):
                return 'Medium'
            else:
                return 'Simple'

        df['mappingComplexity'] = df.apply(assess_complexity, axis=1)

        return df

    @staticmethod
    def analyze_mapping_coverage(target_schema, mappings):
        """
        Analyzes coverage of the target schema by the provided mappings.

        Args:
            target_schema (dict): Target schema definition
            mappings (list): List of mapping dictionaries

        Returns:
            dict: Coverage analysis
        """
        # Count total attributes in schema
        total_attributes = 0
        flat_attributes = []

        for entity, attributes in target_schema.items():
            for attr_name, attr_type in attributes.items():
                if "STRUCT" in attr_type:
                    # Extract nested attributes for STRUCT types
                    struct_pattern = r'<([^>]+)>'
                    struct_match = re.search(struct_pattern, attr_type)
                    if struct_match:
                        struct_fields = struct_match.group(1).split(',')
                        for field in struct_fields:
                            if ':' in field:
                                field_name = field.split(':')[0].strip()
                                flat_attributes.append(f"{entity}.{attr_name}.{field_name}")
                                total_attributes += 1
                else:
                    flat_attributes.append(f"{entity}.{attr_name}")
                    total_attributes += 1

        # Count mapped attributes
        mapped_attributes = set()
        for mapping in mappings:
            target_attr = f"{mapping['targetEntity']}.{mapping['targetAttribute']}"
            mapped_attributes.add(target_attr)

        # Calculate coverage metrics
        coverage_percentage = round(len(mapped_attributes) / max(total_attributes, 1) * 100)

        # Find unmapped attributes
        unmapped = [attr for attr in flat_attributes if attr not in mapped_attributes]

        return {
            "total_attributes": total_attributes,
            "mapped_attributes": len(mapped_attributes),
            "coverage_percentage": coverage_percentage,
            "unmapped_attributes": unmapped
        }
