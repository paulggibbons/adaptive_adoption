# Adaptive Adoption — Operations Playbooks

Practical procedures for the manifest pipeline. Read alongside [ARCHITECTURE.md](./ARCHITECTURE.md).

## Add a new tool

1. **Edit `data/tools.yml`.** Add a new entry at the bottom (or wherever sort order dictates). Required fields:
   ```yaml
   - slug: my-new-tool
     name: My New Tool
     aliases: []
     type: diagnostic        # or canvas, template, etc. — see schema enum
     status: build-next      # start here; promote to "live" when shipped
     framework_mapping:
       domain: change-agility  # or leadership-delta / behavioral-governance / cross-cutting
       pillar: 01-master-the-craft  # optional, see schema for valid values
       pillar_num: 1
       pillar_name: Master the Craft
     short_description: One-line blurb for the index card.
     dates:
       created: '2026-05-12'
       last_updated: '2026-05-12'
     sort_order: 100
     tags: [change-agility, build-next]
   ```

2. **Validate locally:**
   ```bash
   python scripts/validate_manifests.py
   ```
   Must exit 0. If it fails, fix the errors before committing.

3. **Commit + push.** CI runs the same validator on the PR. Once merged, the MkDocs build regenerates tool index pages, and Vercel rebuilds pg-advisory-astro.

4. **Verify on production** within ~60s:
   - MkDocs site: check the appropriate domain's tools index (e.g., `paulggibbons.github.io/adaptive_adoption/change-agility/tools/`)
   - Astro site: if `status: live`, the new page should appear at `paulgibbonsadvisory.com/diagnostics/<slug>` — but this requires creating the page shell + widget in `pg-advisory-astro` separately (see "Promote a tool to live" below)

## Edit an existing tool

1. Edit the relevant entry in `data/tools.yml`.
2. Validate: `python scripts/validate_manifests.py`.
3. Commit + push. Webhook fires Vercel rebuild. Live in ~30–60s.

**Common edits:**
- Updating `long_description`, `short_description`, `hero_copy` — pure manifest, no Astro changes needed.
- Updating `cta` — pure manifest, no Astro changes needed.
- Updating `hero_image` — file must exist in `pg-advisory-astro/public/images/`. If you're adding a new image, that's a pg-advisory-astro commit.

## Promote a tool from `build-next` to `live`

This is more involved because `live` triggers conditional schema requirements AND requires a corresponding Astro page to exist.

1. **Build the page in pg-advisory-astro** if it doesn't exist:
   - Create `src/components/diagnostics/<WidgetName>.tsx` with the interactive widget
   - Create `src/pages/diagnostics/<page-slug>.astro` as a thin manifest-consumer:
     ```astro
     ---
     import DiagnosticPageLayout from '../../components/DiagnosticPageLayout.astro';
     import MyWidget from '../../components/diagnostics/MyWidget.tsx';
     import { getTool } from '../../lib/manifest';
     const tool = await getTool('my-new-tool');
     ---
     <DiagnosticPageLayout tool={tool}>
       <MyWidget client:load />
     </DiagnosticPageLayout>
     ```
   - Add widget-specific `<style is:global>` block at the bottom of the page shell (CSS for `.my-widget-*` classes used inside MyWidget). Use one of the existing pages (e.g., `cynefin.astro`) as a template.

2. **Update the manifest entry** to populate all required-for-live fields:
   ```yaml
   status: live
   astro_url: /diagnostics/my-new-tool   # matches the page route
   hero_copy: "Punchy one-liner under 140 chars."
   hero_image: /images/my-domain-diagram.png
   hero_image_alt: "Description for screen readers."
   long_description: |-
     Multi-paragraph editorial body. Becomes the intro text on the page.
   cta:
     primary:
       text: "Discuss your results with Paul"
       url: "mailto:paul@paulgibbonsadvisory.com"
       style: "primary"
     secondary:
       text: "All AI Tools"
       url: "/diagnostics"
       style: "secondary"
   attribution:
     - "Original framework — Gibbons (2026)"
   dates:
     ...
     built: '2026-05-12'
   ```

3. **Run pressure tests locally** to catch anything you missed:
   ```bash
   python scripts/pressure_test_manifest.py
   ```

4. Commit manifest + Astro changes in separate PRs (or one if they're tightly coupled).

## Deprecate a tool (mark as archived)

1. Update the manifest entry:
   ```yaml
   status: archived
   archived_reason: "Superseded by RIST Trust Diagnostic — see /diagnostics/rist-trust"
   dates:
     ...
     archived: '2026-05-12'
   ```
   `archived_reason` and `dates.archived` are required when status is `archived` (enforced by schema).

2. **Decide what to do with the page** in pg-advisory-astro:
   - **Option A (recommended):** keep the page rendering but the manifest entry now reads `status: archived` — the page shell still runs `getTool(slug)` and works. But you may want to add a deprecation notice or redirect.
   - **Option B:** delete the page shell file. Then the URL 404s. Add a `redirects` entry to `pg-advisory-astro/vercel.json` if you want to redirect old URLs to a replacement.
   - **Option C:** if pulling the page entirely, change `astro_url` to `null` in the manifest. Schema permits this for non-live entries.

3. Commit + push.

## Refresh the snapshot fallback

The snapshot at `pg-advisory-astro/src/data/tools.snapshot.yml` is committed audit-trail data. Refresh it occasionally so the fallback isn't years stale:

```bash
cp /path/to/adaptive_adoption/data/tools.yml /path/to/pg-advisory-astro/src/data/tools.snapshot.yml
cd /path/to/pg-advisory-astro
git add src/data/tools.snapshot.yml
git commit -m "snapshot: refresh tools.snapshot.yml from adaptive_adoption@main"
```

Run after major manifest releases (Phase 4 content expansion, etc.). Not needed for routine edits — the live fetch handles those.

## Roll back a bad production deploy

**Fast path (Vercel UI, ~30s, non-destructive):**

1. Vercel dashboard → `pg-advisory-astro` → Deployments
2. Find the last known-good deployment
3. "..." menu → **Instant Rollback**
4. Verify production reverted

**If Vercel rollback is unavailable** (e.g., the bad state is in main commit history and you need to undo the commit):

```bash
cd pg-advisory-astro
git fetch origin
git checkout main
git revert <bad-commit-sha> -m 1  # -m 1 for merge commits
git push origin main
```

Webhook fires, Vercel rebuilds with the revert applied.

**Nuclear option** (rare — only if Vercel rollback + git revert both fail):

```bash
git checkout main
git reset --hard pre-phase-3b-pr-b-backup-2026-05-12  # or another backup tag
git push --force-with-lease origin main
```

Force-push to main is destructive. Use only if other options exhausted.

## Roll back a bad manifest change

1. Identify the bad commit on `adaptive_adoption/main`.
2. `git revert <bad-sha>` and push, OR `git reset --hard <previous-sha> && git push --force-with-lease` if it's recent and uncomplicated.
3. The webhook fires → Vercel rebuilds pg-advisory-astro with the reverted manifest. Live in ~60s.

The manifest changes ALSO need to roll back on the MkDocs site (paulggibbons.github.io), but that auto-updates via the same push, so no separate action needed.

## Inspect what's currently deployed

```bash
# Check production manifest version (commit SHA of last tools.yml change)
curl -s https://paulgibbonsadvisory.com/diagnostics/aabi | grep -oP 'manifest-version" content="\K[^"]+'

# Compare against current adaptive_adoption main
cd adaptive_adoption
git log -1 --format='%H' main -- data/tools.yml
```

If they differ, the live site is stale → check Vercel for a failed build, or fire the webhook manually:

```bash
curl -X POST 'https://api.vercel.com/v1/integrations/deploy/prj_anehJW3ICdzJEtynlCT4Bbn4kcSm/ltoWiHb6Px'
```

(That URL is the active deploy hook. Hitting it any time triggers a rebuild of pg-advisory-astro from current main state.)

## Add a new schema field

1. Edit `schemas/tools.schema.json` — add the field definition. Make it optional (don't add to `required` unless absolutely necessary — it will retroactively reject all existing entries).
2. If the field has conditional logic (required for certain `status` values), implement it in `scripts/validate_manifests.py` inside `check_v12_rules()`.
3. Add a corresponding pressure test in `scripts/pressure_test_manifest.py` for the failure modes.
4. Update `src/lib/manifest.ts` in pg-advisory-astro to add the TypeScript type.
5. Update `DiagnosticPageLayout.astro` (or the relevant component) to render the field, with a fallback if absent.
6. Bump schema version in the JSON Schema description: v1.2 → v1.3.
7. Document the change in [ARCHITECTURE.md](./ARCHITECTURE.md) schema reference section.

## Trigger a Vercel rebuild without a code change

```bash
curl -X POST 'https://api.vercel.com/v1/integrations/deploy/prj_anehJW3ICdzJEtynlCT4Bbn4kcSm/ltoWiHb6Px'
```

Useful when you've updated `data/tools.yml` and pushed but Vercel didn't pick it up (rare). Also useful for testing the deploy hook.

## Run all checks locally before pushing

```bash
cd adaptive_adoption
python scripts/validate_manifests.py        # schema + v1.2 rules
python scripts/check_live_urls.py           # 13 live URLs return 200
python scripts/pressure_test_manifest.py    # 29 stress tests

cd ../pg-advisory-astro
npm run build                                # full Astro build
```

All four should pass.
