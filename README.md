# AgentForge v3.0: The Production Suite 🛸🤖

**AgentForge** is an advanced agentic swarm orchestrator designed to build professional, multi-file web applications and API integrations autonomously. Version 3.0, "Web & API Professional," introduces a high-performance frontend architecture and real-world connectivity.

---

## 🚀 Key Features (v3.0)

### 🛰️ Mission Control Dashboard
A pro-grade UI built with `CustomTkinter` featuring:
- **Matrix Logs**: Real-time streaming of swarm activity.
- **Live Architecture**: A dynamic pane showing the project structure as it evolves.
- **Dependency Registry**: Automated tracking of external libraries (e.g., `streamlit`, `pandas`).
- **Workspace Explorer**: Integrated file tree and code viewer for immediate inspection.

### 🌐 Web-First Swarm Architecture
- **ArchitectAgent**: Enforces a strict **Backend-Service-Frontend (BSF)** pattern.
- **CoderAgent**: Prioritizes live data using the `requests` library and secure API key management via `.env`.
- **ReviewerAgent**: Performs **Technical Debt Analysis**, suggesting and enforcing performance optimizations.

### 🛡️ Production Guardrails
- **Self-Healing Loop**: Automatic AST syntax checking and repair.
- **Rate-Limit Intelligence**: Exponential backoff (429 handling) for Gemini Free Tier stability.
- **Safe Execution**: Background detection and launching for Streamlit web apps.

---

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Ashish9059/AgentForg.git
cd AgentForg
```

### 2. Setup Virtual Environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

---

## 🖥️ Usage

1. **Launch the Dashboard**:
   ```bash
   .\run.bat
   ```
2. **Configure API Key**: Enter your Google Gemini API Key in the sidebar "Security Token" field.
3. **Start a Mission**: Enter an objective (e.g., *"Build a Real-Time Crypto Sentinel Dashboard using Streamlit"*) and click **Start Mission**.

---

## 🏗️ Architecture [V3.0]

| Component | Responsibility |
| :--- | :--- |
| **Orchestrator** | Manages the dynamic swarm routing and refactor loops. |
| **Architect** | Designs the BSF structure and plans the filesystem. |
| **Coder** | Generates production-grade, file-aware Python code. |
| **Reviewer** | Audits code for technical debt and performance. |
| **Executor** | Safely launches scripts and web servers in isolated workspaces. |

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

*Built with Agentic Coding Excellence.*
