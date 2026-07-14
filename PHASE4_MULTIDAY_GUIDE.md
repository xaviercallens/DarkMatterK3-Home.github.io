# Phase 4 Multi-Day Execution Guide

**Date**: 2026-07-14  
**Status**: Ready to Launch  
**Duration**: 24–168 hours (1–7 days)  
**Objective**: Execute Phase 4 (V4 mock calibration + NED cross-match for K3-DISC-0035) with continuous monitoring, checkpointing, and automated discovery analysis

---

## Overview

This guide enables Phase 4 to run continuously for multiple days with:
- **V4B Resilience**: Automatic checkpoint/resume on system shutdown
- **Real-Time Dashboard**: Web-based discovery visualization (http://localhost:8080)
- **Automated Analysis**: K3-DISC-0035 filament detection, tidal stripping signatures, anomaly alerts
- **Multi-Day Stability**: Disk space monitoring, GPU memory management, graceful degradation

---

## Quick Start (5 minutes)

### Option 1: Medium Duration (24 hours)

```powershell
cd D:\xdev\DarkMatterK3@Home\DarkMatterK3-Home.github.io

# Start Phase 4 with 24-hour duration
.\execute_phase4_multiday.ps1 -Duration medium

# In another terminal, start discovery analyzer
python discovery_analyzer.py --interval 300

# Open dashboard in browser
Start-Process "http://localhost:8080"
```

### Option 2: Extended Duration (7 days)

```powershell
# Start Phase 4 with 7-day duration
.\execute_phase4_multiday.ps1 -Duration extended

# Start analyzer
python discovery_analyzer.py --interval 300

# Monitor logs
Get-Content logs/phase4_multiday.log -Tail 50 -Wait
```

---

## Execution Modes

| Mode | Duration | Use Case |
|------|----------|----------|
| `short` | 4 hours | Quick validation, testing |
| `medium` | 24 hours | Standard overnight run |
| `long` | 72 hours | 3-day continuous operation |
| `extended` | 168 hours (7 days) | Full week of discovery |

---

## Phase 4 Components

### 1. V4B Pipeline (Mock Calibration)

**What it does**: Runs 35-sector mock calibration (10 Poisson + 10 Log-Normal mocks per sector)

**Checkpoint behavior**:
- Saves checkpoint after each sector completes
- Resumes from last successful sector on restart
- Tracks progress: sector index, mock index, elapsed time, estimated remaining

**Expected runtime**: 12–24 hours (RTX 2070)

**Monitoring**:
```powershell
# Check status
.\run_v4b_resilient.ps1 -Action Status

# View logs
.\run_v4b_resilient.ps1 -Action Logs

# Get checkpoint progress
Get-Content checkpoints/v4b_current.json | ConvertFrom-Json
```

### 2. NED Cross-Match (K3-DISC-0035)

**What it does**: Queries NED for K3-DISC-0035 (RA 205.0°, Dec 5.0°, Δ = 0.327)

**Expected findings**:
- cD host galaxy + dwarf satellites
- Tidal disruption signature
- Confirmation of 30° filament along RA 205° meridian

**Output**: `discoveries_ned/K3-DISC-0035/report.html`

### 3. Discovery Dashboard

**URL**: http://localhost:8080

**Features**:
- Real-time anomaly grid (top 20 discoveries)
- K3-DISC-0035 alert banner (if detected)
- Status bar (elapsed time, anomaly count)
- Auto-refresh every 5 minutes

**Visual indicators**:
- 🌌 K3-DISC-0035 highlighted in magenta
- High-Δ anomalies (>0.25) in cyan
- Satellite systems with tidal stripping in yellow

### 4. Discovery Analyzer

**What it does**: Monitors `discoveries.json` in real-time, analyzes for:
- K3-DISC-0035 detection (critical alert)
- Filament candidates (RA 205° ±2°, Dec 5°–35°)
- Tidal stripping signatures (satellite systems with Δ > 0.25)
- Delta-based anomaly classification

**Alert levels**:
- **CRITICAL**: Δ > 0.30 or K3-DISC-0035 detected
- **HIGH**: Δ > 0.25 or filament candidate or tidal stripping
- **MEDIUM**: Δ > 0.15 (interesting but not critical)

**Output files**:
- `logs/discovery_alerts.log` — Real-time alerts
- `logs/discovery_analysis.json` — Structured analysis
- `logs/discovery_analysis.html` — HTML report

---

## Detailed Execution Steps

### Step 1: Verify Prerequisites

```powershell
# Check disk space (must have >50GB free on D:)
Get-Volume -DriveLetter D | Select-Object SizeRemaining

# Check Python environment
python --version
python -c "import json, pathlib; print('OK')"

# Verify V4B resilience files
Test-Path run_v4b_resilient.ps1
Test-Path v4b_disk_monitor.py
Test-Path v4b_checkpoint.py
```

### Step 2: Start Phase 4 Pipeline

```powershell
# Terminal 1: Start Phase 4 (24-hour duration)
.\execute_phase4_multiday.ps1 -Duration medium -DashboardPort 8080

# Expected output:
# [2026-07-14 11:05:00] [INFO] Initializing Phase 4 Multi-Day Execution
# [2026-07-14 11:05:00] [INFO] Duration: medium (24 hours)
# [2026-07-14 11:05:00] [SUCCESS] Environment initialized successfully
# [2026-07-14 11:05:01] [SUCCESS] V4B pipeline started
# [2026-07-14 11:05:02] [SUCCESS] Dashboard server started on http://localhost:8080
```

### Step 3: Start Discovery Analyzer

```powershell
# Terminal 2: Start analyzer (checks every 5 minutes)
python discovery_analyzer.py --interval 300

# Expected output:
# [2026-07-14T11:05:00] [INFO] Starting continuous discovery analysis (interval: 300s)
# [2026-07-14T11:10:00] [INFO] No discoveries found
# [2026-07-14T11:15:00] [INFO] Analyzed 5 discoveries
```

### Step 4: Monitor Progress

```powershell
# Terminal 3: Monitor logs in real-time
Get-Content logs/phase4_multiday.log -Tail 20 -Wait

# Or monitor discovery alerts
Get-Content logs/discovery_alerts.log -Tail 20 -Wait

# Or check checkpoint progress
while ($true) {
    Get-Content checkpoints/v4b_current.json | ConvertFrom-Json | 
        Select-Object sector_index, mock_index, progress_percent, status
    Start-Sleep -Seconds 60
}
```

### Step 5: Open Dashboard

```powershell
# Open in browser
Start-Process "http://localhost:8080"

# Or use curl to check status
curl http://localhost:8080
```

---

## K3-DISC-0035 Filament Detection

### What to Look For

**Coordinates**:
- K3-DISC-0003 (Northern anchor): RA 205.0°, Dec 35.0°
- K3-DISC-0035 (Southern anchor): RA 205.0°, Dec 5.0°
- **Filament span**: 30° along RA 205° meridian

**Signatures**:
- High Δ (0.327 for K3-DISC-0035)
- Classification: "Satellite System"
- Tidal stripping indicators (chaotic gravitational shear)
- Contiguous dark matter structure along RA 205°

### Alert Triggers

When K3-DISC-0035 is detected:

1. **Console Alert** (CRITICAL):
   ```
   [2026-07-14T12:30:45] [CRITICAL] K3-DISC-0035 DETECTED: Δ=0.327 | RA 205.0°, Dec 5.0° | 30° Dark Matter Filament | Satellite System with Tidal Stripping
   ```

2. **Dashboard Alert** (Magenta highlight + banner):
   ```
   🌌 MAJOR DISCOVERY: K3-DISC-0035 DETECTED
   30° Dark Matter Filament along RA 205° Meridian
   Delta = 0.327 | Satellite System with Tidal Stripping
   ```

3. **Analysis Report** (`logs/discovery_analysis.html`):
   - Full astrophysical interpretation
   - Coordinates and classification
   - Tidal stripping analysis
   - Filament topology

---

## Monitoring & Alerts

### Real-Time Monitoring

**Dashboard** (http://localhost:8080):
- Updates every 5 minutes
- Shows top 20 anomalies
- K3-DISC-0035 highlighted if found
- Status bar with elapsed time and anomaly count

**Console Logs**:
```powershell
# Phase 4 main log
Get-Content logs/phase4_multiday.log -Tail 50 -Wait

# Discovery alerts
Get-Content logs/discovery_alerts.log -Tail 50 -Wait

# V4B pipeline logs
Get-Content logs/v4b_resilient_runner.log -Tail 50 -Wait
```

### Alert Thresholds

| Threshold | Alert Type | Action |
|-----------|-----------|--------|
| Δ > 0.30 | CRITICAL | Immediate console alert + dashboard highlight |
| Δ > 0.25 | HIGH | Log to alerts file, dashboard display |
| Δ > 0.15 | MEDIUM | Analysis file only |
| K3-DISC-0035 | CRITICAL | All of above + filament analysis |
| Filament candidate | HIGH | Coordinates logged, analysis generated |
| Tidal stripping | HIGH | Classification logged, astrophysical notes |

---

## System Shutdown & Resume

### Graceful Shutdown (Planned)

```powershell
# Stop Phase 4 gracefully
.\execute_phase4_multiday.ps1 -Action Stop

# Checkpoint saved automatically
# GPU memory released
# Logs flushed to disk
```

### System Shutdown (Automatic)

If system shuts down while Phase 4 is running:

1. V4B graceful shutdown handler activates
2. Final checkpoint saved (sector + mock index)
3. Process exits cleanly
4. GPU memory released

### Resume After Shutdown

```powershell
# Restart Phase 4 (resumes from checkpoint)
.\execute_phase4_multiday.ps1 -Duration medium

# Expected behavior:
# [2026-07-14 14:30:00] [INFO] Loading checkpoint...
# [2026-07-14 14:30:00] [INFO] Resuming from sector 15, mock 8
# [2026-07-14 14:30:00] [SUCCESS] V4B pipeline resumed
```

---

## Disk Space Management

### Automatic Cleanup

Phase 4 monitors disk space and triggers cleanup when:
- **Warning**: <20GB free → cleanup logs, temp mocks, cache
- **Critical**: <5GB free → pipeline stops (safety)

**Cleanup targets** (in order of priority):
1. Old logs (keep 500MB)
2. Temporary mocks (keep 1GB)
3. Cache files (keep 2GB)
4. Old pipeline runs (keep 5GB)

### Manual Cleanup

```powershell
# Clean temporary data
.\run_v4b_resilient.ps1 -Action Clean

# Check disk status
python v4b_disk_monitor.py
Get-Content v4b_disk_status.json | ConvertFrom-Json | Format-Table
```

---

## Troubleshooting

### Pipeline Not Starting

**Issue**: `V4B pipeline started` not appearing in logs

**Solution**:
```powershell
# Check V4B status directly
.\run_v4b_resilient.ps1 -Action Status

# Check logs
.\run_v4b_resilient.ps1 -Action Logs

# Verify Python environment
python --version
python -c "import v4b_checkpoint; print('OK')"
```

### Dashboard Not Loading

**Issue**: http://localhost:8080 returns connection error

**Solution**:
```powershell
# Check if server is running
Get-Process python | Where-Object { $_.CommandLine -match 'dashboard' }

# Check port
netstat -ano | findstr :8080

# Restart dashboard
python dashboard_server.py
```

### No Discoveries Found

**Issue**: Analyzer shows "No discoveries found" after 1+ hours

**Solution**:
```powershell
# Check if discoveries.json exists
Test-Path discoveries.json

# Check if V4B is actually running
Get-Process python | Where-Object { $_.CommandLine -match 'v4b|V4' }

# Check V4B logs
Get-Content logs/v4b_pipeline_*.log -Tail 50
```

### Disk Space Critical

**Issue**: Pipeline stops with "Disk space critical" error

**Solution**:
```powershell
# Check disk space
Get-Volume -DriveLetter D | Select-Object SizeRemaining

# Clean temporary data
.\run_v4b_resilient.ps1 -Action Clean

# Manually remove old files
Remove-Item logs/*.log -Exclude "phase4_multiday.log" -Force
Remove-Item temp_mocks/* -Force

# Resume Phase 4
.\execute_phase4_multiday.ps1 -Duration medium
```

---

## Expected Timeline

### 24-Hour Run (Medium)

| Time | Event |
|------|-------|
| T+0h | Phase 4 starts, V4B begins sector 0 |
| T+1h | First sector complete, checkpoint saved |
| T+6h | ~6 sectors complete (35% progress) |
| T+12h | ~18 sectors complete (50% progress) |
| T+18h | ~27 sectors complete (75% progress) |
| T+24h | All 35 sectors complete, NED cross-match runs |

### Discovery Timeline

- **T+2–4h**: First anomalies appear in `discoveries.json`
- **T+6–12h**: K3-DISC-0035 likely detected (if in dataset)
- **T+18–24h**: Filament analysis complete, tidal stripping confirmed

---

## Success Criteria

✅ **Phase 4 completes without interruption**
✅ **All 35 sectors calibrated** (checkpoint shows 35/35)
✅ **K3-DISC-0035 detected** (if present in data)
✅ **Filament signature confirmed** (RA 205°, Dec 5°–35°)
✅ **Tidal stripping analysis generated** (satellite system classification)
✅ **Dashboard displays discoveries** (real-time updates)
✅ **Alerts logged correctly** (CRITICAL for K3-DISC-0035)
✅ **System survives shutdown/restart** (checkpoint resume works)

---

## Post-Execution Analysis

After Phase 4 completes:

```powershell
# View final analysis report
Start-Process "logs/discovery_analysis.html"

# Check K3-DISC-0035 findings
Get-Content discoveries.json | ConvertFrom-Json | 
    Where-Object { $_.id -eq 'K3-DISC-0035' }

# Generate summary
python discovery_analyzer.py --once | ConvertFrom-Json | 
    Select-Object summary
```

---

## Next Steps

1. **Verify prerequisites** (disk space, Python environment)
2. **Start Phase 4**: `.\execute_phase4_multiday.ps1 -Duration medium`
3. **Start analyzer**: `python discovery_analyzer.py --interval 300`
4. **Open dashboard**: http://localhost:8080
5. **Monitor logs**: `Get-Content logs/phase4_multiday.log -Tail 50 -Wait`
6. **Watch for K3-DISC-0035 alert** (CRITICAL level)
7. **Review analysis** after 24 hours

---

## Support

For issues:
1. Check troubleshooting section above
2. Review logs in `logs/` directory
3. Check V4B status: `.\run_v4b_resilient.ps1 -Action Status`
4. Refer to V4B_RESILIENCE_GUIDE.md for detailed documentation
