# Locate an existing user-level conda installation on a self-hosted Windows runner.
# No administrator privileges, new packages, or environment changes are required.
param([string]$EnvironmentName = "asian-options")
$ErrorActionPreference = "Stop"
if (-not $IsWindows -and $PSVersionTable.PSEdition -eq "Core") {
    throw "This helper is only intended for a Windows GitHub Actions runner."
}
$candidates = @()
if ($env:CONDA_EXE) { $candidates += $env:CONDA_EXE }
$found = Get-Command conda.exe -ErrorAction SilentlyContinue
if ($found) { $candidates += $found.Source }
foreach ($folder in @(
    "$env:USERPROFILE\miniconda3", "$env:USERPROFILE\anaconda3",
    "$env:USERPROFILE\miniforge3", "$env:USERPROFILE\mambaforge",
    "$env:LOCALAPPDATA\miniconda3", "$env:LOCALAPPDATA\anaconda3",
    "$env:LOCALAPPDATA\miniforge3",
    "$env:LOCALAPPDATA\Programs\miniconda3",
    "$env:LOCALAPPDATA\Programs\Miniconda3",
    "$env:LOCALAPPDATA\Programs\Anaconda3",
    "C:\ProgramData\miniconda3", "C:\ProgramData\anaconda3"
)) {
    $candidates += (Join-Path $folder "Scripts\conda.exe")
}
$conda = $null
foreach ($candidate in ($candidates | Select-Object -Unique)) {
    if ($candidate -and (Test-Path -LiteralPath $candidate -PathType Leaf)) {
        $conda = (Resolve-Path -LiteralPath $candidate).Path
        break
    }
}
if (-not $conda) {
    throw "Conda executable not found for runner user $env:USERNAME. Ensure the runner is running while the same Windows user is logged in, or add conda.exe to that user's PATH."
}
Write-Host "Using existing conda at $conda"
& $conda run --no-capture-output -n $EnvironmentName python -c "import sys, numpy, scipy; print('Conda Python:', sys.executable)"
if ($LASTEXITCODE -ne 0) {
    throw "Conda environment '$EnvironmentName' is not available for Windows user $env:USERNAME. Create/activate it under the SAME account as the runner."
}
# GitHub's GITHUB_ENV/GITHUB_PATH are UTF-8 files *without BOM*. Windows
# PowerShell 5.1 Out-File -Encoding utf8 writes a BOM, so use .NET explicitly.
$utf8 = New-Object System.Text.UTF8Encoding($false)
if ($env:GITHUB_ENV) {
    [System.IO.File]::AppendAllText($env:GITHUB_ENV, "CONDA_EXE=$conda" + [Environment]::NewLine, $utf8)
    if ($env:GITHUB_SHA -and $env:GITHUB_SHA.Length -ge 8) {
        [System.IO.File]::AppendAllText($env:GITHUB_ENV, "SHORT_SHA=$($env:GITHUB_SHA.Substring(0,8))" + [Environment]::NewLine, $utf8)
    }
}

# MiKTeX commonly installs in the user's profile on non-admin university PCs.
# Discover an existing installation; NEVER install or update TeX here.
$texFolders = @(
    "$env:LOCALAPPDATA\Programs\MiKTeX\miktex\bin\x64",
    "$env:LOCALAPPDATA\MiKTeX\miktex\bin\x64",
    "$env:APPDATA\MiKTeX\miktex\bin\x64",
    "$env:ProgramFiles\MiKTeX\miktex\bin\x64",
    "C:\Program Files\MiKTeX\miktex\bin\x64"
)
foreach ($texDir in $texFolders) {
    if (-not (Test-Path -LiteralPath (Join-Path $texDir "xelatex.exe") -PathType Leaf)) {
        continue
    }
    $env:PATH = "$texDir;$env:PATH"
    if ($env:GITHUB_PATH) {
        [System.IO.File]::AppendAllText($env:GITHUB_PATH, $texDir + [Environment]::NewLine, $utf8)
    }
    Write-Host "Located existing MiKTeX: $texDir"
    break
}
Write-Host "Environment '$EnvironmentName' is ready; no installs performed."
