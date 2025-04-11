# orchestrator.py - Orchestrator Agent for Banking Customer 360 Multi-Agent System

import os
import json
import time
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import importlib
import redis

# Import individual agent modules
from use_case_agent import UseCaseAgent
from data_designer_agent import DataDesignerAgent
from source_system_agent import SourceSystemAgent
from mapping_agent import MappingAgent
from certification_agent import CertificationAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Orchestrator")

# Initialize Redis for state management
try:
    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        password=os.getenv("REDIS_PASSWORD", ""),
        decode_responses=True
    )
    redis_client.ping()  # Test connection
    logger.info("Redis connection established successfully")
except Exception as e:
    logger.warning(f"Redis connection failed: {e}. Using in-memory state storage.")
    redis_client = None

# Data structures
@dataclass
class ProjectState:
    project_id: str
    status: str
    current_stage: str
    requirements: Dict
    schema: Dict = None
    data_sources: Dict = None
    mappings: List = None
    certification: Dict = None
    errors: List = None
    start_time: float = None
    completion_time: float = None

    def to_dict(self):
        return asdict(self)

@dataclass
class AgentTask:
    agent_name: str
    task_type: str
    input_data: Dict
    status: str = "pending"
    output: Any = None
    error: str = None
    start_time: float = None
    completion_time: float = None

class OrchestratorAgent:
    def __init__(self, project_id=None):
        self.project_id = project_id or f"project_{int(time.time())}"
        self.state = ProjectState(
            project_id=self.project_id,
            status="initialized",
            current_stage="setup",
            requirements={},
            errors=[],
            start_time=time.time()
        )
        self._save_state()

        # Initialize agent instances
        self.use_case_agent = UseCaseAgent()
        self.data_designer_agent = DataDesignerAgent()
        self.source_system_agent = SourceSystemAgent()
        self.mapping_agent = MappingAgent()
        self.certification_agent = CertificationAgent()

        logger.info(f"Orchestrator initialized with project ID: {self.project_id}")

    def _save_state(self):
        """Save current state to Redis or fallback to local variable."""
        if redis_client:
            redis_client.set(f"project:{self.project_id}", json.dumps(self.state.to_dict()))
        logger.debug(f"State saved for project {self.project_id}")

    def _load_state(self):
        """Load state from Redis if available."""
        if redis_client:
            state_data = redis_client.get(f"project:{self.project_id}")
            if state_data:
                state_dict = json.loads(state_data)
                self.state = ProjectState(**state_dict)
                logger.debug(f"State loaded for project {self.project_id}")

    def process_requirements(self, requirements: str) -> Dict:
        """Process business requirements and orchestrate the entire workflow."""
        try:
            # Initialize project with requirements
            self.state.requirements = {"text": requirements}
            self.state.status = "processing"
            self.state.current_stage = "requirements_analysis"
            self._save_state()

            logger.info(f"Starting new Customer 360 project with ID: {self.project_id}")

            # Step 1: Use Case Analysis
            logger.info("Running Use Case Agent")
            use_case_result = self.use_case_agent.analyze_requirements(requirements)
            self.state.current_stage = "schema_design"
            self._save_state()

            # Step 2: Run Data Designer and Source System agents in parallel
            # In a real implementation, we'd use async/await or threading here
            logger.info("Running Data Designer Agent")
            schema_result = self.data_designer_agent.design_schema(requirements, use_case_result)
            self.state.schema = schema_result
            self._save_state()

            logger.info("Running Source System Agent")
            source_system_result = self.source_system_agent.identify_sources(requirements, use_case_result)
            self.state.data_sources = source_system_result
            self.state.current_stage = "mapping_generation"
            self._save_state()

            # Step 3: Generate Mappings
            logger.info("Running Mapping Agent")
            mapping_result = self.mapping_agent.generate_mappings(schema_result, source_system_result)
            self.state.mappings = mapping_result
            self.state.current_stage = "certification"
            self._save_state()

            # Step 4: Certification
            logger.info("Running Certification Agent")
            certification_result = self.certification_agent.certify_data_product(schema_result, mapping_result, requirements)
            self.state.certification = certification_result

            # Mark project as complete
            self.state.status = "completed"
            self.state.current_stage = "complete"
            self.state.completion_time = time.time()
            self._save_state()

            logger.info(f"Customer 360 project {self.project_id} completed successfully")

            return self.state.to_dict()

        except Exception as e:
            logger.error(f"Error processing requirements: {e}", exc_info=True)
            self.state.status = "failed"
            self.state.errors.append(str(e))
            self._save_state()
            raise

    def get_project_status(self) -> Dict:
        """Get the current status of the project."""
        self._load_state()
        return self.state.to_dict()

    def get_task_statistics(self) -> Dict:
        """Get statistics about task execution times."""
        self._load_state()

        if not self.state.completion_time or not self.state.start_time:
            return {"status": "incomplete"}

        total_time = self.state.completion_time - self.state.start_time

        return {
            "total_time": round(total_time, 2),
            "stages": {
                "requirements_analysis": "completed",
                "schema_design": "completed",
                "mapping_generation": "completed",
                "certification": "completed"
            },
            "status": self.state.status
        }

    def visualize_workflow(self):
        """Generate a visual representation of the workflow."""
        # This could be expanded to create a more detailed visualization
        stages = [
            {"name": "Requirements Analysis", "agent": "Use Case Agent", "status": "completed" if self.state.current_stage != "requirements_analysis" else "in_progress"},
            {"name": "Schema Design", "agent": "Data Designer Agent", "status": "completed" if self.state.current_stage not in ["requirements_analysis", "schema_design"] else "in_progress" if self.state.current_stage == "schema_design" else "pending"},
            {"name": "Source Identification", "agent": "Source System Agent", "status": "completed" if self.state.current_stage not in ["requirements_analysis", "schema_design"] else "in_progress" if self.state.current_stage == "schema_design" else "pending"},
            {"name": "Mapping Generation", "agent": "Mapping Agent", "status": "completed" if self.state.current_stage not in ["requirements_analysis", "schema_design", "mapping_generation"] else "in_progress" if self.state.current_stage == "mapping_generation" else "pending"},
            {"name": "Certification", "agent": "Certification Agent", "status": "completed" if self.state.current_stage == "complete" else "in_progress" if self.state.current_stage == "certification" else "pending"},
        ]

        return stages

def create_agent_system(api_only=False):
    """Create the multi-agent system with orchestrator and specialized agents."""
    orchestrator = OrchestratorAgent()

    if api_only:
        from fastapi import FastAPI
        from pydantic import BaseModel

        app = FastAPI(title="Banking Customer 360 Multi-Agent API")

        class RequirementsRequest(BaseModel):
            requirements: str

        @app.post("/process")
        async def process_requirements(request: RequirementsRequest):
            result = orchestrator.process_requirements(request.requirements)
            return result

        @app.get("/status/{project_id}")
        async def get_status(project_id: str):
            orchestrator.project_id = project_id
            return orchestrator.get_project_status()

        @app.get("/workflow/{project_id}")
        async def get_workflow(project_id: str):
            orchestrator.project_id = project_id
            return orchestrator.visualize_workflow()

        return app
    else:
        return orchestrator

def visualize_terminal_workflow(stages):
    """Create a simple terminal visualization of the workflow."""
    status_symbols = {
        "completed": "✅",
        "in_progress": "🔄",
        "pending": "⏳"
    }

    result = "Customer 360 Workflow Progress:\n\n"

    for i, stage in enumerate(stages):
        result += f"{status_symbols[stage['status']]} {stage['name']} ({stage['agent']})\n"
        if i < len(stages) - 1:
            result += "    |\n    ▼\n"

    return result

if __name__ == "__main__":
    # Example usage when running directly
    import argparse

    parser = argparse.ArgumentParser(description="Banking Customer 360 Orchestrator Agent")
    parser.add_argument("--requirements", type=str, help="File containing business requirements")
    parser.add_argument("--api", action="store_true", help="Run as API server")
    parser.add_argument("--status", type=str, help="Get status of a project by ID")

    args = parser.parse_args()

    if args.api:
        import uvicorn
        app = create_agent_system(api_only=True)
        print("Starting API server at http://0.0.0.0:8000")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    elif args.status:
        orchestrator = OrchestratorAgent(project_id=args.status)
        status = orchestrator.get_project_status()
        workflow = orchestrator.visualize_workflow()

        print(json.dumps(status, indent=2))
        print("\n" + visualize_terminal_workflow(workflow))
    elif args.requirements:
        with open(args.requirements, "r") as f:
            requirements_text = f.read()

        orchestrator = OrchestratorAgent()
        result = orchestrator.process_requirements(requirements_text)
        workflow = orchestrator.visualize_workflow()

        print(json.dumps(result, indent=2))
        print("\n" + visualize_terminal_workflow(workflow))
    else:
        print("Please provide a requirements file, use --api flag to run as a server, or use --status to check a project")
