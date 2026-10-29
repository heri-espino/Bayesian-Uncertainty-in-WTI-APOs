# Install the cuted.sty dependency for Wiley, on a non-admin MiKTeX runner.
# Prefer the native MiKTeX package database. When it is stale or the selected
# mirror lacks sttools, derive cuted.sty from the official CTAN LPPL-1.3 sources
# into paper/build/local_tex/ (ignored by Git, copied into disposable stage).
# This downloads a LaTeX package only, NEVER financial/market data.
$ErrorActionPreference = "Stop"

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$miktex = Get-Command miktex.exe -ErrorAction Stop
$kpsewhich = Get-Command kpsewhich.exe -ErrorAction Stop

function Find-Cuted {
    $found = @(& $kpsewhich.Source cuted.sty 2>$null)
    if ($LASTEXITCODE -eq 0 -and $found.Count -gt 0) {
        return $found[0]
    }
    return $null
}

$existing = Find-Cuted
if ($existing) {
    Write-Host "MiKTeX already resolves cuted.sty: $existing"
} else {
    Write-Host "cuted.sty is missing. Refreshing the MiKTeX package database (user mode)."
    & $miktex.Source packages update-package-database
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "MiKTeX database refresh failed; attempting installation and CTAN fallback."
    }
    & $miktex.Source packages install sttools
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "MiKTeX could not install sttools (e.g. unknown package). Trying official CTAN source."
    }
    $existing = Find-Cuted
}

$localPackageDir = Join-Path $repo "paper\build\local_tex"
if (-not $existing) {
    $localCuted = Join-Path $localPackageDir "cuted.sty"
    if (-not (Test-Path -LiteralPath $localCuted -PathType Leaf)) {
        $ctan = "https://mirrors.ctan.org/macros/latex/contrib/sttools.zip"
        $downloadDir = Join-Path $repo "paper\build\local_sttools_download"
        $archive = Join-Path $downloadDir "sttools.zip"
        $extractDir = Join-Path $downloadDir "source"
        New-Item -ItemType Directory -Force -Path $downloadDir, $localPackageDir | Out-Null
        Write-Host "Obtaining sttools LPPL source from $ctan"
        # Windows PowerShell 5.1 on university PCs sometimes defaults to old TLS.
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        Invoke-WebRequest -Uri $ctan -OutFile $archive -UseBasicParsing -MaximumRedirection 10
        if (-not (Test-Path -LiteralPath $archive) -or (Get-Item $archive).Length -lt 4000) {
            throw "CTAN did not return a valid sttools archive."
        }
        Expand-Archive -LiteralPath $archive -DestinationPath $extractDir -Force
        $insFiles = @(Get-ChildItem -Path $extractDir -Filter sttools.ins -File -Recurse)
        if ($insFiles.Count -ne 1) {
            throw "Expected one sttools.ins in the official CTAN source ZIP; got $($insFiles.Count)."
        }
        $sourceDir = $insFiles[0].Directory.FullName
        if (-not (Test-Path -LiteralPath (Join-Path $sourceDir "cuted.dtx"))) {
            throw "CTAN archive does not contain cuted.dtx alongside sttools.ins."
        }
        $latex = Get-Command latex.exe -ErrorAction Stop
        Write-Host "Extracting cuted.sty from CTAN source using latex sttools.ins."
        Push-Location $sourceDir
        try {
            & $latex.Source -interaction=nonstopmode -halt-on-error sttools.ins
            if ($LASTEXITCODE -ne 0) {
                throw "LaTeX docstrip extraction failed for the CTAN sttools source."
            }
        } finally {
            Pop-Location
        }
        $generated = Join-Path $sourceDir "cuted.sty"
        if (-not (Test-Path -LiteralPath $generated) -or (Get-Item $generated).Length -lt 1000) {
            throw "CTAN extraction did not create a plausible cuted.sty file."
        }
        Copy-Item -LiteralPath $generated -Destination $localCuted -Force
    }
    Write-Host "Using locally generated LPPL cuted.sty at $localCuted (JFM stage only)."
} else {
    Write-Host "Ready: $existing"
}

# Best effort only: some MiKTeX versions restrict editing on-the-fly package
# preferences from an unattended terminal. Do not fail the build for that.
$initexmf = Get-Command initexmf.exe -ErrorAction SilentlyContinue
if ($initexmf) {
    & $initexmf.Source '--set-config-value=[MPM]AutoInstall=yes'
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "Could not set MiKTeX automatic installation preference; other missing packages may require a separate installation."
    }
}
Write-Host "Wiley cuted.sty preflight complete. No financial market data were accessed."
