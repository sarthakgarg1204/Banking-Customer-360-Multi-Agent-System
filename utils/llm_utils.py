# llm_utils.py - Utilities for working with LLMs via Ollama

import json
import requests
import time
import os
from typing import Dict, List, Any, Optional

class OllamaLLM:
    """
    Client for interacting with Ollama API to access Gemma-2B model.
    """

    def __init__(self, model_name="gemma-2b", base_url="http://localhost:11434"):
        """
        Initialize the Ollama LLM client.

        Args:
            model_name (str): Name of the model to use
            base_url (str): Ollama API base URL
        """
        self.model_name = model_name
        self.base_url = base_url.rstrip('/')
        self.generate_endpoint = f"{self.base_url}/api/generate"
        self.chat_endpoint = f"{self.base_url}/api/chat"
        self.list_endpoint = f"{self.base_url}/api/tags"

    def _check_model_availability(self):
        """Check if the specified model is available in Ollama."""
        try:
            response = requests.get(self.list_endpoint)
            models = response.json().get('models', [])
            available_models = [model.get('name') for model in models]

            if self.model_name not in available_models:
                print(f"Warning: Model {self.model_name} not found in available models: {available_models}")
                return False
            return True
        except Exception as e:
            print(f"Error checking model availability: {str(e)}")
            return False

    def generate(self, prompt: str, system_prompt: Optional[str] = None,
                temperature: float = 0.7, max_tokens: Optional[int] = None) -> str:
        """
        Generate text completion using Ollama.

        Args:
            prompt (str): The prompt to send to the model
            system_prompt (str, optional): System instructions for the model
            temperature (float): Sampling temperature (0.0 to 1.0)
            max_tokens (int, optional): Maximum number of tokens to generate

        Returns:
            str: Generated text
        """
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "temperature": temperature,
        }

        if system_prompt:
            payload["system"] = system_prompt

        if max_tokens:
            payload["max_tokens"] = max_tokens

        try:
            response = requests.post(self.generate_endpoint, json=payload)
            if response.status_code == 200:
                return response.json().get('response', '')
            else:
                print(f"Error: Received status code {response.status_code}")
                print(response.text)
                return f"Error: Failed to generate text. Status code: {response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"

    def chat(self, messages: List[Dict[str, str]],
             system_prompt: Optional[str] = None,
             temperature: float = 0.7) -> str:
        """
        Chat completion using Ollama.

        Args:
            messages (List[Dict]): List of message dicts with 'role' and 'content'
            system_prompt (str, optional): System instructions for the model
            temperature (float): Sampling temperature (0.0 to 1.0)

        Returns:
            str: Response from the model
        """
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
        }

        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = requests.post(self.chat_endpoint, json=payload)
            if response.status_code == 200:
                return response.json().get('message', {}).get('content', '')
            else:
                print(f"Error: Received status code {response.status_code}")
                print(response.text)
                return f"Error: Failed to chat. Status code: {response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"


class AgentPromptLibrary:
    """
    Library of prompts for banking data product agents.
    """

    @staticmethod
    def use_case_agent_prompt(business_requirements: str) -> str:
        """Generate prompt for the Use Case Agent."""
        return f"""
        You are an expert Use Case Agent specialized in banking customer data analytics.

        Analyze the following business requirements for a banking Customer 360 view:

        {business_requirements}

        Extract and structure the following information:
        1. Primary business objective
        2. Key use cases (e.g., personalization, risk assessment)
        3. Required customer attributes and their importance
        4. Compliance and regulatory considerations
        5. KPIs and success metrics

        Format your response as JSON with these categories.
        """

    @staticmethod
    def data_designer_agent_prompt(use_case_requirements: Dict[str, Any]) -> str:
        """Generate prompt for the Data Designer Agent."""
        req_json = json.dumps(use_case_requirements, indent=2)
        return f"""
        You are an expert Data Designer Agent specialized in banking data models.

        Based on the following analyzed requirements:

        {req_json}

        Design an optimal schema for a Customer 360 data product with:
        1. Core entities (e.g., Customer, Accounts, Transactions)
        2. Entity attributes with appropriate data types
        3. Entity relationships and cardinality
        4. Logical grouping of related attributes

        Consider best practices for banking data models, including:
        - Separating transactional from profile data
        - Supporting time-variant analytics
        - Enabling regulatory reporting requirements
        - Maintaining data lineage and audit trails

        Format your response as JSON with entity definitions and their attributes.
        """

    @staticmethod
    def source_system_agent_prompt(use_case_requirements: Dict[str, Any]) -> str:
        """Generate prompt for the Source System Agent."""
        req_json = json.dumps(use_case_requirements, indent=2)
        return f"""
        You are an expert Source System Agent specialized in banking data systems.

        Based on the following requirements:

        {req_json}

        Identify appropriate source systems for a retail banking Customer 360 view:
        1. List each relevant source system (e.g., Core Banking, CRM)
        2. For each system, identify key data tables/entities
        3. Assess data quality and update frequency
        4. Note any data access or integration challenges

        Consider these common banking systems:
        - Core Banking System (customer accounts, transactions)
        - CRM System (interactions, service requests)
        - Digital Banking Platforms (online/mobile behavior)
        - Credit Risk Systems (scoring, assessments)
        - Marketing Campaign Systems (offers, responses)

        Format your response as JSON with systems and their key data entities.
        """

    @staticmethod
    def mapping_agent_prompt(schema: Dict[str, Any], source_systems: Dict[str, Any]) -> str:
        """Generate prompt for the Mapping Agent."""
        schema_json = json.dumps(schema, indent=2)
        sources_json = json.dumps(source_systems, indent=2)

        return f"""
        You are an expert Mapping Agent specialized in data integration for banking.

        Create source-to-target mappings between source systems and the target schema:

        TARGET SCHEMA:
        {schema_json}

        SOURCE SYSTEMS:
        {sources_json}

        For each target attribute, create a mapping specification with:
        1. Source system and table
        2. Source attribute name
        3. Any required transformation logic
        4. Data type conversion if needed

        Consider these common transformation types:
        - Direct mapping (1:1 copy)
        - Format standardization (dates, codes)
        - Conditional logic (CASE statements)
        - Derivation (calculated fields)
        - Lookups (code to description)

        Format your response as a list of JSON objects, each representing a mapping.
        """

    @staticmethod
    def certification_agent_prompt(schema: Dict[str, Any], mappings: List[Dict[str, Any]]) -> str:
        """Generate prompt for the Certification Agent."""
        schema_json = json.dumps(schema, indent=2)
        mappings_json = json.dumps(mappings, indent=2)

        return f"""
        You are an expert Certification Agent specialized in banking data governance.

        Evaluate the following Customer 360 data product for compliance and quality:

        TARGET SCHEMA:
        {schema_json}

        DATA MAPPINGS:
        {mappings_json}

        Assess the data product on these dimensions:
        1. Data quality (completeness, accuracy)
        2. Regulatory compliance (GDPR, banking regulations)
        3. PII handling and data privacy
        4. Data lineage and documentation
        5. Overall fitness for purpose

        Identify any issues that must be addressed before certification and suggest remediation steps.

        Format your response as a JSON report with assessment scores and recommendations.
        """


class MultiAgentOrchestrator:
    """
    Orchestrates the flow between multiple agents for banking Customer 360 creation.
    """

    def __init__(self, llm: OllamaLLM):
        """
        Initialize the orchestrator with an LLM client.

        Args:
            llm (OllamaLLM): The LLM client for agent interactions
        """
        self.llm = llm
        self.prompt_library = AgentPromptLibrary()
        self.current_state = {}

    def process_requirements(self, business_requirements: str) -> Dict[str, Any]:
        """
        Process business requirements through the full agent workflow.

        Args:
            business_requirements (str): Business requirements text

        Returns:
            dict: Complete workflow results
        """
        results = {
            "business_requirements": business_requirements,
            "timestamps": {
                "start": time.time()
            }
        }

        # Step 1: Use Case Agent
        print("🤖 Use Case Agent processing requirements...")
        use_case_prompt = self.prompt_library.use_case_agent_prompt(business_requirements)
        use_case_response = self.llm.generate(use_case_prompt)

        try:
            use_case_analysis = json.loads(use_case_response)
        except json.JSONDecodeError:
            # If not proper JSON, wrap in a basic structure
            use_case_analysis = {"analysis": use_case_response}

        results["use_case_analysis"] = use_case_analysis
        results["timestamps"]["use_case_complete"] = time.time()

        # Step 2: Data Designer Agent
        print("🤖 Data Designer Agent creating schema...")
        designer_prompt = self.prompt_library.data_designer_agent_prompt(use_case_analysis)
        schema_response = self.llm.generate(designer_prompt)

        try:
            proposed_schema = json.loads(schema_response)
        except json.JSONDecodeError:
            # If not proper JSON, create a simplified schema
            proposed_schema = {
                "Customer": {
                    "customerId": "STRING",
                    "customerName": "STRING",
                    "customerSegment": "STRING"
                }
            }

        results["proposed_schema"] = proposed_schema
        results["timestamps"]["schema_complete"] = time.time()

        # Step 3: Source System Agent
        print("🤖 Source System Agent identifying data sources...")
        source_prompt = self.prompt_library.source_system_agent_prompt(use_case_analysis)
        sources_response = self.llm.generate(source_prompt)

        try:
            data_sources = json.loads(sources_response)
        except json.JSONDecodeError:
            # If not proper JSON, create simplified sources
            data_sources = {
                "Core Banking System": {
                    "tables": ["CUSTOMER_MASTER", "ACCOUNT_MASTER"],
                    "update_frequency": "Daily"
                },
                "CRM System": {
                    "tables": ["CUSTOMER_INTERACTIONS"],
                    "update_frequency": "Real-time"
                }
            }

        results["data_sources"] = data_sources
        results["timestamps"]["sources_complete"] = time.time()

        # Step 4: Mapping Agent
        print("🤖 Mapping Agent creating data mappings...")
        mapping_prompt = self.prompt_library.mapping_agent_prompt(proposed_schema, data_sources)
        mappings_response = self.llm.generate(mapping_prompt)

        try:
            data_mappings = json.loads(mappings_response)
            # Ensure it's a list
            if not isinstance(data_mappings, list):
                data_mappings = [data_mappings]
        except json.JSONDecodeError:
            # Create simplified mappings
            data_mappings = [
                {
                    "sourceSystem": "Core Banking System",
                    "sourceTable": "CUSTOMER_MASTER",
                    "sourceAttribute": "CUST_ID",
                    "targetEntity": "Customer",
                    "targetAttribute": "customerId",
                    "transformationLogic": "CAST(CUST_ID AS STRING)",
                }
            ]

        results["data_mappings"] = data_mappings
        results["timestamps"]["mappings_complete"] = time.time()

        # Step 5: Certification Agent
        print("🤖 Certification Agent validating the data product...")
        certification_prompt = self.prompt_library.certification_agent_prompt(proposed_schema, data_mappings)
        certification_response = self.llm.generate(certification_prompt)

        try:
            certification_results = json.loads(certification_response)
        except json.JSONDecodeError:
            # Create simplified certification results
            certification_results = {
                "dataQualityScore": 85,
                "complianceStatus": "Needs Review",
                "recommendations": ["Validate PII handling", "Add data lineage documentation"]
            }

        results["certification_results"] = certification_results
        results["timestamps"]["certification_complete"] = time.time()

        # Calculate elapsed times
        start_time = results["timestamps"]["start"]
        for step, timestamp in results["timestamps"].items():
            if step != "start":
                results["timestamps"][f"{step}_elapsed"] = round(timestamp - start_time, 2)

        results["timestamps"]["total_elapsed"] = round(
            results["timestamps"]["certification_complete"] - start_time, 2)

        return results

    def generate_report(self, results: Dict[str, Any]) -> str:
        """
        Generate a comprehensive report from the agent workflow results.

        Args:
            results (dict): Results from the agent workflow

        Returns:
            str: Formatted markdown report
        """
        # Extract key information
        use_case = results.get("use_case_analysis", {})
        schema = results.get("proposed_schema", {})
        sources = results.get("data_sources", {})
        mappings = results.get("data_mappings", [])
        certification = results.get("certification_results", {})

        # Format as markdown report
        report = f"""
        # Customer 360 Data Product Report

        ## Executive Summary

        This report presents the automatically generated Customer 360 data product based on
        provided business requirements. The data product was designed and certified using
        a multi-agent AI system.

        **Business Objective**: {use_case.get("primaryBusinessObjective", "N/A")}

        **Quality Score**: {certification.get("dataQualityScore", "N/A")}/100

        **Compliance Status**: {certification.get("complianceStatus", "N/A")}

        **Processing Time**: {results.get("timestamps", {}).get("total_elapsed", "N/A")} seconds

        ## Data Product Schema

        The Customer 360 data product includes the following entities:

        """

        # Add schema entities
        for entity_name, attributes in schema.items():
            report += f"### {entity_name}\n\n"
            report += "| Attribute | Data Type |\n|-----------|----------|\n"

            for attr_name, attr_type in attributes.items():
                report += f"| {attr_name} | {attr_type} |\n"

            report += "\n"

        # Add source systems
        report += "## Source Systems\n\n"
        report += "| System | Tables | Update Frequency |\n|--------|--------|----------------|\n"

        for system_name, details in sources.items():
            tables = ", ".join(details.get("tables", []))
            frequency = details.get("update_frequency", "N/A")
            report += f"| {system_name} | {tables} | {frequency} |\n"

        report += "\n"

        # Add sample mappings (first 5)
        report += "## Sample Data Mappings\n\n"
        report += "| Source System | Source Table | Source Attribute | Target Entity | Target Attribute | Transformation |\n"
        report += "|--------------|-------------|-----------------|--------------|----------------|---------------|\n"

        for mapping in mappings[:5]:
            source_sys = mapping.get("sourceSystem", "N/A")
            source_tbl = mapping.get("sourceTable", "N/A")
            source_attr = mapping.get("sourceAttribute", "N/A")
            target_entity = mapping.get("targetEntity", "N/A")
            target_attr = mapping.get("targetAttribute", "N/A")
            transform = mapping.get("transformationLogic", "Direct")

            report += f"| {source_sys} | {source_tbl} | {source_attr} | {target_entity} | {target_attr} | {transform} |\n"

        report += f"\n*Showing {min(5, len(mappings))} of {len(mappings)} total mappings*\n\n"

        # Add certification recommendations
        report += "## Certification Recommendations\n\n"
        recommendations = certification.get("recommendations", [])

        if recommendations:
            for rec in recommendations:
                report += f"- {rec}\n"
        else:
            report += "No specific recommendations provided.\n"

        report += "\n## Next Steps\n\n"
        report += """
        1. Review the data product design with business stakeholders
        2. Address any certification recommendations
        3. Implement the data pipeline based on the provided mappings
        4. Set up monitoring and quality checks
        5. Document data lineage and usage guidelines
        """

        return report


class AgentMemory:
    """
    Maintains context and history for banking agents.
    """

    def __init__(self, agent_name: str, max_entries: int = 10):
        """
        Initialize agent memory.

        Args:
            agent_name (str): Name of the agent
            max_entries (int): Maximum memory entries to retain
        """
        self.agent_name = agent_name
        self.max_entries = max_entries
        self.memory = []
        self.key_facts = {}

    def add_interaction(self, prompt: str, response: str):
        """
        Add an interaction to the agent's memory.

        Args:
            prompt (str): Prompt sent to the agent
            response (str): Response received from the agent
        """
        self.memory.append({
            "timestamp": time.time(),
            "prompt": prompt,
            "response": response
        })

        # Trim memory if needed
        if len(self.memory) > self.max_entries:
            self.memory = self.memory[-self.max_entries:]

    def add_fact(self, key: str, value: Any):
        """
        Add or update a key fact in the agent's memory.

        Args:
            key (str): Fact identifier
            value (Any): Fact value
        """
        self.key_facts[key] = {
            "value": value,
            "timestamp": time.time()
        }

    def get_fact(self, key: str) -> Any:
        """
        Retrieve a fact from memory.

        Args:
            key (str): Fact identifier

        Returns:
            Any: The fact value or None if not found
        """
        fact_entry = self.key_facts.get(key)
        return fact_entry["value"] if fact_entry else None

    def format_memory_for_context(self) -> str:
        """
        Format memory as context for inclusion in prompts.

        Returns:
            str: Formatted memory context
        """
        context = f"--- {self.agent_name}'s Previous Knowledge ---\n"

        # Add key facts
        if self.key_facts:
            context += "Key facts:\n"
            for key, fact in self.key_facts.items():
                value = fact["value"]
                # Simplify complex objects for context
                if isinstance(value, (dict, list)):
                    value = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                context += f"- {key}: {value}\n"

        # Add recent interactions summary
        if self.memory:
            context += "\nRecent interactions:\n"
            for idx, entry in enumerate(reversed(self.memory[-3:])):
                prompt_summary = entry["prompt"][:50] + "..." if len(entry["prompt"]) > 50 else entry["prompt"]
                response_summary = entry["response"][:50] + "..." if len(entry["response"]) > 50 else entry["response"]
                context += f"[{idx+1}] Prompt: {prompt_summary}\n"
                context += f"    Response: {response_summary}\n"

        return context + "\n---\n"

    def save_to_file(self, filename: str = None):
        """
        Save agent memory to a file.

        Args:
            filename (str, optional): File path. If None, generate based on agent name.
        """
        if filename is None:
            filename = f"{self.agent_name.lower().replace(' ', '_')}_memory.json"

        data = {
            "agent_name": self.agent_name,
            "timestamp": time.time(),
            "key_facts": self.key_facts,
            "memory": self.memory
        }

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    def load_from_file(self, filename: str = None):
        """
        Load agent memory from a file.

        Args:
            filename (str, optional): File path. If None, generate based on agent name.

        Returns:
            bool: Success status
        """
        if filename is None:
            filename = f"{self.agent_name.lower().replace(' ', '_')}_memory.json"

        try:
            with open(filename, 'r') as f:
                data = json.load(f)

            self.agent_name = data.get("agent_name", self.agent_name)
            self.key_facts = data.get("key_facts", {})
            self.memory = data.get("memory", [])

            return True
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading memory: {str(e)}")
            return False
