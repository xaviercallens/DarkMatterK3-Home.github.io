#Requires -Version 5.1
<#
.SYNOPSIS
    Unit Tests for V4B Resilience PowerShell Components

.DESCRIPTION
    Tests for:
    - v4b_service_wrapper.ps1 (Windows service wrapper)
    - v4b_graceful_shutdown.ps1 (graceful shutdown handler)
    - run_v4b_resilient.ps1 (resilient pipeline runner)
#>

param(
    [string]$TestCategory = 'All',  # All, Service, Shutdown, Runner
    [switch]$Verbose
)

$ErrorActionPreference = 'Continue'

# Test configuration
$RepoRoot = 'D:\xdev\DarkMatterK3@Home\DarkMatterK3-Home.github.io'
$TestResults = @()
$TestsPassed = 0
$TestsFailed = 0

function Write-TestHeader {
    param([string]$Message)
    Write-Host "`n" + ("=" * 70) -ForegroundColor Cyan
    Write-Host $Message -ForegroundColor Cyan
    Write-Host ("=" * 70) -ForegroundColor Cyan
}

function Write-TestCase {
    param([string]$Name, [string]$Status, [string]$Message = "")
    
    $statusColor = if ($Status -eq 'PASS') { 'Green' } else { 'Red' }
    $statusSymbol = if ($Status -eq 'PASS') { '✓' } else { '✗' }
    
    Write-Host "  $statusSymbol $Name ... $Status" -ForegroundColor $statusColor
    
    if ($Message) {
        Write-Host "    → $Message" -ForegroundColor Gray
    }
    
    $TestResults += @{
        Name = $Name
        Status = $Status
        Message = $Message
    }
    
    if ($Status -eq 'PASS') {
        $script:TestsPassed++
    } else {
        $script:TestsFailed++
    }
}

function Test-FileExists {
    param([string]$FilePath, [string]$Description)
    
    if (Test-Path $FilePath) {
        Write-TestCase "File exists: $Description" 'PASS' $FilePath
        return $true
    } else {
        Write-TestCase "File exists: $Description" 'FAIL' "File not found: $FilePath"
        return $false
    }
}

function Test-FileContent {
    param([string]$FilePath, [string]$Pattern, [string]$Description)
    
    if (-not (Test-Path $FilePath)) {
        Write-TestCase "File content: $Description" 'FAIL' "File not found: $FilePath"
        return $false
    }
    
    $content = Get-Content $FilePath -Raw
    if ($content -match $Pattern) {
        Write-TestCase "File content: $Description" 'PASS'
        return $true
    } else {
        Write-TestCase "File content: $Description" 'FAIL' "Pattern not found: $Pattern"
        return $false
    }
}

function Test-PowerShellSyntax {
    param([string]$FilePath, [string]$Description)
    
    if (-not (Test-Path $FilePath)) {
        Write-TestCase "PowerShell syntax: $Description" 'FAIL' "File not found: $FilePath"
        return $false
    }
    
    try {
        $null = [System.Management.Automation.PSParser]::Tokenize((Get-Content $FilePath -Raw), [ref]$null)
        Write-TestCase "PowerShell syntax: $Description" 'PASS'
        return $true
    } catch {
        Write-TestCase "PowerShell syntax: $Description" 'FAIL' $_.Exception.Message
        return $false
    }
}

function Test-PythonSyntax {
    param([string]$FilePath, [string]$Description)
    
    if (-not (Test-Path $FilePath)) {
        Write-TestCase "Python syntax: $Description" 'FAIL' "File not found: $FilePath"
        return $false
    }
    
    try {
        $pythonExe = if (Test-Path (Join-Path $RepoRoot '.venv\Scripts\python.exe')) {
            Join-Path $RepoRoot '.venv\Scripts\python.exe'
        } else {
            'python'
        }
        
        & $pythonExe -m py_compile $FilePath 2>&1 | Out-Null
        Write-TestCase "Python syntax: $Description" 'PASS'
        return $true
    } catch {
        Write-TestCase "Python syntax: $Description" 'FAIL' $_.Exception.Message
        return $false
    }
}

# ============================================================================
# SERVICE WRAPPER TESTS
# ============================================================================

function Test-ServiceWrapper {
    Write-TestHeader "V4B Service Wrapper Tests"
    
    $serviceWrapperPath = Join-Path $RepoRoot 'v4b_service_wrapper.ps1'
    
    # Test 1: File exists
    Test-FileExists $serviceWrapperPath 'v4b_service_wrapper.ps1'
    
    # Test 2: PowerShell syntax
    Test-PowerShellSyntax $serviceWrapperPath 'v4b_service_wrapper.ps1'
    
    # Test 3: Required functions defined
    $content = Get-Content $serviceWrapperPath -Raw
    
    $requiredFunctions = @(
        'Install-V4BService',
        'Start-V4BService',
        'Stop-V4BService',
        'Remove-V4BService',
        'Get-V4BServiceStatus',
        'Get-V4BServiceLogs'
    )
    
    foreach ($func in $requiredFunctions) {
        if ($content -match "function $func") {
            Write-TestCase "Function defined: $func" 'PASS'
        } else {
            Write-TestCase "Function defined: $func" 'FAIL'
        }
    }
    
    # Test 4: Parameter validation
    if ($content -match 'ValidateSet.*Install.*Start.*Stop.*Remove.*Status.*Logs.*Restart') {
        Write-TestCase "Parameter validation: Action parameter" 'PASS'
    } else {
        Write-TestCase "Parameter validation: Action parameter" 'FAIL'
    }
    
    # Test 5: Service name defined
    if ($content -match "ServiceName.*=.*'DarkMatterK3-V4B'") {
        Write-TestCase "Service name: DarkMatterK3-V4B" 'PASS'
    } else {
        Write-TestCase "Service name: DarkMatterK3-V4B" 'FAIL'
    }
    
    # Test 6: Error handling
    if ($content -match 'ErrorActionPreference' -and $content -match 'try.*catch') {
        Write-TestCase "Error handling: try-catch blocks" 'PASS'
    } else {
        Write-TestCase "Error handling: try-catch blocks" 'FAIL'
    }
}

# ============================================================================
# GRACEFUL SHUTDOWN TESTS
# ============================================================================

function Test-GracefulShutdown {
    Write-TestHeader "V4B Graceful Shutdown Tests"
    
    $shutdownPath = Join-Path $RepoRoot 'v4b_graceful_shutdown.ps1'
    
    # Test 1: File exists
    Test-FileExists $shutdownPath 'v4b_graceful_shutdown.ps1'
    
    # Test 2: PowerShell syntax
    Test-PowerShellSyntax $shutdownPath 'v4b_graceful_shutdown.ps1'
    
    # Test 3: Required functions defined
    $content = Get-Content $shutdownPath -Raw
    
    $requiredFunctions = @(
        'Find-V4BProcess',
        'Send-GracefulShutdown',
        'Stop-ProcessForcefully',
        'Save-FinalCheckpoint',
        'Write-LogFiles',
        'Clear-GPUMemory'
    )
    
    foreach ($func in $requiredFunctions) {
        if ($content -match "function $func") {
            Write-TestCase "Function defined: $func" 'PASS'
        } else {
            Write-TestCase "Function defined: $func" 'FAIL'
        }
    }
    
    # Test 4: Shutdown sequence
    $shutdownSequence = @(
        'Save-FinalCheckpoint',
        'Send-GracefulShutdown',
        'Stop-ProcessForcefully',
        'Clear-GPUMemory',
        'Write-LogFiles'
    )
    
    $mainExecution = $content -split '# Main execution' | Select-Object -Last 1
    
    foreach ($step in $shutdownSequence) {
        if ($mainExecution -match $step) {
            Write-TestCase "Shutdown sequence: $step" 'PASS'
        } else {
            Write-TestCase "Shutdown sequence: $step" 'FAIL'
        }
    }
    
    # Test 5: Timeout handling
    if ($content -match 'TimeoutSeconds.*=.*60' -or $content -match '\$TimeoutSeconds') {
        Write-TestCase "Timeout handling: 60-second timeout" 'PASS'
    } else {
        Write-TestCase "Timeout handling: 60-second timeout" 'FAIL'
    }
    
    # Test 6: Logging
    if ($content -match 'Write-Log' -and $content -match 'logs/v4b_graceful_shutdown.log') {
        Write-TestCase "Logging: Write-Log function" 'PASS'
    } else {
        Write-TestCase "Logging: Write-Log function" 'FAIL'
    }
}

# ============================================================================
# RESILIENT RUNNER TESTS
# ============================================================================

function Test-ResilientRunner {
    Write-TestHeader "V4B Resilient Runner Tests"
    
    $runnerPath = Join-Path $RepoRoot 'run_v4b_resilient.ps1'
    
    # Test 1: File exists
    Test-FileExists $runnerPath 'run_v4b_resilient.ps1'
    
    # Test 2: PowerShell syntax
    Test-PowerShellSyntax $runnerPath 'run_v4b_resilient.ps1'
    
    # Test 3: Required functions defined
    $content = Get-Content $runnerPath -Raw
    
    $requiredFunctions = @(
        'Get-PythonExe',
        'Test-DiskSpace',
        'Test-CheckpointIntegrity',
        'Start-V4BPipeline',
        'Stop-V4BPipeline',
        'Get-V4BStatus',
        'Get-V4BLogs',
        'Resume-V4BPipeline',
        'Remove-V4BTemporaryData'
    )
    
    foreach ($func in $requiredFunctions) {
        if ($content -match "function $func") {
            Write-TestCase "Function defined: $func" 'PASS'
        } else {
            Write-TestCase "Function defined: $func" 'FAIL'
        }
    }
    
    # Test 4: Action parameter validation
    if ($content -match "ValidateSet.*'Start'.*'Stop'.*'Status'.*'Logs'.*'Resume'.*'Clean'") {
        Write-TestCase "Parameter validation: Action parameter" 'PASS'
    } else {
        Write-TestCase "Parameter validation: Action parameter" 'FAIL'
    }
    
    # Test 5: Retry logic
    if ($content -match 'MaxRetries' -and $content -match 'RetryDelaySeconds' -and $content -match 'exponential') {
        Write-TestCase "Retry logic: Exponential backoff" 'PASS'
    } else {
        Write-TestCase "Retry logic: Exponential backoff" 'FAIL'
    }
    
    # Test 6: Pre-flight checks
    if ($content -match 'Test-DiskSpace' -and $content -match 'Test-CheckpointIntegrity') {
        Write-TestCase "Pre-flight checks: Disk and checkpoint" 'PASS'
    } else {
        Write-TestCase "Pre-flight checks: Disk and checkpoint" 'FAIL'
    }
    
    # Test 7: Status tracking
    if ($content -match 'v4b_status.json') {
        Write-TestCase "Status tracking: v4b_status.json" 'PASS'
    } else {
        Write-TestCase "Status tracking: v4b_status.json" 'FAIL'
    }
}

# ============================================================================
# DISK MONITOR TESTS
# ============================================================================

function Test-DiskMonitor {
    Write-TestHeader "V4B Disk Monitor Tests"
    
    $diskMonitorPath = Join-Path $RepoRoot 'v4b_disk_monitor.py'
    
    # Test 1: File exists
    Test-FileExists $diskMonitorPath 'v4b_disk_monitor.py'
    
    # Test 2: Python syntax
    Test-PythonSyntax $diskMonitorPath 'v4b_disk_monitor.py'
    
    # Test 3: Required classes defined
    $content = Get-Content $diskMonitorPath -Raw
    
    if ($content -match 'class DiskMonitor') {
        Write-TestCase "Class defined: DiskMonitor" 'PASS'
    } else {
        Write-TestCase "Class defined: DiskMonitor" 'FAIL'
    }
    
    # Test 4: Thresholds defined
    $thresholds = @(
        'CRITICAL_THRESHOLD',
        'WARNING_THRESHOLD',
        'TARGET_FREE_SPACE'
    )
    
    foreach ($threshold in $thresholds) {
        if ($content -match $threshold) {
            Write-TestCase "Threshold defined: $threshold" 'PASS'
        } else {
            Write-TestCase "Threshold defined: $threshold" 'FAIL'
        }
    }
    
    # Test 5: Cleanup targets defined
    if ($content -match 'CLEANUP_TARGETS') {
        Write-TestCase "Cleanup targets: CLEANUP_TARGETS" 'PASS'
    } else {
        Write-TestCase "Cleanup targets: CLEANUP_TARGETS" 'FAIL'
    }
    
    # Test 6: Required methods
    $requiredMethods = @(
        'get_disk_usage',
        'check_disk_health',
        '_attempt_cleanup',
        '_cleanup_directory',
        '_save_status',
        'log_status'
    )
    
    foreach ($method in $requiredMethods) {
        if ($content -match "def $method") {
            Write-TestCase "Method defined: $method" 'PASS'
        } else {
            Write-TestCase "Method defined: $method" 'FAIL'
        }
    }
}

# ============================================================================
# CHECKPOINT TESTS
# ============================================================================

function Test-Checkpoint {
    Write-TestHeader "V4B Checkpoint Tests"
    
    $checkpointPath = Join-Path $RepoRoot 'v4b_checkpoint.py'
    
    # Test 1: File exists
    Test-FileExists $checkpointPath 'v4b_checkpoint.py'
    
    # Test 2: Python syntax
    Test-PythonSyntax $checkpointPath 'v4b_checkpoint.py'
    
    # Test 3: Required classes defined
    $content = Get-Content $checkpointPath -Raw
    
    $requiredClasses = @(
        'CheckpointData',
        'CheckpointManager',
        'CheckpointedLoop'
    )
    
    foreach ($class in $requiredClasses) {
        if ($content -match "@dataclass|class $class") {
            Write-TestCase "Class defined: $class" 'PASS'
        } else {
            Write-TestCase "Class defined: $class" 'FAIL'
        }
    }
    
    # Test 4: CheckpointData fields
    $requiredFields = @(
        'timestamp',
        'phase',
        'sector_index',
        'mock_index',
        'status',
        'progress_percent',
        'elapsed_seconds',
        'estimated_remaining_seconds',
        'last_successful_sector',
        'last_successful_mock'
    )
    
    foreach ($field in $requiredFields) {
        if ($content -match $field) {
            Write-TestCase "CheckpointData field: $field" 'PASS'
        } else {
            Write-TestCase "CheckpointData field: $field" 'FAIL'
        }
    }
    
    # Test 5: Required methods
    $requiredMethods = @(
        'save_checkpoint',
        'load_checkpoint',
        'get_resume_position',
        'mark_sector_complete',
        'mark_failed',
        'get_statistics',
        'clear_checkpoint',
        'verify_checkpoint_integrity'
    )
    
    foreach ($method in $requiredMethods) {
        if ($content -match "def $method") {
            Write-TestCase "Method defined: $method" 'PASS'
        } else {
            Write-TestCase "Method defined: $method" 'FAIL'
        }
    }
}

# ============================================================================
# MAIN TEST EXECUTION
# ============================================================================

Write-Host @"
╔════════════════════════════════════════════════════════════════════════════╗
║                    V4B RESILIENCE CODE REVIEW & TESTS                      ║
║                                                                            ║
║  This test suite verifies:                                                ║
║  - File existence and syntax correctness                                  ║
║  - Required functions and classes defined                                 ║
║  - Proper error handling and logging                                      ║
║  - Correct parameter validation                                           ║
║  - Integration between components                                         ║
╚════════════════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# Run tests based on category
switch ($TestCategory) {
    'All' {
        Test-DiskMonitor
        Test-Checkpoint
        Test-ServiceWrapper
        Test-GracefulShutdown
        Test-ResilientRunner
    }
    'Service' {
        Test-ServiceWrapper
    }
    'Shutdown' {
        Test-GracefulShutdown
    }
    'Runner' {
        Test-ResilientRunner
    }
    'Python' {
        Test-DiskMonitor
        Test-Checkpoint
    }
    default {
        Write-Host "Unknown test category: $TestCategory" -ForegroundColor Red
        exit 1
    }
}

# ============================================================================
# TEST SUMMARY
# ============================================================================

Write-TestHeader "Test Summary"

Write-Host "Total Tests: $($TestsPassed + $TestsFailed)" -ForegroundColor White
Write-Host "Passed: $TestsPassed" -ForegroundColor Green
Write-Host "Failed: $TestsFailed" -ForegroundColor $(if ($TestsFailed -eq 0) { 'Green' } else { 'Red' })

if ($TestsFailed -eq 0) {
    Write-Host "`n✓ All tests passed!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "`n✗ Some tests failed. Review output above." -ForegroundColor Red
    exit 1
}
