#!/usr/bin/env powershell
# ========================================
# Titanic Survival Predictor - Start Script
# ========================================

Write-Host ""
Write-Host "🚢 Titanic Survival Predictor - Starting..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$scriptDir = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition

# Start Backend API
Write-Host "📍 Starting Flask API..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptDir'; python app.py"

# Wait for backend to start
Start-Sleep -Seconds 3

# Start Frontend
Write-Host "📍 Starting React Frontend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptDir\titanic-frontend'; npm run dev"

Write-Host ""
Write-Host "✅ Both servers are starting!" -ForegroundColor Green
Write-Host ""
Write-Host "🔗 Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host "🔗 API: http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Tip: Open frontend URL in your browser" -ForegroundColor Green
Write-Host ""
