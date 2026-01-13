from .base_agent import BaseAgent
import os

class CoderAgent(BaseAgent):
    """
    V3.0 Professional Coder: Implements BSF architecture with a focus on real-world 
    API connectivity, security (.env), and robustness.
    """
    def write_code(self, plan: str, filename: str, project_context: str = ""):
        prompt = f"""
        You are a Senior Python Developer implementing AgentForge v3.0 standards.
        Your task is to write high-quality, production-ready code for the file: '{filename}'

        PROJECT ARCHITECTURE: {plan}
        PREVIOUSLY WRITTEN FILES FOR CONTEXT:
        {project_context}

        V3.0 CODING REQUIREMENTS:
        1. REAL-WORLD DATA: If the file involves data fetching (Weather, Crypto, etc.), YOU MUST use the 'requests' library to call actual public APIs (e.g., CoinGecko, OpenWeather). DO NOT use mocks or fixed random values.
        2. SECURITY: Never hardcode API keys. Use `os.getenv()` and `load_dotenv()` from `python-dotenv`. Expect keys like 'PROJECT_API_KEY'.
        3. WEB DASHBOARD: If this is 'web_interface.py', use Streamlit for a premium-looking dashboard. 
        4. ERROR HANDLING: Implement robust try-except blocks, especially for network requests.
        5. STYLE: Pure Python 3.10+, zero-dependency except for streamlit, requests, and python-dotenv.

        OUTPUT: Return ONLY the raw code for '{filename}'. No markdown, no explanations.
        """
        return self.query(prompt)