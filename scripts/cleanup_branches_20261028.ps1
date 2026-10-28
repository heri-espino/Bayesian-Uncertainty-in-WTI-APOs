# Archive and prune old GitHub branches, preserving unique history as Git tags.
# Run from any branch. No local checkout, merge, reset, or file deletion.
# Preview: powershell -ExecutionPolicy Bypass -File .\scripts\cleanup_branches_20261028.ps1
# Apply:   powershell -ExecutionPolicy Bypass -File .\scripts\cleanup_branches_20261028.ps1 -Apply
param([switch]$Apply)

$ErrorActionPreference = "Stop"
$root = (& git rev-parse --show-toplevel)
if ($LASTEXITCODE -ne 0 -or -not $root) {
    throw "Run from inside the WTI APO Git repository."
}
Push-Location $root.Trim()
try {
    $remote = (& git remote get-url origin | Select-Object -First 1)
    if ($LASTEXITCODE -ne 0 -or $remote -notmatch 'github[.]com[:/]heri-espino/Bayesian-Uncertainty-in-WTI-APOs([.]git)?$') {
        throw "Unexpected origin remote. Refusing to change branches."
    }

    & git fetch origin --prune "+refs/heads/*:refs/remotes/origin/*"
    if ($LASTEXITCODE -ne 0) { throw "git fetch failed" }
    $manifestText = (& git show "refs/remotes/origin/main:docs/branch_cleanup_inventory_2026-10-28.tsv") -join [Environment]::NewLine
    if ($LASTEXITCODE -ne 0 -or -not $manifestText) { throw "Missing approved branch inventory" }
    $manifest = @($manifestText | ConvertFrom-Csv -Delimiter ([char]9))
    if ($manifest.Count -ne 47) { throw "Unexpected inventory size: $($manifest.Count)" }

    $headLines = @(& git ls-remote --heads origin)
    if ($LASTEXITCODE -ne 0) { throw "Could not list remote branch heads" }
    $remoteHeads = @{}
    foreach ($line in $headLines) {
        if ($line -match '^([a-f0-9]{40})\s+refs/heads/(.+)$') {
            $remoteHeads[$Matches[2]] = $Matches[1]
        }
    }
    $tagLines = @(& git ls-remote --tags --refs origin "refs/tags/archive/branches-20261028/*")
    if ($LASTEXITCODE -ne 0) { throw "Could not list archive tags" }
    $remoteTags = @{}
    foreach ($line in $tagLines) {
        if ($line -match '^([a-f0-9]{40})\s+refs/tags/(.+)$') {
            $remoteTags[$Matches[2]] = $Matches[1]
        }
    }

    $kept = 0; $deleted = 0; $tagged = 0; $skipped = 0; $planned = 0
    foreach ($item in $manifest) {
        $branch = [string]$item.branch
        $expected = [string]$item.expected_sha
        $decision = [string]$item.decision
        if ($branch -notmatch '^[A-Za-z0-9][A-Za-z0-9._/-]*$' -or $expected -notmatch '^[a-f0-9]{40}$') {
            throw "Invalid inventory entry $branch"
        }
        if ($decision -eq "keep") {
            Write-Host "[KEEP] $branch"
            $kept++
            continue
        }
        if ($decision -ne "archive_if_unmerged_then_delete") { throw "Unexpected disposition: $branch" }
        if (-not $remoteHeads.ContainsKey($branch)) {
            Write-Host "[SKIP absent] $branch"
            $skipped++
            continue
        }
        $actual = [string]$remoteHeads[$branch]
        if ($actual -ne $expected) {
            Write-Warning "SKIP $branch: remote head changed from inventory SHA. No deletion."
            $skipped++
            continue
        }

        & git merge-base --is-ancestor $expected refs/remotes/origin/main
        $isMerged = ($LASTEXITCODE -eq 0)
        if ($LASTEXITCODE -notin @(0,1)) { throw "Cannot inspect merge ancestry: $branch" }
        $tag = "archive/branches-20261028/$branch"
        $tagRef = "refs/tags/$tag"
        if (-not $isMerged) {
            if ($remoteTags.ContainsKey($tag)) {
                if ($remoteTags[$tag] -ne $expected) {
                    throw "Conflicting existing archive tag: $tag"
                }
                Write-Host "[ARCHIVED] $branch"
            } elseif ($Apply) {
                & git cat-file -e "$($expected)^{commit}"
                if ($LASTEXITCODE -ne 0) { throw "Missing commit object for $branch" }
                Write-Host "[ARCHIVE] $branch -> $tag"
                & git push origin "$($expected):$tagRef"
                if ($LASTEXITCODE -ne 0) { throw "Failed to push archive tag: $tag" }
                $check = @(& git ls-remote --tags --refs origin $tagRef)
                if ($LASTEXITCODE -ne 0 -or $check.Count -ne 1 -or $check[0] -notmatch "^$expected\s+") {
                    throw "Archive tag verification failed: $tag"
                }
                $remoteTags[$tag] = $expected
                $tagged++
            } else {
                Write-Host "[PREVIEW tag] $branch -> $tag"
            }
        }

        if ($Apply) {
            Write-Host "[DELETE] $branch"
            & git push "--force-with-lease=refs/heads/$($branch):$expected" origin ":refs/heads/$branch"
            if ($LASTEXITCODE -ne 0) { throw "Git refused deletion: $branch" }
            $deleted++
        } else {
            Write-Host "[PREVIEW delete] $branch"
            $planned++
        }
    }

    if ($Apply) {
        Write-Host "DONE: $deleted remote branches deleted; $tagged archive tags added; $kept kept; $skipped skipped."
    } else {
        Write-Host "DRY RUN: $planned branches eligible; $kept kept; $skipped skipped. No changes made."
        Write-Host "To apply, run this script with -Apply or run the manual GitHub workflow."
    }
} finally {
    Pop-Location
}
