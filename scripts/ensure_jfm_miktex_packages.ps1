# Repair missing dependencies for the existing, user-level MiKTeX installation.
# Does not require administrator access or download financial market data.
# The WileyNJDv5 class requires cuted.sty from the MiKTeX package sttools.
$ErrorActionPreference = "Stop"

$miktex = Get-Command miktex.exe -ErrorAction SilentlyContinue
$kpsewhich = Get-Command kpsewhich.exe -ErrorAction SilentlyContinue
if (-not $miktex -or -not $kpsewhich) {
    throw "MiKTeX tools not on PATH for the runner user. Check scripts/resolve_conda_windows_runner.ps1."
}

$existing = & $kpsewhich.Source cuted.sty
if ($LASTEXITCODE -ne 0) { $existing = $null }
if (-not $existing) {
    Write-Host "Missing cuted.sty; installing only the required MiKTeX package sttools in user mode."
    # Never use --admin; this must run in the same non-admin Windows user as the runner.
    & $miktex.Source packages install sttools
    if ($LASTEXITCODE -ne 0) { throw "User-mode MiKTeX installation of sttools failed." }
} else {
    Write-Host "Already installed: $($existing | Select-Object -First 1)"
}

$installed = & $kpsewhich.Source cuted.sty
if ($LASTEXITCODE -ne 0 -or -not $installed) {
    throw "MiKTeX still cannot locate cuted.sty after installing sttools."
}
Write-Host "Ready: $($installed | Select-Object -First 1)"

# In a headless runner, an interactive Install/Cancel prompt cannot be answered.
# Enable MiKTeX's documented per-user on-the-fly package installation for
# subsequent missing Wiley dependencies (never system-wide / --admin).
$initexmf = Get-Command initexmf.exe -ErrorAction SilentlyContinue
if (-not $initexmf) { throw "MiKTeX initexmf.exe not found on PATH." }
& $initexmf.Source '--set-config-value=[MPM]AutoInstall=yes'
if ($LASTEXITCODE -ne 0) {
    throw "Could not enable user-level MiKTeX automatic package installation."
}
Write-Host "MiKTeX per-user automatic package installation enabled for future missing LaTeX dependencies."
