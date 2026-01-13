from .base_agent import BaseAgent

class ReviewerAgent(BaseAgent):
    """
    V3.0 Senior Code Reviewer: Performs technical debt analysis and forces 
    at least one mandatory performance or syntax optimization pass.
    """
    def review_code(self, code: str, filename: str):
        prompt = f"""
        You are a Senior Code Reviewer focusing on Performance and Technical Debt.
        Analyze the following code for '{filename}':

        --- CODE START ---
        {code}
        --- CODE END ---

        V3.0 REVIEW PROTOCOL:
        1. SYNTAX: Ensure no errors (logical or PEP 8).
        2. TECHNICAL DEBT: Identify one mandatory optimization (e.g., 'Using List Comprehension', 'Reducing redundant API calls', 'Global variable removal').
        3. BSF COMPLIANCE: Ensure it fits the Backend-Service-Frontend pattern.

        OUTPUT: 
        - If the code is perfect and no optimization is needed (rare), return "PASSED".
        - Otherwise, provide a concise critique and start your response with "FIX: [Optimization Suggestion]".
        Explain EXACTLY what needs to change to reduce technical debt.
        """
        return self.query(prompt)