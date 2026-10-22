$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$rehearsalPython = Join-Path $PSScriptRoot '..\.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $rehearsalPython)) {
    $rehearsalPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
    if (-not (Test-Path -LiteralPath $rehearsalPython)) {
        python -m venv .venv
        & $rehearsalPython -m pip install -r requirements.txt
    }
}
Write-Host 'Open http://127.0.0.1:8766 and choose Experience the sample. Keep this window open.'
& $rehearsalPython server.py
