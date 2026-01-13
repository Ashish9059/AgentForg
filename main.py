import sys
import os

# 1. Path Setup
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    print("Checking dependencies...")
    import customtkinter as ctk
    from ui.app import AgentForgeApp
    print("Starting GUI...")
    app = AgentForgeApp()
    app.mainloop()
except Exception as e:
    # THIS WILL PRINT THE EXACT REASON IT WONT OPEN
    print("\n" + "="*50)
    print("CRITICAL LAUNCH ERROR:")
    print(e)
    print("="*50)
    import traceback
    traceback.print_exc()
    input("\nPress Enter to close...")