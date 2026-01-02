param(
    [ValidateSet("start", "stop", "status")]
    [string]$Action = "start",
    [ValidateSet("all", "adsim", "insight", "interactive")]
    [string]$Mode = "interactive"
)

$ErrorActionPreference = "Stop"
$rootPath = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path -replace '\\', '/'

function Show-Intro {
    Write-Host ""
    Write-Host "Adsim Launcher" -ForegroundColor Cyan
    Write-Host "1) Generate a research report in Adsim Insight"
    Write-Host "2) Upload the report as Adsim seed file on Home"
    Write-Host "3) Enter prompt to run prediction/simulation"
    Write-Host ""
}

function Show-Endpoints {
    Write-Host ""
    Write-Host "Web Endpoints" -ForegroundColor Cyan
    Write-Host "Adsim Frontend   : http://localhost:3000"
    Write-Host "Adsim Backend    : http://localhost:5001"
    Write-Host "Insight Flask    : http://localhost:5000"
    Write-Host "Insight Streamlit: http://localhost:8501"
    Write-Host ""
}

function Choose-Mode {
    Write-Host ""
    Write-Host "Select start mode:" -ForegroundColor Cyan
    Write-Host "1) Start Adsim + Adsim Insight"
    Write-Host "2) Start Adsim only"
    Write-Host "3) Start Adsim Insight only"
    Write-Host "4) Status only"
    Write-Host "5) Stop services"
    $choice = Read-Host "Enter 1-5"
    switch ($choice) {
        "1" { return @("start", "all") }
        "2" { return @("start", "adsim") }
        "3" { return @("start", "insight") }
        "4" { return @("status", "all") }
        "5" { return @("stop", "all") }
        default { return @("start", "all") }
    }
}

function Test-Command {
    param([string]$Name)
    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

function Test-DockerDaemon {
    if (-not (Test-Command -Name "docker")) {
        return $false
    }
    try {
        docker info | Out-Null
        return $true
    } catch {
        return $false
    }
}

function Test-Port {
    param([int]$Port)
    $conn = Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue
    return $null -ne $conn
}

function Test-EnvFile {
    param([string]$Path)
    return (Test-Path -Path $Path)
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

if ($Mode -eq "interactive") {
    Show-Intro
    $selection = Choose-Mode
    $Action = $selection[0]
    $Mode = $selection[1]
}

if ($Action -eq "status") {
    Show-PortStatus -Ports @(3000, 5001, 5000, 8501, 8502, 8503)
    Show-Endpoints
    return
}

if ($Action -eq "stop") {
    if (Test-DockerDaemon) {
        Push-Location "$rootPath"
        docker compose -f "$rootPath/docker-compose.bettafish.yml" down
        Pop-Location
    } else {
        Write-Host "Docker Desktop is not running. Skip Adsim Insight stop." -ForegroundColor Yellow
    }
    Write-Host "Close the Adsim devserver window(s) to stop npm run dev." -ForegroundColor Yellow
    Show-Endpoints
    return
}

Write-Host "Checking ports..." -ForegroundColor Cyan
Show-PortStatus -Ports @(3000, 5001, 5000, 8501, 8502, 8503)

if ($Mode -in @("all", "adsim")) {
    if (Test-Command -Name "npm") {
        $adsimEnv = "$rootPath/.env"
        if (-not (Test-EnvFile -Path $adsimEnv)) {
            Write-Host "Adsim .env not found. Copy .env.example and fill keys if needed:" -ForegroundColor Yellow
            Write-Host "Copy-Item `"$rootPath/.env.example`" `"$rootPath/.env`""
        }
        Write-Host "Starting Adsim (frontend + backend)..." -ForegroundColor Cyan
        $adsimCmd = "cd `"$rootPath`"; npm run dev"
        Start-Process powershell -ArgumentList "-NoExit", "-Command", $adsimCmd
    } else {
        Write-Host "npm not found. Skip Adsim start." -ForegroundColor Yellow
    }
}

if ($Mode -in @("all", "insight")) {
    if (Test-DockerDaemon) {
        $insightEnv = "$rootPath/third_party/BettaFish/.env"
        if (-not (Test-EnvFile -Path $insightEnv)) {
            Write-Host "Adsim Insight .env not found. Copy .env.example and fill API keys:" -ForegroundColor Yellow
            Write-Host "Copy-Item `"$rootPath/third_party/BettaFish/.env.example`" `"$rootPath/third_party/BettaFish/.env`""
            Write-Host "Skip Adsim Insight start." -ForegroundColor Yellow
            return
        }
        Write-Host "Starting Adsim Insight (based on BettaFish) via Docker Compose..." -ForegroundColor Cyan
        Push-Location "$rootPath"
        docker compose -f "$rootPath/docker-compose.bettafish.yml" up -d
        Pop-Location
    } else {
        Write-Host "Docker Desktop is not running. Start Docker Desktop and press Enter to retry." -ForegroundColor Yellow
        Read-Host "Press Enter after Docker Desktop is running"
        if (Test-DockerDaemon) {
            Write-Host "Starting Adsim Insight (based on BettaFish) via Docker Compose..." -ForegroundColor Cyan
            Push-Location "$rootPath"
            docker compose -f "$rootPath/docker-compose.bettafish.yml" up -d
            Pop-Location
        } else {
            Write-Host "Docker Desktop is still not running. Skip Adsim Insight start." -ForegroundColor Yellow
        }
    }
}

Write-Host "Done. Check ports: Adsim 3000/5001, Adsim Insight 5000/8501/8502/8503" -ForegroundColor Green
Show-Endpoints
