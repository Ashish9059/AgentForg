from .base_agent import BaseAgent

class TesterAgent(BaseAgent):
    """
    V3.0 QA Engineer: Generates comprehensive test suites for projects.
    """
    def generate_tests(self, plan: dict, project_context: str):
        project_name = plan.get("project_name", "agent_project")
        
        prompt = f"""
        You are a QA Automation Engineer for AgentForge v3.0.
        Your goal is to write a comprehensive 'test_suite.py' using Python's `unittest` framework.

        PROJECT PLAN: {plan}
        PROJECT CONTEXT:
        {project_context}

        INSTRUCTIONS:
        1. Analyze the project logic and structure.
        2. Write tests covering at least 3 happy paths and 2 edge cases.
        3. Ensure the test file can run standalone within the project directory.
        4. Mock external APIs if necessary, or test the service logic.

        OUTPUT: Return ONLY the raw Python code for 'test_suite.py'.
        """
        
        print("[Tester] Analysing code coverage...")
        code = self.query(prompt)
        clean_code = self.scrub_output(code)
        
        return clean_code
