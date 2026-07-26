# Stream E: Bootstrap Rust toolchain on Windows
# Idempotent: safe to run multiple times
# Sets stable Rust toolchain, reports versions, probes symlink status

param(
    [switch]$Verbose = $false
)

$ErrorActionPreference = "Stop"

Write-Host "=== Stream E Rust Toolchain Bootstrap ===" -ForegroundColor Cyan

# 1. Check if rustup is available
try {
    $rustup_version = & rustup --version 2>&1
    Write-Host "rustup found: $rustup_version" -ForegroundColor Green
} catch {
    Write-Host "ERROR: rustup not installed. Install from https://rustup.rs/" -ForegroundColor Red
    exit 1
}

# 2. Set stable toolchain if not already set
Write-Host "Configuring stable Rust toolchain..." -ForegroundColor Cyan
try {
    & rustup default stable 2>&1 | Out-Null
    Write-Host "Stable toolchain set." -ForegroundColor Green
} catch {
    Write-Host "WARNING: Could not set default toolchain: $_" -ForegroundColor Yellow
}

# 3. Report toolchain versions
Write-Host "`nToolchain versions:" -ForegroundColor Cyan
$cargo_version = & cargo --version 2>&1
$rustc_version = & rustc --version 2>&1
$host_triple = & rustc -vV 2>&1 | Select-String "host:" | ForEach-Object { $_.ToString().Split(":")[1].Trim() }

Write-Host "  cargo: $cargo_version"
Write-Host "  rustc: $rustc_version"
Write-Host "  host:  $host_triple"

# 4. Report GPU
Write-Host "`nGPU:" -ForegroundColor Cyan
try {
    $gpu_info = & nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader 2>&1
    Write-Host "  $gpu_info"
} catch {
    Write-Host "  nvidia-smi not available (GPU work will be CPU-only)" -ForegroundColor Yellow
}

# 5. Probe symlinks
Write-Host "`nSymlink status (dangling = broken on this Windows worktree):" -ForegroundColor Cyan
$symlinks = @("core", "core_wasm", "logs", "archives", "ui_loom", "EuclidClusterViz", "additional_storage")
$repo_root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

foreach ($link in $symlinks) {
    $path = Join-Path $repo_root $link
    if (Test-Path $path) {
        $resolved = (Get-Item $path).FullName
        if ($resolved -match "^/mnt/|^\\\\") {
            Write-Host "  $link -> DANGLING (Linux path: $resolved)" -ForegroundColor Red
        } else {
            Write-Host "  $link -> OK (real directory)" -ForegroundColor Green
        }
    } else {
        Write-Host "  $link -> MISSING" -ForegroundColor Yellow
    }
}

Write-Host "`n=== Bootstrap complete ===" -ForegroundColor Green
exit 0
