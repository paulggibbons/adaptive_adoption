# Adaptive Adoption — Troubleshooting

Failure modes and how to diagnose them. Read alongside [ARCHITECTURE.md](./ARCHITECTURE.md) and [OPERATIONS.md](./OPERATIONS.md).

## "I pushed to adaptive_adoption main but the live site didn't update"

Expected latency: ~30–60s after push. If it's been 5+ minutes:

1. **Check the GitHub webhook fired:**
   ```bash
   gh api repos/paulggibbons/adaptive_adoption/hooks/622310725/deliveries --jq '.[0:3]'
   ```
   The most recent delivery should be within seconds of your push, with `status: "OK"` and `status_code: 201` (Vercel "deployment queued").

   - If `status_code` is something else (4xx/5xx): Vercel rejected the ping. Probably the deploy hook URL is stale or the project was deleted. Check Vercel dashboard.
   - If no recent delivery: GitHub didn't fire the webhook. Webhook may have been disabled. Re-enable in `https://github.com/paulggibbons/adaptive_adoption/settings/hooks`.

2. **Check Vercel actually built:**
   - Vercel dashboard → `pg-advisory-astro` → Deployments
   - Top deployment should be timestamped near your push, status `Ready`.
   - If status is `Error`: click in to see the build log.
   - If no recent deployment: the deploy hook never fired (see step 1) or Vercel paused the project.

3. **Check the manifest commit actually touched `tools.yml`:**
   ```bash
   git log -1 --name-only main
   ```
   If your change was to a different file (e.g. just docs/README), Vercel built but the manifest didn't change so the live site won't visibly differ. This is expected — only `tools.yml` changes affect the diagnostic pages.

4. **Force a rebuild** if everything looks fine but the site is stale:
   ```bash
   curl -X POST 'https://api.vercel.com/v1/integrations/deploy/prj_anehJW3ICdzJEtynlCT4Bbn4kcSm/ltoWiHb6Px'
   ```

## "Validator fails locally with errors I don't understand"

The validator outputs include the slug and the field path. Example:

```
ERROR FAIL slug='my-tool' [framework_mapping → domain]: 'banana' is not one of [...]
```

This means: the entry with slug `my-tool` has `framework_mapping.domain = 'banana'` which is not in the enum.

**Common causes:**

- **Typo in an enum value.** Check `schemas/tools.schema.json` for the valid set.
- **Status changed to `live` without populating required fields.** Run:
  ```bash
  python scripts/validate_manifests.py 2>&1 | grep 'status=live requires'
  ```
- **`related_tools` references a slug that doesn't exist.** Either fix the slug or remove the dangling reference.
- **YAML syntax error in the file** — validator will say `Missing top-level 'tools' key` or similar. Open the file in an editor with YAML linting.

## "Pressure tests fail"

```bash
python scripts/pressure_test_manifest.py --verbose
```

The `--verbose` flag shows stderr for any failing test. Two failure modes:

- **`expected rejection (rc=1) but validator accepted (rc=0)`** — the validator is leaking. Some failure mode that should be caught isn't. Look at the mutation function for that test (e.g., `mutate_dup_slug`) and figure out what should have rejected it.
- **`expected acceptance (rc=0) but validator rejected (rc=1)`** — the validator is over-strict. Some valid input is being rejected. Look at the test definition and decide whether the schema rule is too tight or the test's expectation is wrong.

If a test passes with `PASS*` (asterisk), the validator correctly rejected but the specific stderr substring wasn't found. That's tolerable — the rejection is what matters — but worth investigating if you want better error messages.

## "MkDocs build fails on CI"

Look at the failing job in `.github/workflows/mkdocs.yml`. Common causes:

1. **`validate-manifests` job failed** — see the previous troubleshooting section. Fix the manifest, push again.
2. **Generator failed** — `scripts/generate_tool_pages.py` references a template that doesn't exist, or chokes on a malformed entry. Check the build log for a Python traceback. Most likely fix: an entry has a field shape the generator doesn't handle. Either fix the entry or extend the generator.
3. **`mkdocs build` failed** — broken markdown link, missing image, etc. Build log shows which file/line.

## "URL health check failed: PASS X/13"

`scripts/check_live_urls.py` runs in CI as a non-blocking warning. If you see `FAIL N/13`:

1. **Identify which URL(s) failed:** the script outputs a table; look for rows that don't say `200 OK`.
2. **Visit the URL manually.** If it 404s, the page was renamed/deleted. Update `astro_url` in the manifest OR restore the page.
3. **If it 5xx's:** Vercel build broke. Check Vercel dashboard for an Error deployment.
4. **If it times out:** Vercel may be cold-starting or under load. Re-run the check in a minute. Persistent timeouts mean Vercel's edge has an issue — open a support ticket.

The check is non-blocking precisely because transient flakes happen. Don't lose sleep over a single failed run.

## "I see broken styling on a diagnostic page in production"

Most likely a CSS regression (we hit this hard during Phase 3 — see the session trace at `2026-05-12-phase-3-completion-and-css-recovery.md`).

**Diagnosis flow:**

1. **Open browser devtools on the broken page.** Inspect the element that looks wrong.
2. **Look at its `Computed Styles` panel.** If most rules show "user agent stylesheet" (browser defaults), the CSS for that class isn't loading.
3. **Search the codebase for the class name:**
   ```bash
   cd pg-advisory-astro
   grep -rn "\.broken-class-name" src/
   ```
   The class should be defined somewhere — either in `src/styles/`, in a `<style>` block in a page shell, or in the `DiagnosticPageLayout`'s scoped styles.
4. **If nowhere:** the class is orphaned. Find its definition in one of the `.before-v12.bak` files in `src/pages/diagnostics/` and decide where to put it (per-page inline `<style is:global>` block, or `src/styles/diagnostic-chrome.css` for shared rules).

**Quick fix template:** add the orphaned style block to the page's `.astro` file as `<style is:global>` at the bottom. Build + push.

## "Astro build fails on Vercel with manifest fetch error"

Build log will show something like `[manifest] Raw GitHub fetch failed (...); falling back to snapshot`.

If you see this:

1. **GitHub is intermittently down** — the snapshot fallback fired. Production deployed from snapshot. Manifest changes since the last snapshot refresh are NOT in production. **Refresh the snapshot** when GitHub recovers (see [OPERATIONS.md](./OPERATIONS.md) → "Refresh the snapshot fallback").
2. **The raw GitHub URL changed** — main branch was renamed, repo was renamed, repo went private, etc. Update `MANIFEST_URL` in `pg-advisory-astro/src/lib/manifest.ts`.
3. **Rate-limited by GitHub** — unlikely but possible with many concurrent builds. Add a GitHub token to the fetch headers for higher rate limits.

If the build log shows the fetch SUCCEEDED but the snapshot warning still appeared, that's a code bug in manifest.ts — the fallback logic is misfiring.

## "Vercel deploy succeeded but the page shows old content"

Most likely a browser cache issue:

1. **Hard reload** (Cmd+Shift+R / Ctrl+Shift+R).
2. **Check `<meta name="manifest-version">` in page source.** It should match the latest commit SHA on `adaptive_adoption/main` that touched `data/tools.yml`:
   ```bash
   curl -s https://paulgibbonsadvisory.com/diagnostics/aabi | grep manifest-version
   git -C ~/repos/adaptive_adoption log -1 --format='%H' main -- data/tools.yml
   ```
   Same SHA = fresh. Different SHA = Vercel hasn't rebuilt, or rebuild used snapshot fallback.

3. **Check Vercel CDN cache** — Vercel sometimes serves cached HTML at the edge for a few minutes after a deploy. Wait 2–3 minutes and try again.

## "I want to revert just a single tool's edit without reverting the commit"

Edit `data/tools.yml` to undo your change in that one entry. Commit + push. The webhook fires a rebuild with the reverted state. Net effect: one tool reverts, everything else stays current.

## "How do I know if the webhook is still alive?"

```bash
gh api repos/paulggibbons/adaptive_adoption/hooks/622310725 --jq '{active, last_response, events}'
```

- `active: true` means GitHub still has it enabled.
- `last_response.code: 201` means Vercel accepted the last delivery.
- `events: ["push"]` means it fires on push (which is what we want).

To re-test:
```bash
gh api repos/paulggibbons/adaptive_adoption/hooks/622310725/pings --method POST
```

Then check Vercel for a new deployment.

## "I deleted a tool entry from tools.yml. What happens?"

1. CI validates — passes (deletion is valid).
2. Webhook fires, Vercel rebuilds.
3. **In pg-advisory-astro: `getTool('deleted-slug')` throws** at build time:
   ```
   [manifest] No tool with slug "deleted-slug" in data/tools.yml
   ```
   This **breaks the Astro build.** Production stays on the previous deploy.

**The fix:** if you're deleting a tool, also delete its `src/pages/diagnostics/<slug>.astro` page shell in pg-advisory-astro at the same time (separate PR, ideally before the manifest delete).

**Safer alternative:** mark the tool `status: archived` instead of deleting. The schema requires `archived_reason` and `dates.archived` when archived, but `getTool()` still returns the entry so the page doesn't break. See [OPERATIONS.md](./OPERATIONS.md) → "Deprecate a tool".

## "Something went deeply wrong and I need to start fresh"

The git backup tags are immutable on origin:

```bash
cd adaptive_adoption
git checkout pre-phase-3c-backup-2026-05-12
# This is a detached HEAD on the state right before Phase 3c started.
# Cherry-pick any commits you want to keep, then force-push main.

cd ../pg-advisory-astro
git checkout pre-phase-3b-pr-b-backup-2026-05-12
# Same — pre-Phase 3b state.
```

Reset main only after exhausting other options. It's destructive and will require everyone with a local clone to re-clone.
