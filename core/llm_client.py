import os
import warnings
# Suppress Google Generative AI deprecation warnings for cleaner v3.0 console
warnings.filterwarnings("ignore", category=FutureWarning)

import google.generativeai as genai
from typing import Optional, Callable

class LLMClient:
    def __init__(self):
        # Setup Gemini
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.model = None

        if self.google_api_key:
            self.initialize(self.google_api_key)
        else:
             print("Warning: GOOGLE_API_KEY is missing. Please set it in sidebar.")

    def initialize(self, api_key: str):
        """
        Initializes or re-initializes the Gemini model with a new key.
        """
        try:
            # SANITIZATION: Remove whitespace, newlines, and quotes
            self.google_api_key = api_key.strip().replace('\n', '').replace('\r', '').replace('"', '').replace("'", "")
            
            if not self.google_api_key:
                 print("Error: Empty API Key provided.")
                 return False

            print(f"[DEBUG] Config Key: {self.google_api_key[:5]}...{self.google_api_key[-3:]} (Len: {len(self.google_api_key)})")
            
            genai.configure(api_key=self.google_api_key)
            
            # DEBUG: List models to console
            print("\n[DEBUG] Listing Available Gemini Models:")
            try:
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        print(f" - {m.name}")
            except Exception as e:
                print(f" [DEBUG] Could not list models: {e}")
            print("----------------------------------------\n")

            self.safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE",
                },
            ]
            
            self.model = genai.GenerativeModel(
                model_name='gemini-2.5-flash',
                safety_settings=self.safety_settings
            )
            print("Message: Gemini Client Initialized Successfully (Default: gemini-2.5-flash).")
            return True
        except Exception as e:
            print(f"Error initializing Gemini: {e}")
            self.model = None
            return False

    def query(self, user_prompt: str, system_prompt: str = "You are a helpful AI software assistant.", callback: Callable[[str], None] = None) -> str:
        """
        Queries Gemini 1.5/2.5 Pro.
        Supports streaming via callback(token).
        """
        if not self.model:
            return "Error: Gemini Client not initialized (Missing Key)."

        try:
            # Gemini 1.5/2.5 style combination of prompts
            combined_prompt = f"System Instruction: {system_prompt}\n\nUser Task: {user_prompt}"
            
            # Smart Fallback Logic for Next-Gen Models
            primary_name = self.model._model_name.split("/")[-1]
            fallbacks = []
            
            # If on bleeding edge (2.5/3.0), fall back to stable flash or other previews
            if "2.5-pro" in primary_name:
                fallbacks = ["gemini-2.5-flash", "models/gemini-2.0-flash", "gemini-1.5-flash"]
            elif "2.5-flash" in primary_name:
                fallbacks = ["models/gemini-2.0-flash", "gemini-1.5-flash"]
            elif "1.5-pro" in primary_name: # Legacy path if they switch back
                fallbacks = ["gemini-1.5-flash"]
            
            # Attempt generation
            try:
                return self._generate(self.model, combined_prompt, callback)
            except Exception as e:
                error_str = str(e)
                if "404" in error_str or "not found" in error_str:
                     # Only fallback on 404s (model missing), NOT on 429s (handled by _generate retry)
                    print(f"⚠️ Primary model ({primary_name}) failed. Attempting fallbacks...")
                    for model_name in fallbacks:
                        try:
                            print(f"🔄 Switching to {model_name}...")
                            fallback_model = genai.GenerativeModel(
                                model_name=model_name,
                                safety_settings=self.safety_settings
                            )
                            # Update self.model so subsequent calls use the working one
                            self.model = fallback_model 
                            return self._generate(fallback_model, combined_prompt, callback)
                        except Exception as fallback_e:
                            print(f"❌ {model_name} failed: {fallback_e}")
                            continue
                # If all fallbacks fail or it's a different error, re-raise
                raise e

        except Exception as e:
            return f"Error querying Gemini: {str(e)}"

    def _generate(self, model, prompt, callback):
        import time
        max_retries = 5 # Increased for safety
        
        for attempt in range(max_retries):
            try:
                full_response = ""
                response = model.generate_content(prompt, stream=True)
                for chunk in response:
                    if chunk.text:
                        token = chunk.text
                        if callback:
                            callback(token)
                        full_response += token
                return full_response
                
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "Quota exceeded" in error_str:
                    wait_time = (attempt + 1) * 20 # Wait 20s, 40s, 60s, 80s, 100s
                    print(f"\n⚠️ Rate Limit Hit (429). Waiting {wait_time}s before retry ({attempt+1}/{max_retries})...")
                    time.sleep(wait_time)
                    continue # Retry loop
                elif "503" in error_str:
                    time.sleep(5)
                    continue
                else:
                    raise e # Non-retriable error
        
        raise Exception("Max retries exceeded for Rate Limit (429).")

# Singleton instance
llm_client = LLMClient()