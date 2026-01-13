from core.llm_client import llm_client
import re

class BaseAgent:
    """
    Base class for all agents in AgentForge v3.0.
    Provides common LLM query interface and output cleaning utilities.
    """
    def __init__(self, role: str = "Assistant"):
        self.role = role

    def query(self, prompt: str, system_prompt: str = None) -> str:
        """
        Wraps the llm_client query for streamlined usage.
        """
        if system_prompt:
            return llm_client.query(prompt, system_prompt)
        return llm_client.query(prompt)

    def scrub_output(self, text: str) -> str:
        """
        Removes known LLM hallucinations and 'noise' tokens from the output.
        """
        noise_tokens = [
            "<|begin_of_text|>",
            "<|start_header_id|>",
            "<|end_header_id|>",
            "<|eot_id|>",
            "<｜begin▁of▁sentence｜>",
            "</s>",
            "markdown>",
            "**Here is the code**",
            "I will now provide the solution",
        ]
        
        cleaned_text = text
        for token in noise_tokens:
            cleaned_text = cleaned_text.replace(token, "")
            
        return cleaned_text.strip()