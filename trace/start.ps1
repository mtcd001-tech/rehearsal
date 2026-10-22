$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
if (-not (Test-Path -LiteralPath '.venv\Scripts\python.exe')) {
    python -m venv .venv
    & '.venv\Scripts\python.exe' -m pip install -r requirements-lock.txt
}
Write-Host 'Trace is opening at http://127.0.0.1:8765. Keep this terminal open.'
& '.venv\Scripts\python.exe' server.py
