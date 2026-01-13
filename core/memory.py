import os
import re

class ProjectMemory:
    """
    V3.0 Context Engine: Tracks project evolution, cross-file dependencies, 
    and external libraries (API Registry).
    """
    def __init__(self):
        self.project_files = {}
        self.summary = ""
        self.external_dependencies = set()

    def log_file(self, filename: str, content: str):
        self.project_files[filename] = content
        # API Registry: Track new imports
        imports = re.findall(r"^(?:import|from) (\S+)", content, re.MULTILINE)
        for imp in imports:
            clean_imp = imp.split(".")[0]
            # Ignore standard library (simplistic filter)
            if clean_imp not in ["os", "sys", "json", "time", "datetime", "math", "re", "unittest", "uuid", "abc"]:
                self.external_dependencies.add(clean_imp)

    def get_project_context(self):
        context = "Project Structure & Memory:\n"
        for fname, content in self.project_files.items():
            context += f"--- FILE: {fname} ---\n{content[:500]}...\n\n"
        
        if self.external_dependencies:
            context += f"EXTERNAL DEPENDENCIES DETECTED: {', '.join(self.external_dependencies)}\n"
        
        return context

    def get_dependencies(self):
        return list(self.external_dependencies)

    def clear(self):
        self.project_files = {}
        self.external_dependencies = set()

memory = ProjectMemory()
