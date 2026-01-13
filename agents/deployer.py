from .base_agent import BaseAgent

class DeployerAgent(BaseAgent):
    """
    V3.0 DevOps Engineer: Generates production-grade deployment guides.
    """
    def generate_guide(self, plan: dict, project_context: str):
        project_name = plan.get("project_name", "agent_project")
        
        prompt = f"""
        You are a DevOps Engineer for AgentForge v3.0.
        Your goal is to write a professional 'DEPLOY.md' guide for the project: {project_name}.

        PROJECT PLAN: {plan}
        PROJECT CONTEXT:
        {project_context}

        INSTRUCTIONS:
        1. Identify dependencies and entry points.
        2. Provide clear instructions for setting up a virtual environment and installing requirements.
        3. Include sections for Environment Variables (based on .env.example).
        4. Recommend a hosting strategy (e.g., Streamlit Cloud, Heroku, or Docker).

        OUTPUT: Return the full content of 'DEPLOY.md' in Markdown format.
        """
        
        print("[Deployer] Finalizing Deployment Protocol...")
        return self.query(prompt)
