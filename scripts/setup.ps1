$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "=== myproject01 Windows Setup ==="
Write-Host ""

# 1. Check Python
try {
    python --version | Out-Null
} catch {
    Write-Host "Python not found."
    Write-Host "Install Python 3.11+ from https://python.org"
    Write-Host "IMPORTANT: Check 'Add Python to PATH'"
    exit 1
}

# 2. Create virtual environment if missing
if (-not (Test-Path ".\.venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
} else {
    Write-Host "Virtual environment already exists."
}

# 3. Activate venv
Write-Host "Activating virtual environment..."
& .\.venv\Scripts\Activate.ps1

# 4. Upgrade pip
Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

# 5. Install dependencies
Write-Host "Installing dependencies..."
pip install -r requirements.txt

# 6. Create .env if missing
if (-not (Test-Path ".\.env")) {
    if (Test-Path ".\.env.example") {
        Copy-Item ".\.env.example" ".\.env"
        Write-Host ".env created from .env.example"
        Write-Host "Edit .env if you want to enable Telegram."
    }
}

# 7. Create runtime folders
New-Item -ItemType Directory -Force -Path ".\runtime\db" | Out-Null
New-Item -ItemType Directory -Force -Path ".\runtime\logs" | Out-Null
New-Item -ItemType Directory -Force -Path ".\runtime\exports" | Out-Null

Write-Host ""
Write-Host "Setup complete."
Write-Host "Run the project with: .\scripts\run.ps1"
Write-Host ""