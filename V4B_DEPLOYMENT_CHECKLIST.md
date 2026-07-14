# V4B Deployment Checklist

**Date**: 2026-07-14  
**Status**: Ready for Deployment  
**Purpose**: Step-by-step checklist for deploying V4B resilience infrastructure

---

## Pre-Deployment Verification

- [ ] All V4B resilience files created and in place
- [ ] Python dependencies installed (astropy, numpy, scipy)
- [ ] PowerShell execution policy set to allow scripts: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- [ ] Administrator access available (for Windows service installation)
- [ ] Disk space available: >50GB free on D: drive
- [ ] GPU drivers updated (NVIDIA recommended)
- [ ] `.venv` Python environment configured or system Python available

---

## Files Verification

### Core Resilience Components

- [ ] `v4b_disk_monitor.py` — Disk space monitoring (250+ lines)
- [ ] `v4b_checkpoint.py` — Checkpoint/resume system (350+ lines)
- [ ] `v4b_service_wrapper.ps1` — Windows service wrapper (400+ lines)
- [ ] `v4b_graceful_shutdown.ps1` — Graceful shutdown handler (300+ lines)
- [ ] `run_v4b_resilient.ps1` — Resilient pipeline runner (350+ lines)

### Documentation

- [ ] `V4B_RESILIENCE_GUIDE.md` — Comprehensive guide (600+ lines)
- [ ] `V4B_RESILIENCE_IMPLEMENTATION.md` — Implementation summary
- [ ] `V4B_DEPLOYMENT_CHECKLIST.md` — This file
- [ ] `RELEASE_NOTES.md` — Updated with V4B details
- [ ] `TODO.md` — Updated with V4B tasks

### Phase 4 Files

- [ ] `PHASE4_EXECUTION_PLAN.md` — Phase 4 timeline
- [ ] `PHASE4_SUMMARY.md` — Phase 4 overview
- [ ] `WEAK_LENSING_DATA_REQUEST.md` — Weak-lensing request
- [ ] `execute_phase4_full.ps1` — Phase 4 orchestration
- [ ] `run_ned_k3_disc_0035.ps1` — NED cross-match runner

---

## Step 1: Verify Python Environment

```powershell
# Check Python version
python --version

# Check required packages
python -c "import astropy; import numpy; import scipy; print('All packages OK')"

# Test v4b_disk_monitor.py
python v4b_disk_monitor.py

# Test v4b_checkpoint.py
python v4b_checkpoint.py
```

**Expected Output**:
- Python 3.8+
- All packages imported successfully
- Disk monitor shows drive usage
- Checkpoint manager shows status

---

## Step 2: Test Disk Space Monitoring

```powershell
# Run disk monitor
python v4b_disk_monitor.py

# Check disk status file
Get-Content v4b_disk_status.json | ConvertFrom-Json | Format-Table
```

**Expected Output**:
- `v4b_disk_status.json` created
- Drive usage displayed
- Free space >5GB (critical threshold)

---

## Step 3: Test Checkpoint System

```powershell
# Verify checkpoint integrity
python -c "from v4b_checkpoint import CheckpointManager; m = CheckpointManager(); print('Checkpoint OK' if m.verify_checkpoint_integrity() else 'Checkpoint failed')"

# Check checkpoint directory
Get-ChildItem checkpoints/ -ErrorAction SilentlyContinue
```

**Expected Output**:
- Checkpoint integrity verified
- `checkpoints/` directory exists (may be empty initially)

---

## Step 4: Test Graceful Shutdown Handler

```powershell
# Test graceful shutdown script (dry run)
.\v4b_graceful_shutdown.ps1 -ProcessId 0

# Check graceful shutdown logs
Get-Content logs/v4b_graceful_shutdown.log -Tail 10 -ErrorAction SilentlyContinue
```

**Expected Output**:
- Script runs without errors
- Log file created in `logs/`

---

## Step 5: Test Resilient Runner

```powershell
# Check resilient runner status
.\run_v4b_resilient.ps1 -Action Status

# Check resilient runner logs
.\run_v4b_resilient.ps1 -Action Logs
```

**Expected Output**:
- Status file created: `v4b_status.json`
- Log file created: `logs/v4b_resilient_runner.log`

---

## Step 6: Install Windows Service (Optional but Recommended)

```powershell
# Run as Administrator
# Check if running as admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "ERROR: Must run as Administrator" -ForegroundColor Red
    exit 1
}

# Install service
.\v4b_service_wrapper.ps1 -Action Install

# Verify installation
Get-Service -Name DarkMatterK3-V4B -ErrorAction SilentlyContinue
```

**Expected Output**:
- Service installed successfully
- Service name: `DarkMatterK3-V4B`
- Start type: Automatic

---

## Step 7: Start V4B Pipeline

### Option A: Windows Service (Recommended for Multi-Day)

```powershell
# Start service
.\v4b_service_wrapper.ps1 -Action Start

# Verify service is running
.\v4b_service_wrapper.ps1 -Action Status

# Check service logs
.\v4b_service_wrapper.ps1 -Action Logs
```

### Option B: Resilient Runner (Direct Control)

```powershell
# Start pipeline
.\run_v4b_resilient.ps1 -Action Start

# Monitor progress
.\run_v4b_resilient.ps1 -Action Status
```

**Expected Output**:
- Service/runner starts successfully
- Status shows "running"
- Logs show pipeline initialization

---

## Step 8: Monitor V4B Progress

### Daily Monitoring

```powershell
# Check overall status
.\run_v4b_resilient.ps1 -Action Status

# View recent logs
.\run_v4b_resilient.ps1 -Action Logs

# Check disk space
Get-Content v4b_disk_status.json | ConvertFrom-Json

# Check checkpoint progress
Get-Content checkpoints/v4b_current.json | ConvertFrom-Json | Select-Object sector_index, mock_index, progress_percent, status
```

### Real-Time Monitoring

```powershell
# Monitor V4 pipeline output in real-time
Get-Content logs/v4b_pipeline_*.log -Tail 20 -Wait

# Monitor disk space changes
while ($true) {
    Clear-Host
    Get-Content v4b_disk_status.json | ConvertFrom-Json | Format-Table
    Start-Sleep -Seconds 60
}
```

---

## Step 9: Handle System Shutdown/Restart

### Graceful Shutdown (Planned)

```powershell
# Stop service gracefully
.\v4b_service_wrapper.ps1 -Action Stop

# Or stop resilient runner
.\run_v4b_resilient.ps1 -Action Stop

# Verify process is gone
Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match 'v4b|V4' }
```

### System Shutdown (Automatic)

The Windows service will:
1. Receive shutdown notification
2. Execute graceful shutdown handler
3. Save final checkpoint
4. Exit cleanly

### Resume After Shutdown

```powershell
# Resume from checkpoint
.\run_v4b_resilient.ps1 -Action Resume

# Or restart service
.\v4b_service_wrapper.ps1 -Action Start
```

---

## Step 10: Verify Multi-Day Operation

### Checkpoint Recovery Test

```powershell
# Start pipeline
.\run_v4b_resilient.ps1 -Action Start

# Wait for first checkpoint (after first sector completes)
Start-Sleep -Seconds 300

# Check checkpoint
Get-Content checkpoints/v4b_current.json | ConvertFrom-Json

# Stop pipeline
.\run_v4b_resilient.ps1 -Action Stop

# Resume from checkpoint
.\run_v4b_resilient.ps1 -Action Resume

# Verify progress continued from checkpoint
Get-Content checkpoints/v4b_current.json | ConvertFrom-Json
```

**Expected Result**:
- Pipeline resumes from last successful checkpoint
- No work is lost
- Progress continues seamlessly

---

## Troubleshooting During Deployment

### Issue: Python not found

**Solution**:
```powershell
# Check Python path
python --version
Get-Command python

# If not found, install Python or use .venv
.\venv\Scripts\python.exe --version
```

### Issue: Disk monitor fails

**Solution**:
```powershell
# Check disk space manually
Get-Volume

# Check disk monitor logs
Get-Content logs/v4b_disk_monitor.log -Tail 20
```

### Issue: Service won't install

**Solution**:
```powershell
# Run as Administrator
Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File v4b_service_wrapper.ps1 -Action Install" -Verb RunAs

# Or check if service already exists
Get-Service -Name DarkMatterK3-V4B -ErrorAction SilentlyContinue
```

### Issue: Checkpoint not resuming

**Solution**:
```powershell
# Check checkpoint file
Get-Content checkpoints/v4b_current.json

# Verify checkpoint integrity
python -c "from v4b_checkpoint import CheckpointManager; m = CheckpointManager(); m.verify_checkpoint_integrity()"

# Clear corrupted checkpoint if needed
Remove-Item checkpoints/v4b_current.json -Force
```

---

## Post-Deployment Verification

- [ ] V4B pipeline started successfully
- [ ] Checkpoint system working (checkpoint file created)
- [ ] Disk space monitoring active (status file updated)
- [ ] Logs being written to `logs/v4b_*.log`
- [ ] Service running (if installed)
- [ ] Status file updated: `v4b_status.json`

---

## Expected Timeline

| Phase | Duration | Checkpoint |
|-------|----------|-----------|
| **Deployment** | 30 minutes | All checks pass |
| **Initial Start** | 5 minutes | Pipeline initializes |
| **First Sector** | 20–40 minutes | First checkpoint saved |
| **Calibration** | 12–24 hours | 35/35 sectors complete |

---

## Success Criteria

✓ **Disk Space Monitoring**: Real-time monitoring active  
✓ **Checkpoint System**: Checkpoints saved after each sector  
✓ **Graceful Shutdown**: Process exits cleanly on stop signal  
✓ **Resume Capability**: Pipeline resumes from checkpoint with zero work loss  
✓ **Windows Service**: Service starts automatically on reboot  
✓ **Logging**: All operations logged to `logs/v4b_*.log`  
✓ **Status Tracking**: Status files updated regularly  

---

## Quick Reference Commands

```powershell
# Start V4B (Windows Service)
.\v4b_service_wrapper.ps1 -Action Start

# Check status
.\v4b_service_wrapper.ps1 -Action Status

# View logs
.\v4b_service_wrapper.ps1 -Action Logs

# Stop gracefully
.\v4b_service_wrapper.ps1 -Action Stop

# Resume from checkpoint
.\run_v4b_resilient.ps1 -Action Resume

# Monitor progress
.\run_v4b_resilient.ps1 -Action Status

# Clean temporary data
.\run_v4b_resilient.ps1 -Action Clean
```

---

## Support Resources

- **V4B_RESILIENCE_GUIDE.md**: Comprehensive guide with examples
- **V4B_RESILIENCE_IMPLEMENTATION.md**: Implementation details
- **RELEASE_NOTES.md**: Release notes with V4B updates
- **logs/v4b_*.log**: Detailed logs for debugging
- **GitHub Issues**: Report issues at https://github.com/xaviercallens/DarkMatterK3-Home.github.io/issues

---

## Deployment Sign-Off

- [ ] All pre-deployment checks passed
- [ ] All files verified and in place
- [ ] Python environment tested
- [ ] Disk space monitoring verified
- [ ] Checkpoint system verified
- [ ] Windows service installed (if applicable)
- [ ] V4B pipeline started successfully
- [ ] First checkpoint saved
- [ ] Multi-day operation tested and verified
- [ ] Documentation reviewed
- [ ] Ready for production deployment

---

## Next Steps

1. **Complete all checklist items above**
2. **Start V4B pipeline**: `.\v4b_service_wrapper.ps1 -Action Start`
3. **Monitor progress daily**: `.\v4b_service_wrapper.ps1 -Action Status`
4. **Check logs weekly**: `.\v4b_service_wrapper.ps1 -Action Logs`
5. **Verify checkpoint advancement**: `Get-Content checkpoints/v4b_current.json | ConvertFrom-Json`
6. **Plan for system maintenance**: Schedule downtime if needed
7. **Backup checkpoints**: Copy `checkpoints/` directory regularly

---

## Deployment Complete

Once all checklist items are verified, V4B is ready for production multi-day operation.

**Estimated completion**: 12–24 hours for 35-sector mock calibration  
**Expected outcome**: 35/35 sectors calibrated with checkpoint recovery capability
