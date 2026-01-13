from agents.architect import ArchitectAgent
from agents.coder import CoderAgent
from agents.reviewer import ReviewerAgent
from agents.tester import TesterAgent
from agents.deployer import DeployerAgent
from core.executor import CodeExecutor
from core.memory import memory
import time
import os
import ast

class ForgeOrchestrator:
    """
    V3.0 Production Orchestrator: Manages the Dynamic Swarm with an added 
    Optimization Refactor Loop and stability guardrails.
    """
    def __init__(self):
        self.architect = ArchitectAgent()
        self.coder = CoderAgent()
        self.reviewer = ReviewerAgent()
        self.tester = TesterAgent()
        self.deployer = DeployerAgent()
        self.executor = CodeExecutor()

    def _enforce_rate_limit(self):
        """Mandatory cooldown for Gemini Free Tier (5 RPM limit)."""
        time.sleep(10)

    def run_cycle(self, task_description: str):
        print(f"🚀 INITIATING MISSION V3.0: {task_description}")
        
        # 1. Classification (Router)
        mode = self._classify_task(task_description)
        print(f"Swarm Mode: {mode}")

        # 2. Planning
        print("\n[Architect] Mapping Neural Architecture...")
        plan = self.architect.plan_project(task_description)
        project_name = plan.get("project_name", "agent_project")
        project_dir = os.path.join("workspace", project_name)
        os.makedirs(project_dir, exist_ok=True)
        self._enforce_rate_limit()

        # 3. Build Loop (Sequential File Writing)
        for file_meta in plan.get("files", []):
            filename = file_meta['filename']
            self.autonomous_build_file(plan, filename, project_dir, mode)

        # 4. Expansion Phase (Complex Only)
        if mode == "COMPLEX":
            print("\n[Tester] Drafting Verification Suite...")
            tests = self.tester.generate_tests(plan, memory.get_project_context())
            self._save_file(project_dir, "test_suite.py", tests)
            self._enforce_rate_limit()

            print("\n[Deployer] Finalizing Deployment Protocol...")
            guide = self.deployer.generate_guide(plan, memory.get_project_context())
            self._save_file(project_dir, "DEPLOY.md", guide)
            self._enforce_rate_limit()

        # 5. Execution
        entry_point = plan.get("entry_point", "web_interface.py")
        print(f"\n[Executor] Launching {entry_point} in project '{project_name}'...")
        self.executor.execute_project(project_name=project_name, entry_point_script=entry_point)

    def autonomous_build_file(self, plan, filename, project_dir, mode):
        """Builds a file with self-healing and V3.0 Optimization Loop."""
        attempts = 0
        max_attempts = 3
        
        while attempts < max_attempts:
            print(f"   Writing {filename} (Attempt {attempts+1})...")
            context = memory.get_project_context()
            code = self.coder.write_code(str(plan), filename, context)
            code = self.coder.scrub_output(code)
            self._enforce_rate_limit()

            # Guardrail: Python Syntax Check
            if filename.endswith(".py"):
                try:
                    ast.parse(code)
                except SyntaxError as e:
                    print(f"   ⚠️ Syntax Error in {filename}: {e}. Retrying...")
                    attempts += 1
                    continue

            # Review & Optimization Loop (Force 1 Refactor in COMPLEX mode)
            if mode == "COMPLEX":
                print(f"   Analyzing Technical Debt for {filename}...")
                review_feedback = self.reviewer.review_code(code, filename)
                self._enforce_rate_limit()

                if "FIX:" in review_feedback:
                    print(f"   ♻️ Optimization Found: {review_feedback.strip()}")
                    print(f"   Refactoring {filename} for performance...")
                    code = self.coder.write_code(f"REFACTOR REQUEST: {review_feedback}\nORIGINAL PLAN: {plan}", filename, context)
                    code = self.coder.scrub_output(code)
                    self._enforce_rate_limit()

            self._save_file(project_dir, filename, code)
            memory.log_file(filename, code)
            break

    def _classify_task(self, task: str) -> str:
        """Determines if the swarm operates in Lean or Full mode."""
        # Simple heuristic or LLM call. Here we use a quick prompt.
        prompt = f"Categorize this task as 'SIMPLE' (single file script/CLI) or 'COMPLEX' (multi-file, web, or API). Task: {task}. Return ONLY 'SIMPLE' or 'COMPLEX'."
        from core.llm_client import llm_client
        res = llm_client.query(prompt)
        return "COMPLEX" if "COMPLEX" in res.upper() else "SIMPLE"

    def _save_file(self, dir_path, filename, content):
        path = os.path.join(dir_path, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

orchestrator = ForgeOrchestrator()