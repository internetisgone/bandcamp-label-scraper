@echo off
echo pls be patient...

py -m venv .venv
call .venv\Scripts\activate.bat
pip install requests
pip install beautifulsoup4
py main.py