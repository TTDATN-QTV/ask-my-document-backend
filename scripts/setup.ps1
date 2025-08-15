# scripts/setup.ps1
# ====================================================================
# Script to prepare the FastAPI development environment
# Can be run from anywhere; will switch to project root automatically.
# ====================================================================

Write-Host "Starting environment setup..." -ForegroundColor Cyan

# 0. Move to project root (one level up from scripts/)
Set-Location "$PSScriptRoot\.."

# 1. Create virtual environment
python -m venv .venv

# 2. Allow running scripts for this session
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

# 3. Activate the virtual environment
. .\.venv\Scripts\Activate.ps1

# 4. (Optional) Upgrade pip
python -m pip install --upgrade pip

# 5. Install dependencies
pip install -r requirements.txt

# 6. Set environment variable for the current session
$env:APP_ENV = "test"

Write-Host "Environment setup completed! APP_ENV=$env:APP_ENV" -ForegroundColor Green

# 7. (Optional) Start FastAPI server in development mode
Write-Host "Starting FastAPI server..." -ForegroundColor Yellow
uvicorn app.main:app --reload
