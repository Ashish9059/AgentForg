import customtkinter as ctk
import threading
import sys
import os
import json
from datetime import datetime

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.orchestrator import orchestrator
from core.memory import memory
from core.llm_client import llm_client 

# --- MISSION CONTROL THEME (v3.0) ---
# Palette: High-Contrast "Deep Space"
THEME = {
    "bg_dark": "#0B0E14",      # Deeper Space
    "bg_panel": "#151921",     # Solid Panel
    "bg_input": "#1C212B",     # Input Field
    "primary": "#00FF41",      # Matrix Green
    "secondary": "#58A6FF",    # Tech Blue
    "accent": "#FF3366",       # Alert Red
    "text_main": "#E6EDF3",    # Clean White
    "text_dim": "#7D8590",     # Faded Grey
    "border": "#30363D",       # Subtle Border
    "log_bg": "#000000"        # True Black
}

ctk.set_appearance_mode("Dark")

class AgentForgeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AgentForge v3.0 [Mission Control]")
        self.geometry("1400x900")
        self.configure(fg_color=THEME["bg_dark"])

        # Layout Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._create_sidebar()
        self._create_main_tabs()

        # Redirect stdout
        sys.stdout = PrintLogger(self.log_textbox)

    def _create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color=THEME["bg_panel"], border_width=1, border_color=THEME["border"])
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1)

        # 1. Dashboard Header
        self.header = ctk.CTkLabel(self.sidebar, text="AGENTFORGE", font=ctk.CTkFont(family="Inter", size=24, weight="bold"), text_color=THEME["secondary"])
        self.header.grid(row=0, column=0, padx=20, pady=(30, 0))
        
        self.sub_header = ctk.CTkLabel(self.sidebar, text="v3.0 PRODUCTION SUITE", font=ctk.CTkFont(family="Consolas", size=10), text_color=THEME["text_dim"])
        self.sub_header.grid(row=1, column=0, padx=20, pady=(0, 20))

        # 2. Swarm Status
        self.status_box = ctk.CTkFrame(self.sidebar, fg_color=THEME["bg_dark"], corner_radius=8, border_width=1, border_color=THEME["border"])
        self.status_box.grid(row=2, column=0, padx=15, pady=10, sticky="ew")
        
        self.status_dot = ctk.CTkLabel(self.status_box, text="●", font=("Arial", 20), text_color=THEME["text_dim"])
        self.status_dot.grid(row=0, column=0, padx=(10, 5), pady=10)
        
        self.status_msg = ctk.CTkLabel(self.status_box, text="STANDBY", font=("Inter", 12, "bold"), text_color=THEME["text_dim"])
        self.status_msg.grid(row=0, column=1, padx=5, pady=10)

        # 3. Credentials
        ctk.CTkLabel(self.sidebar, text="SECURITY TOKEN", font=("Inter", 10, "bold"), text_color=THEME["text_dim"]).grid(row=3, column=0, padx=25, pady=(20, 5), sticky="w")
        self.api_key = ctk.CTkEntry(self.sidebar, placeholder_text="Enter Gemini Key...", show="*", height=35, fg_color=THEME["bg_input"], border_color=THEME["border"])
        self.api_key.grid(row=4, column=0, padx=20, pady=0, sticky="ew")
        
        if os.getenv("GOOGLE_API_KEY"):
            self.api_key.insert(0, os.getenv("GOOGLE_API_KEY"))

        # 4. Swarm Controls
        self.launch_btn = ctk.CTkButton(
            self.sidebar, 
            text="START MISSION", 
            command=self.execute_mission, 
            height=45, 
            fg_color="#238636", # GitHub Green
            font=("Inter", 13, "bold"),
            hover_color="#2ea043"
        )
        self.launch_btn.grid(row=5, column=0, padx=20, pady=25, sticky="ew")

        # 5. Live Metrics Tracker
        self.metrics_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.metrics_frame.grid(row=6, column=0, padx=20, pady=10, sticky="ew")
        
        self.dep_title = ctk.CTkLabel(self.metrics_frame, text="DYNAMIC DEPENDENCIES", font=("Inter", 10, "bold"), text_color=THEME["secondary"])
        self.dep_title.pack(anchor="w")
        
        self.dep_list = ctk.CTkLabel(self.metrics_frame, text="Pending execution...", font=("Consolas", 11), text_color=THEME["text_dim"], justify="left", wraplength=220)
        self.dep_list.pack(anchor="w", pady=5)

        # Progress Section
        self.progress = ctk.CTkProgressBar(self.sidebar, mode="indeterminate", height=6, progress_color=THEME["secondary"])
        # Grid it when active

    def _create_main_tabs(self):
        self.tabs = ctk.CTkTabview(
            self, 
            fg_color="transparent",
            segmented_button_fg_color=THEME["bg_panel"],
            segmented_button_selected_color=THEME["secondary"],
            segmented_button_unselected_hover_color=THEME["border"]
        )
        self.tabs.grid(row=0, column=1, padx=15, pady=10, sticky="nsew")
        
        self.tab_ctrl = self.tabs.add("MISSION CONTROL")
        self.tab_work = self.tabs.add("WORKSPACE")
        self.tab_guide = self.tabs.add("DEPLOY GUIDE")
        self.tab_brain = self.tabs.add("PROJECT BRAIN")

        # --- MISSION CONTROL TAB (Dual Pane) ---
        self.tab_ctrl.grid_columnconfigure(0, weight=3) # Logs
        self.tab_ctrl.grid_columnconfigure(1, weight=2) # Summary Card
        self.tab_ctrl.grid_rowconfigure(1, weight=1)

        # Top: Objective Input
        self.input_box = ctk.CTkTextbox(self.tab_ctrl, height=80, fg_color=THEME["bg_panel"], border_width=1, border_color=THEME["border"], font=("Inter", 15))
        self.input_box.grid(row=0, column=0, columnspan=2, padx=0, pady=(0, 15), sticky="ew")
        self.input_box.insert("1.0", "Enter mission objective...")

        # Left: Matrix Console
        self.log_textbox = ctk.CTkTextbox(self.tab_ctrl, fg_color=THEME["log_bg"], text_color=THEME["primary"], font=("Consolas", 13), border_width=1, border_color=THEME["border"])
        self.log_textbox.grid(row=1, column=0, padx=(0, 10), pady=0, sticky="nsew")

        # Right: Project Summary Card
        self.summary_card = ctk.CTkFrame(self.tab_ctrl, fg_color=THEME["bg_panel"], border_width=1, border_color=THEME["border"])
        self.summary_card.grid(row=1, column=1, padx=0, pady=0, sticky="nsew")
        
        ctk.CTkLabel(self.summary_card, text="LIVE ARCHITECTURE", font=("Inter", 14, "bold"), text_color=THEME["secondary"]).pack(pady=15)
        
        self.plan_view = ctk.CTkTextbox(self.summary_card, fg_color="transparent", text_color=THEME["text_main"], font=("Consolas", 11), state="disabled")
        self.plan_view.pack(fill="both", expand=True, padx=10, pady=5)

        # --- WORKSPACE TAB ---
        self.tab_work.grid_columnconfigure(0, weight=1)
        self.tab_work.grid_columnconfigure(1, weight=4)
        self.tab_work.grid_rowconfigure(0, weight=1)

        self.explorer = ctk.CTkScrollableFrame(self.tab_work, label_text="PROJECT FILES", fg_color=THEME["bg_panel"])
        self.explorer.grid(row=0, column=0, padx=(0,10), pady=0, sticky="nsew")

        self.editor = ctk.CTkTextbox(self.tab_work, fg_color="#1E1E1E", text_color="#D4D4D4", font=("Consolas", 14), wrap="none")
        self.editor.grid(row=0, column=1, sticky="nsew")

        # --- GUIDE TAB ---
        self.guide_view = ctk.CTkTextbox(self.tab_guide, fg_color=THEME["bg_panel"], font=("Inter", 14))
        self.guide_view.pack(fill="both", expand=True)

        # --- BRAIN TAB ---
        self.brain_view = ctk.CTkTextbox(self.tab_brain, fg_color=THEME["bg_panel"], font=("Consolas", 11), text_color=THEME["text_dim"])
        self.brain_view.pack(fill="both", expand=True)

    def execute_mission(self):
        objective = self.input_box.get("1.0", "end").strip()
        if not objective or objective == "Enter mission objective...": return

        key = self.api_key.get().strip()
        if not key and not os.getenv("GOOGLE_API_KEY"):
            print("❌ AUTH ERROR: System requires a valid API Token.")
            return

        if key and not llm_client.model:
            llm_client.initialize(key)

        # UI Visual Lock
        self.launch_btn.configure(state="disabled", text="MISSION ACTIVE", fg_color=THEME["bg_panel"])
        self.status_dot.configure(text_color=THEME["secondary"])
        self.status_msg.configure(text="PROCESSING", text_color=THEME["secondary"])
        self.progress.grid(row=7, column=0, padx=20, pady=10, sticky="ew")
        self.progress.start()

        threading.Thread(target=self._run_swarm, args=(objective,), daemon=True).start()

    def _run_swarm(self, objective):
        try:
            orchestrator.run_cycle(objective)
            print("\n>> MISSION ACCOMPLISHED.")
            self.after(0, self.update_visuals)
        except Exception as e:
            print(f"CRITICAL MISSION FAILURE: {e}")
        finally:
            self.after(0, self._reset_ui)

    def _reset_ui(self):
        self.launch_btn.configure(state="normal", text="START MISSION", fg_color="#238636")
        self.status_dot.configure(text_color=THEME["text_dim"])
        self.status_msg.configure(text="STANDBY", text_color=THEME["text_dim"])
        self.progress.stop()
        self.progress.grid_forget()

    def update_visuals(self):
        # Update dependencies list
        self.sync_memory()
        
        # Update plan view
        self.plan_view.configure(state="normal")
        self.plan_view.delete("1.0", "end")
        self.plan_view.insert("1.0", memory.get_project_context())
        self.plan_view.configure(state="disabled")

        # Update Brain
        self.refresh_brain()

        # Update Deploy
        self.load_explorer()

    def load_explorer(self):
        for w in self.explorer.winfo_children(): w.destroy()
        
        ws = "workspace"
        if not os.path.exists(ws): return
        subs = [os.path.join(ws, d) for d in os.listdir(ws) if os.path.isdir(os.path.join(ws, d))]
        if not subs: return
        
        latest = max(subs, key=os.path.getmtime)
        self.explorer.configure(label_text=os.path.basename(latest).upper())
        
        files = os.listdir(latest)
        for f in files:
            if os.path.isfile(os.path.join(latest, f)):
                ctk.CTkButton(self.explorer, text=f, anchor="w", fg_color="transparent", hover_color=THEME["border"], 
                             command=lambda path=os.path.join(latest, f): self.open_file(path)).pack(fill="x")

    def open_file(self, path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            self.editor.delete("1.0", "end")
            self.editor.insert("1.0", content)

    def refresh_brain(self):
        self.brain_view.configure(state="normal")
        self.brain_view.delete("1.0", "end")
        summary = f"NEURAL BRAIN SYNC: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        summary += "-"*40 + "\n"
        summary += f"Active Project Blobs: {len(memory.project_files)}\n"
        summary += f"Dependency Registry: {len(memory.get_dependencies())} registered\n"
        summary += "-"*40 + "\n"
        for dep in memory.get_dependencies():
            summary += f" [DEP] -> {dep}\n"
        self.brain_view.insert("1.0", summary)
        self.brain_view.configure(state="disabled")
    
    def sync_memory(self):
        deps = memory.get_dependencies()
        if deps:
            self.dep_list.configure(text=", ".join(deps).upper(), text_color=THEME["primary"])
        else:
            self.dep_list.configure(text="None detected.", text_color=THEME["text_dim"])

class PrintLogger:
    def __init__(self, widget): self.widget = widget
    def write(self, text):
        self.widget.configure(state="normal")
        self.widget.insert("end", text)
        self.widget.see("end")
        self.widget.configure(state="disabled")
    def flush(self): pass

if __name__ == "__main__":
    app = AgentForgeApp()
    app.mainloop()