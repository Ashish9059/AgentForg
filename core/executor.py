import subprocess
import os
import re
import sys
import time

class CodeExecutor:
    """
    V3.0 Smart Executor: Detects project types and launches them correctly.
    Supports standard Python scripts and Streamlit Web Apps.
    """
    def execute_project(self, project_name: str, entry_point_script: str = None):
        """
        Executes a project.
        """
        # Ensure we are looking into the workspace
        workspace = os.path.join("workspace", project_name)
        if not os.path.exists(workspace):
            print(f"[Executor] Error: Workspace '{workspace}' not found.")
            return (False, f"Workspace '{workspace}' does not exist.")
            
        # Determine Entry Point
        entry_file = entry_point_script or "web_interface.py"
        if not os.path.exists(os.path.join(workspace, entry_file)):
            # Fallback to main.py
            if os.path.exists(os.path.join(workspace, "main.py")):
                entry_file = "main.py"
            else:
                return (False, f"Entry point '{entry_file}' not found.")

        # Detect if it's a Streamlit app
        is_streamlit = False
        with open(os.path.join(workspace, entry_file), "r", encoding="utf-8") as f:
            if "import streamlit" in f.read():
                is_streamlit = True

        print(f"[Executor] Initializing {'Streamlit' if is_streamlit else 'Python'} execution for {entry_file}...")
        
        try:
            if is_streamlit:
                # Launch Streamlit in background (Popen) since it's a persistent server
                # We don't wait for it to finish.
                cmd = ["streamlit", "run", entry_file]
                process = subprocess.Popen(
                    cmd,
                    cwd=workspace,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                print(f"[Executor] 🌐 Streamlit Dashboard launched in background.")
                return (True, "Streamlit server started.")
            else:
                # Standard Python Script (Run and wait)
                res = subprocess.run(
                    [sys.executable, entry_file],
                    cwd=workspace,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                output = res.stdout + "\n" + res.stderr
                return (res.returncode == 0, output)
            
        except subprocess.TimeoutExpired:
            return (False, "Execution timed out (30s limit).")
        except Exception as e:
            print(f"[Executor] Critical Error: {e}")
            return (False, str(e))

executor = CodeExecutor()