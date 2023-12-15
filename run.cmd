@echo off
echo pls be patient...

if not exist ".venv" (
    py -m venv .venv
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt 
) else (
    call .venv\Scripts\activate.bat
)   
py main.py