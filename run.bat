@echo off
cd /d "%~dp0"
call venv\Scripts\activate
echo Starting AgentForge...
venv\Scripts\python.exe main.py
pause