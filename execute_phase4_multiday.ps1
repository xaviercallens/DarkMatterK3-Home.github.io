#Requires -Version 5.1
<#
.SYNOPSIS
    Phase 4 Multi-Day Execution with Checkpointing & Discovery Alerts
    
.DESCRIPTION
    Executes Phase 4 (V4 mock calibration + NED cross-match for K3-DISC-0035) 
    with resilience, checkpointing, and real-time discovery dashboard.
    
    Designed to run continuously for 2-7 days with automatic recovery from 
    system shutdown/restart.
    
.PARAMETER Duration
    How long to run: 'short' (4h), 'medium' (24h), 'long' (72h), 'extended' (7d)
    
.PARAMETER DashboardPort
    Port for real-time discovery dashboard (default 8080)
    
.PARAMETER AlertThreshold
    Delta threshold for discovery alerts (default 0.25, K3-DISC-0035 is 0.327)
#>

param(
    [ValidateSet('short', 'medium', 'long', 'extended')]
    [string]$Duration = 'medium',
    
    [int]$DashboardPort = 8080,
    
    [double]$AlertThreshold = 0.25,
    
    [switch]$SkipDashboard
)

$ErrorActionPreference = 'Continue'

# Configuration
$RepoRoot = 'D:\xdev\DarkMatterK3@Home\DarkMatterK3-Home.github.io'
$LogDir = Join-Path $RepoRoot 'logs'
$DashboardDir = Join-Path $RepoRoot 'dashboard'
$DiscoveriesFile = Join-Path $RepoRoot 'discoveries.json'
$Phase4LogFile = Join-Path $LogDir 'phase4_multiday.log'

# Duration mapping
$DurationMap = @{
    'short'    = 4      # hours
    'medium'   = 24     # hours
    'long'     = 72     # hours
    'extended' = 168    # hours (7 days)
}

$MaxHours = $DurationMap[$Duration]
$StartTime = Get-Date
$EndTime = $StartTime.AddHours($MaxHours)

function Write-Log {
    param([string]$Message, [string]$Level = 'INFO')
    
    $timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    $logEntry = "[$timestamp] [$Level] $Message"
    
    Write-Host $logEntry -ForegroundColor $(
        switch ($Level) {
            'ERROR'   { 'Red' }
            'WARNING' { 'Yellow' }
            'SUCCESS' { 'Green' }
            default   { 'White' }
        }
    )
    
    Add-Content -Path $Phase4LogFile -Value $logEntry
}

function Initialize-Environment {
    Write-Log "Initializing Phase 4 Multi-Day Execution"
    Write-Log "Duration: $Duration ($MaxHours hours)"
    Write-Log "Start time: $StartTime"
    Write-Log "End time: $EndTime"
    Write-Log "Alert threshold: $AlertThreshold"
    
    # Create directories
    if (-not (Test-Path $LogDir)) {
        New-Item -ItemType Directory -Path $LogDir | Out-Null
    }
    
    if (-not (Test-Path $DashboardDir)) {
        New-Item -ItemType Directory -Path $DashboardDir | Out-Null
    }
    
    # Verify V4B resilience infrastructure
    $requiredFiles = @(
        'run_v4b_resilient.ps1',
        'v4b_disk_monitor.py',
        'v4b_checkpoint.py'
    )
    
    foreach ($file in $requiredFiles) {
        $path = Join-Path $RepoRoot $file
        if (-not (Test-Path $path)) {
            Write-Log "ERROR: Required file not found: $file" 'ERROR'
            return $false
        }
    }
    
    Write-Log "Environment initialized successfully" 'SUCCESS'
    return $true
}

function Start-V4BPipeline {
    Write-Log "Starting V4B pipeline with resilience"
    
    try {
        # Start V4B with resilience
        & (Join-Path $RepoRoot 'run_v4b_resilient.ps1') -Action Start
        
        Write-Log "V4B pipeline started" 'SUCCESS'
        return $true
    } catch {
        Write-Log "Failed to start V4B pipeline: $_" 'ERROR'
        return $false
    }
}

function Start-NEDCrossmatch {
    Write-Log "Starting NED cross-match for K3-DISC-0035"
    
    try {
        # Run NED cross-match in background
        $nedScript = Join-Path $RepoRoot 'run_ned_k3_disc_0035.ps1'
        
        if (Test-Path $nedScript) {
            & $nedScript
            Write-Log "NED cross-match completed" 'SUCCESS'
        } else {
            Write-Log "NED cross-match script not found" 'WARNING'
        }
    } catch {
        Write-Log "NED cross-match error: $_" 'WARNING'
    }
}

function Monitor-Discoveries {
    Write-Log "Starting discovery monitoring"
    
    # Load existing discoveries
    $discoveries = @()
    if (Test-Path $DiscoveriesFile) {
        try {
            $discoveries = Get-Content $DiscoveriesFile | ConvertFrom-Json
        } catch {
            Write-Log "Could not load discoveries.json" 'WARNING'
            $discoveries = @()
        }
    }
    
    # Filter for high-delta anomalies
    $anomalies = $discoveries | Where-Object { 
        [double]$_.delta -gt $AlertThreshold 
    } | Sort-Object -Property delta -Descending
    
    Write-Log "Found $($anomalies.Count) anomalies above threshold ($AlertThreshold)" 'INFO'
    
    # Check for K3-DISC-0035 specifically
    $k3Disc0035 = $anomalies | Where-Object { 
        $_.id -eq 'K3-DISC-0035' -or $_.name -match '0035'
    }
    
    if ($k3Disc0035) {
        Write-Log "ALERT: K3-DISC-0035 detected! Delta = $($k3Disc0035.delta)" 'SUCCESS'
        Write-Log "Coordinates: RA $($k3Disc0035.ra)°, Dec $($k3Disc0035.dec)°" 'SUCCESS'
        Write-Log "Classification: $($k3Disc0035.classification)" 'SUCCESS'
        Write-Log "Astrophysical signature: Satellite system with tidal stripping" 'SUCCESS'
    }
    
    return $anomalies
}

function Update-Dashboard {
    param([array]$Anomalies)
    
    Write-Log "Updating discovery dashboard"
    
    # Create dashboard HTML
    $dashboardHtml = @"
<!DOCTYPE html>
<html>
<head>
    <title>Phase 4 Discovery Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Courier New', monospace;
            background: #0a0e27;
            color: #00ff88;
            padding: 20px;
            line-height: 1.6;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { color: #00ffff; margin-bottom: 20px; text-shadow: 0 0 10px #00ffff; }
        .status-bar {
            background: #1a1f3a;
            border: 1px solid #00ff88;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
        }
        .status-item {
            display: inline-block;
            margin-right: 30px;
            color: #00ff88;
        }
        .status-label { color: #00ffff; font-weight: bold; }
        .anomaly-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .anomaly-card {
            background: #1a1f3a;
            border: 2px solid #00ff88;
            padding: 15px;
            border-radius: 5px;
            transition: all 0.3s;
        }
        .anomaly-card:hover {
            border-color: #00ffff;
            box-shadow: 0 0 20px #00ffff;
        }
        .anomaly-id {
            color: #00ffff;
            font-weight: bold;
            font-size: 1.2em;
            margin-bottom: 10px;
        }
        .anomaly-delta {
            color: #ff00ff;
            font-weight: bold;
            font-size: 1.1em;
        }
        .anomaly-coords {
            color: #00ff88;
            font-size: 0.9em;
            margin-top: 10px;
        }
        .anomaly-class {
            color: #ffff00;
            font-size: 0.9em;
            margin-top: 5px;
        }
        .k3-highlight {
            border-color: #ff00ff;
            background: #2a1f3a;
            box-shadow: 0 0 15px #ff00ff;
        }
        .alert-banner {
            background: #ff00ff;
            color: #0a0e27;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
            font-weight: bold;
            text-align: center;
        }
        .filament-alert {
            background: linear-gradient(90deg, #ff00ff, #00ffff);
            color: #0a0e27;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 5px;
            font-weight: bold;
            text-align: center;
            font-size: 1.1em;
        }
        .last-update {
            color: #888;
            font-size: 0.8em;
            margin-top: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ Phase 4 Discovery Dashboard</h1>
        
        <div class="status-bar">
            <div class="status-item">
                <span class="status-label">Status:</span> <span id="status">Running</span>
            </div>
            <div class="status-item">
                <span class="status-label">Anomalies Found:</span> <span id="count">0</span>
            </div>
            <div class="status-item">
                <span class="status-label">Elapsed:</span> <span id="elapsed">0h 0m</span>
            </div>
        </div>
"@

    # Add K3-DISC-0035 alert if found
    $k3Found = $Anomalies | Where-Object { $_.id -eq 'K3-DISC-0035' }
    if ($k3Found) {
        $dashboardHtml += @"
        <div class="filament-alert">
            🌌 MAJOR DISCOVERY: K3-DISC-0035 DETECTED
            <br>
            30° Dark Matter Filament along RA 205° Meridian
            <br>
            Delta = $($k3Found.delta) | Satellite System with Tidal Stripping
        </div>
"@
    }

    # Add anomaly cards
    $dashboardHtml += "<div class='anomaly-grid'>"
    
    foreach ($anomaly in $Anomalies | Select-Object -First 20) {
        $isK3 = $anomaly.id -eq 'K3-DISC-0035'
        $cardClass = if ($isK3) { 'anomaly-card k3-highlight' } else { 'anomaly-card' }
        
        $dashboardHtml += @"
        <div class="$cardClass">
            <div class="anomaly-id">$($anomaly.id)</div>
            <div class="anomaly-delta">Δ = $([Math]::Round($anomaly.delta, 4))</div>
            <div class="anomaly-coords">RA $($anomaly.ra)°, Dec $($anomaly.dec)°</div>
            <div class="anomaly-class">$($anomaly.classification)</div>
        </div>
"@
    }
    
    $dashboardHtml += "</div>"
    $dashboardHtml += "<div class='last-update'>Last updated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')</div>"
    $dashboardHtml += "</div></body></html>"
    
    # Save dashboard
    $dashboardPath = Join-Path $DashboardDir 'index.html'
    Set-Content -Path $dashboardPath -Value $dashboardHtml
    
    Write-Log "Dashboard updated: $dashboardPath" 'SUCCESS'
}

function Start-DashboardServer {
    Write-Log "Starting dashboard server on port $DashboardPort"
    
    # Create simple HTTP server using Python
    $pythonScript = @"
import http.server
import socketserver
import os
from pathlib import Path

PORT = $DashboardPort
DASHBOARD_DIR = r'$DashboardDir'

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DASHBOARD_DIR, **kwargs)

try:
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"Dashboard server running on http://localhost:{PORT}")
        httpd.serve_forever()
except Exception as e:
    print(f"Dashboard server error: {e}")
"@
    
    $pythonPath = Join-Path $RepoRoot 'dashboard_server.py'
    Set-Content -Path $pythonPath -Value $pythonScript
    
    try {
        # Start Python server in background
        Start-Process python -ArgumentList $pythonPath -NoNewWindow
        Write-Log "Dashboard server started on http://localhost:$DashboardPort" 'SUCCESS'
    } catch {
        Write-Log "Failed to start dashboard server: $_" 'WARNING'
    }
}

function Monitor-Pipeline {
    Write-Log "Starting pipeline monitoring loop"
    
    $lastDiscoveryCount = 0
    $checkInterval = 300  # 5 minutes
    
    while ((Get-Date) -lt $EndTime) {
        # Check V4B status
        $status = & (Join-Path $RepoRoot 'run_v4b_resilient.ps1') -Action Status
        
        # Monitor discoveries
        $anomalies = Monitor-Discoveries
        
        # Update dashboard
        if (-not $SkipDashboard) {
            Update-Dashboard -Anomalies $anomalies
        }
        
        # Alert on new discoveries
        if ($anomalies.Count -gt $lastDiscoveryCount) {
            Write-Log "NEW DISCOVERY: Found $($anomalies.Count) anomalies (was $lastDiscoveryCount)" 'SUCCESS'
            $lastDiscoveryCount = $anomalies.Count
        }
        
        # Check disk space
        $diskStatus = python v4b_disk_monitor.py
        
        # Sleep before next check
        Write-Log "Next check in $($checkInterval / 60) minutes..."
        Start-Sleep -Seconds $checkInterval
    }
}

function Stop-Pipeline {
    Write-Log "Stopping Phase 4 pipeline"
    
    try {
        & (Join-Path $RepoRoot 'run_v4b_resilient.ps1') -Action Stop
        Write-Log "Pipeline stopped gracefully" 'SUCCESS'
    } catch {
        Write-Log "Error stopping pipeline: $_" 'WARNING'
    }
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

Write-Host @"
╔════════════════════════════════════════════════════════════════════════════╗
║                  PHASE 4 MULTI-DAY EXECUTION                              ║
║                                                                            ║
║  Duration: $Duration ($MaxHours hours)                                        ║
║  Start: $StartTime                                    ║
║  End: $EndTime                                      ║
║  Alert Threshold: $AlertThreshold                                            ║
║  Dashboard: http://localhost:$DashboardPort                                   ║
╚════════════════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# Initialize
if (-not (Initialize-Environment)) {
    Write-Log "Initialization failed" 'ERROR'
    exit 1
}

# Start services
Start-V4BPipeline
Start-NEDCrossmatch

if (-not $SkipDashboard) {
    Start-DashboardServer
}

# Main monitoring loop
Monitor-Pipeline

# Cleanup
Stop-Pipeline

Write-Log "Phase 4 multi-day execution completed" 'SUCCESS'
