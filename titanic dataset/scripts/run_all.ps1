# Titanic Survival Predictor - Startup Script
Write-Host "================================================" -ForegroundColor Gold
Write-Host "   🚀 TITANIC SURVIVAL PREDICTOR STARTUP   " -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Gold

# 1. Start the Flask Backend in a new window
Write-Host "🔄 Starting Flask Backend (app.py)..." -ForegroundColor Yellow
$BackendDir = Join-Path $PSScriptRoot "..\backend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$BackendDir'; python app.py"

# 2. Wait for backend to initialize
Write-Host "⏳ Waiting for API to warm up..." -ForegroundColor Gray
Start-Sleep -s 3

# 3. Open the Frontend
$FrontendPath = Join-Path $PSScriptRoot "..\frontend\index.html"
Write-Host "🌐 Opening Frontend UI in default browser..." -ForegroundColor Green
Start-Process $FrontendPath

Write-Host "`n✅ System is now running!" -ForegroundColor Green
Write-Host "• Backend: http://localhost:5000"
Write-Host "• Frontend: $FrontendPath"
Write-Host "------------------------------------------------"
