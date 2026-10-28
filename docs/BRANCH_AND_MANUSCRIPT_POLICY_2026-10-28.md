# Canonical branches and manuscript tracks (28 October 2026)

## Distinguish manuscripts from studies

There are **three manuscript/journal adaptations but only two distinct research projects**:

- **Paper A — REMEF (current submission priority)**: `paper/remef/`, editable Word build and blinded PDF. The revised source is on `main`.
- **Paper A — Wiley / Journal of Futures Markets (JFM; alternative venue, not a second independent paper)**: `paper/manuscript/` and `paper/build.py`; the LaTeX variant is preserved on `main`. It should not be simultaneously submitted with the substantially overlapping REMEF Paper A.
- **Paper B — Journal of Commodity Markets (JCM; distinct proposed structural CL-fixing/futures-curve study)**: `paper/jcm/` and `research/JCM_PAPER_B_NOVELTY_MATRIX_AND_STUDY_DESIGN_2026-10-27.md`. The existing JCM CAS build may reuse earlier Paper A sections and is NOT a finished independent Paper B. PR #114 is open and explicitly says not to merge without author approval. Do not commission new experiments just to clean branches.

## Branch strategy

**One durable source of truth: `main`.** The three manuscript directories already coexist there; *journal versions do not require separate permanent branches*. Use a short-lived topic branch only when a PR is necessary, and delete it after merging.

One temporary active branch may remain for genuinely separate, unmerged JCM Paper B planning (`paper/jcm-independent-research-track`). Keep its PR #114 intact pending the author's choice. Also preserve the currently active `fix/remef-svg-media-extension-20261019` / PR #84 until it is resolved, and `results/aao-databento-pilot-2023h1-20261026` until its unique science/results commits are integrated or archived. Do not merge the whole results branch into `main` just to move Word/PDF files.

**Latest REMEF review transfer:** On 2026-10-28, the updated blinded `draft2` Word/PDF blobs were transferred directly from the results branch into `main` as canonical filenames `paper/remef/review/remef_blinded_draft.docx` and `.pdf`. The PDF is 18 pages, corresponds to the reviewed uploaded PDF, and has empty author metadata. This was a selective two-file transfer, not a merge of unrelated experimental commits. The author-identifying Word copy remains at `paper/remef/review/remef_author_draft.docx`. These are *draft/review artifacts*, not submission clearance; figures/references, data publication chronology, licences and publisher requirements remain to be checked.

## Branch inventory and safe first-stage cleanup

GitHub's branch list on 2026-10-28 contained **47 total branches**: `main` and 46 others. Comparisons to `main` found **19 fully merged (zero unique commits)** and **27 other branches** with one or more commits not reachable from `main`. Note that squash-merged PRs can show unique commit SHAs even when their changes are represented in `main`; preserve or archive them until investigated.

To **preview only** the remote branches whose commits are entirely reachable from `main` (PowerShell, from the repository root):

```powershell
git fetch origin --prune
$merged = @(git for-each-ref --format='%(refname:short)' --merged=refs/remotes/origin/main refs/remotes/origin |
  Where-Object { $_ -like 'origin/*' -and $_ -ne 'origin/HEAD' -and $_ -ne 'origin/main' } |
  ForEach-Object { $_.Substring(7) })
$merged
```

After checking the printed branch list, **only those fully merged branches** may be deleted safely without losing their commits:

```powershell
foreach ($branch in $merged) { git push origin --delete $branch }
```

Do not blindly delete any branch not in `$merged`; it may contain historical recoveries, vendor acquisition notes, or unmerged data. The commands do not alter local working files or sparse checkout.

For a nonmerged branch that is truly obsolete, preserve the remote tip under a uniquely named `archive/` Git tag **and verify that the tag is pushed** before deleting its branch, document the original branch/ref and purpose, and preserve any live PRs. Confirm whether its unique files should instead be integrated into `main`; Git tags preserve reachability, not discoverability in the current source tree. Do not force-push or reset, and do not delete an open PR's head branch.

## Working on `main` locally

Your Windows checkout may remain on the results branch even after GitHub `main` is updated. `git push origin main` publishes the *local* `main`, not the checked-out branch; it can be rejected if local `main` is behind. Use `git fetch origin` before switching branches; if local `main` contains its own unmerged commits, inspect/backup and merge carefully rather than resetting. For manuscripts already transferred to remote `main`, no additional push is necessary.
