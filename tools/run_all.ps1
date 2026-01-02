param(
    [ValidateSet("start", "stop", "status")]
    [string]$Action = "start",
    [switch]$SkipBettaFish
)

$ErrorActionPreference = "Stop"
$rootPath = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path -replace '\\', '/'

function Test-Command {
    param([string]$Name)
    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

function Test-Port {
    param([int]$Port)
    $conn = Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue
    return $null -ne $conn
}

function Show-PortStatus {
    param([int[]]$Ports)
    foreach ($port in $Ports) {
        if (Test-Port -Port $port) {
            Write-Host "Port $port is already in use." -ForegroundColor Yellow
        } else {
            Write-Host "Port $port is free." -ForegroundColor Green
        }
    }
}

if ($Action -eq "status") {
    Show-PortStatus -Ports @(3000, 5001, 5000, 8501, 8502, 8503)
    return
}

if ($Action -eq "stop") {
    if (Test-Command -Name "docker") {
        Push-Location "$rootPath"
        docker compose -f "$rootPath/docker-compose.bettafish.yml" down
        Pop-Location
    } else {
        Write-Host "Docker not found. Skip Adsim Insight stop." -ForegroundColor Yellow
    }
    Write-Host "Close the Adsim devserver window(s) to stop npm run dev." -ForegroundColor Yellow
    return
}

Write-Host "Checking ports..." -ForegroundColor Cyan
Show-PortStatus -Ports @(3000, 5001, 5000, 8501, 8502, 8503)

if (Test-Command -Name "npm") {
    Write-Host "Starting Adsim (frontend + backend)..." -ForegroundColor Cyan
    $adsimCmd = "cd `"$rootPath`"; npm run dev"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $adsimCmd
} else {
    Write-Host "npm not found. Skip Adsim start." -ForegroundColor Yellow
}

if (-not $SkipBettaFish) {
    if (Test-Command -Name "docker") {
        Write-Host "Starting Adsim Insight (based on BettaFish) via Docker Compose..." -ForegroundColor Cyan
        Push-Location "$rootPath"
        docker compose -f "$rootPath/docker-compose.bettafish.yml" up -d
        Pop-Location
    } else {
        Write-Host "Docker not found. Skip Adsim Insight start." -ForegroundColor Yellow
    }
}

Write-Host "Done. Check ports: Adsim 3000/5001, Adsim Insight 5000/8501/8502/8503" -ForegroundColor Green
