# Supply the cuted.sty dependency required by WileyNJDv5 in user-level MiKTeX.
# Never run as admin and never request licensed market data. On Windows
# PowerShell 5.1, MiKTeX may print "major issue: ... updates" to STDERR while
# returning exit code zero. Native STDERR + ErrorActionPreference=Stop otherwise
# terminates Actions despite a successful lookup. Invoke via a redirected .NET
# Process instead and assess ExitCode + STDOUT.
$ErrorActionPreference = "Stop"

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$miktex = Get-Command miktex.exe -ErrorAction Stop
$kpsewhich = Get-Command kpsewhich.exe -ErrorAction Stop

function Invoke-MiKTeXProcess {
    param(
        [Parameter(Mandatory=$true)][string]$Executable,
        [Parameter(Mandatory=$true)][string]$Arguments
    )

    $process = New-Object System.Diagnostics.Process
    $start = New-Object System.Diagnostics.ProcessStartInfo
    $start.FileName = $Executable
    $start.Arguments = $Arguments
    $start.UseShellExecute = $false
    $start.CreateNoWindow = $true
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    $process.StartInfo = $start
    try {
        if (-not $process.Start()) {
            throw "Could not start executable $Executable"
        }
        # Read both pipes concurrently to avoid deadlock if either is full.
        $stdoutTask = $process.StandardOutput.ReadToEndAsync()
        $stderrTask = $process.StandardError.ReadToEndAsync()
        $process.WaitForExit()
        return @{
            ExitCode = $process.ExitCode
            StdOut = $stdoutTask.GetAwaiter().GetResult()
            StdErr = $stderrTask.GetAwaiter().GetResult()
        }
    }
    finally {
        $process.Dispose()
    }
}

function Find-Cuted {
    $result = Invoke-MiKTeXProcess -Executable $kpsewhich.Source -Arguments "cuted.sty"
    $location = ([string]$result.StdOut).Trim()
    if ($result.ExitCode -eq 0 -and
        $location -match 'cuted\.sty$' -and
        (Test-Path -LiteralPath $location -PathType Leaf)) {
        # MiKTeX may print an update reminder on stderr despite successful
        # lookup. It is not a missing dependency or a build failure.
        return $location
    }
    if ($result.ExitCode -ne 0) {
        Write-Warning "kpsewhich returned exit code $($result.ExitCode): $($result.StdErr.Trim())"
    }
    return $null
}

$existing = Find-Cuted
if ($existing) {
    Write-Host "PASS: MiKTeX resolves cuted.sty at $existing"
    Write-Host "No MiKTeX package installation or update is necessary."
    exit 0
}

Write-Host "cuted.sty is missing; refreshing the MiKTeX package catalogue in user mode."
$refresh = Invoke-MiKTeXProcess -Executable $miktex.Source -Arguments "packages update-package-database"
if ($refresh.ExitCode -ne 0) {
    Write-Warning "Package catalogue refresh returned $($refresh.ExitCode): $($refresh.StdErr.Trim())"
}
$install = Invoke-MiKTeXProcess -Executable $miktex.Source -Arguments "packages install sttools"
if ($install.ExitCode -ne 0) {
    Write-Warning "sttools package installation returned $($install.ExitCode): $($install.StdErr.Trim())"
}
$existing = Find-Cuted
if ($existing) {
    Write-Host "PASS: cuted.sty is now available: $existing"
    exit 0
}

# Fallback only when the MiKTeX package catalogue/mirror cannot supply sttools:
# extract the official LPPL source from CTAN into a disposable, ignored folder.
# The paper builder stages ONLY the resulting cuted.sty; no vendor files change.
$localPackageDir = Join-Path $repo "paper\build\local_tex"
$localCuted = Join-Path $localPackageDir "cuted.sty"
if (-not (Test-Path -LiteralPath $localCuted -PathType Leaf)) {
    $ctan = "https://mirrors.ctan.org/macros/latex/contrib/sttools.zip"
    $downloadDir = Join-Path $repo "paper\build\local_sttools_download"
    $archive = Join-Path $downloadDir "sttools.zip"
    $extractDir = Join-Path $downloadDir "source"
    New-Item -ItemType Directory -Force -Path $downloadDir, $localPackageDir | Out-Null
    Write-Host "Downloading official CTAN sttools source (LaTeX only): $ctan"
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $ctan -OutFile $archive -UseBasicParsing -MaximumRedirection 10
    if (-not (Test-Path -LiteralPath $archive) -or (Get-Item $archive).Length -lt 4000) {
        throw "CTAN did not return a plausible sttools archive."
    }
    Expand-Archive -LiteralPath $archive -DestinationPath $extractDir -Force
    $insFiles = @(Get-ChildItem -Path $extractDir -Filter sttools.ins -File -Recurse)
    if ($insFiles.Count -ne 1) {
        throw "Expected exactly one sttools.ins in CTAN source; got $($insFiles.Count)."
    }
    $sourceDir = $insFiles[0].Directory.FullName
    if (-not (Test-Path -LiteralPath (Join-Path $sourceDir "cuted.dtx"))) {
        throw "CTAN source is missing cuted.dtx alongside sttools.ins."
    }
    $latex = Get-Command latex.exe -ErrorAction Stop
    Push-Location $sourceDir
    try {
        $extract = Invoke-MiKTeXProcess -Executable $latex.Source -Arguments "-interaction=nonstopmode -halt-on-error sttools.ins"
        if ($extract.ExitCode -ne 0) {
            throw "LaTeX docstrip extraction failed: $($extract.StdErr) $($extract.StdOut)"
        }
    }
    finally {
        Pop-Location
    }
    $generated = Join-Path $sourceDir "cuted.sty"
    if (-not (Test-Path -LiteralPath $generated) -or (Get-Item $generated).Length -lt 1000) {
        throw "LaTeX docstrip did not generate a plausible cuted.sty."
    }
    Copy-Item -LiteralPath $generated -Destination $localCuted -Force
}
Write-Host "PASS: using local CTAN cuted.sty only in the disposable Wiley staging directory: $localCuted"
