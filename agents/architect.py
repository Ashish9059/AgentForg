from .base_agent import BaseAgent
import json

class ArchitectAgent(BaseAgent):
    """
    V3.0 Web & API Architect: Designs high-level project structures focusing on 
    Backend-Service-Frontend (BSF) patterns and Web connectivity.
    """
    def plan_project(self, task_description: str):
        prompt = f"""
        You are the Lead Solution Architect for AgentForge v3.0.
        Your goal is to design a modern, scalable Python application based on the user's request.

        MISSION STANDARDS (V3.0):
        1. ARCHITECTURE: strictly follow the 'Backend-Service-Frontend' (BSF) pattern.
           - Frontend: Always prioritize Streamlit or Flask for web dashboards.
           - Service: API logic, Business logic, and External Integrations (using 'requests').
           - Storage: Data persistence (JSON, SQLite) handled in a dedicated module.
        
        2. FILE STRUCTURE:
           - web_interface.py: The frontend/UI entry point.
           - services.py: The core logic and API connectors.
           - storage.py: Database/File CRUD operations.
           - requirements.txt: All necessary dependencies (e.g., streamlit, requests, python-dotenv).
           - .env.example: Mock environment variables for API keys.

        3. REAL DATA: 
           If the task requires real-world data (Weather, Finance, Crypto, News), the design MUST 
           include a service that uses the 'requests' library to call public APIs.

        TASK: {task_description}

        OUTPUT FORMAT: You must return ONLY a JSON object with this exact structure:
        {{
            "project_name": "SlugifiedName",
            "architecture": "BSF",
            "files": [
                {{"filename": "web_interface.py", "purpose": "Streamlit UI logic"}},
                {{"filename": "services.py", "purpose": "Core logic & API connectivity using requests"}},
                {{"filename": "storage.py", "purpose": "Data persistence"}},
                {{"filename": "requirements.txt", "purpose": "Project dependencies"}}
            ],
            "entry_point": "web_interface.py",
            "external_apis": ["List of APIs to be used, e.g., CoinGecko, OpenWeather"]
        }}
        """
        response = self.query(prompt)
        try:
            # Clean possible markdown noise
            clean_json = self.scrub_output(response).strip()
            if "```json" in clean_json:
                clean_json = clean_json.split("```json")[1].split("```")[0].strip()
            elif "```" in clean_json:
                 clean_json = clean_json.split("```")[1].split("```")[0].strip()
            
            return json.loads(clean_json)
        except Exception as e:
            print(f"Architect Error: Failed to parse plan. Fallback to minimal structure. {e}")
            return {
                "project_name": "agent_project",
                "files": [{"filename": "main.py", "purpose": "main script"}],
                "entry_point": "main.py"
            }