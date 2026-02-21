$ErrorActionPreference = "Stop"

if (-not (Test-Path ".\.venv\Scripts\Activate.ps1")) {
    Write-Host "Virtual environment not found."
    Write-Host "Run: .\scripts\setup.ps1 first."
    exit 1
}

& .\.venv\Scripts\Activate.ps1

python main.py