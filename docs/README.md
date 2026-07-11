# PGA Diagnostics System — Documentation Index

**Status:** canonical navigation
**Owner:** Paul Gibbons
**Last reviewed:** 2026-07-11

This directory is the operating documentation for the PGA diagnostics and AI-tools system spanning:

- `paulggibbons/adaptive_adoption`
- `paulggibbons/pg-advisory-astro`
- Supabase project `Jarvis_paulg` (`dgzulkjyevijzznvfipi`)

## Start here

1. **[SYSTEM-OVERVIEW.md](SYSTEM-OVERVIEW.md)** — the master map: system boundaries, systems of record, end-to-end flow, and where to make changes.
2. **[ARCHITECTURE.md](ARCHITECTURE.md)** — detailed two-repository manifest and deployment architecture.
3. **[SUPABASE-SCHEMA.md](SUPABASE-SCHEMA.md)** — current database tables, RLS policies, RPCs, and diagnostic data flow.
4. **[TOOL-BUILD-PROTOCOL.md](TOOL-BUILD-PROTOCOL.md)** — practical protocol for adding scored diagnostics, self-scored assessments, interactive tools, canvases, and generators.
5. **[OPERATIONS.md](OPERATIONS.md)** — publish, edit, deprecate, validate, rebuild, and roll back.
6. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** — known failure modes and fixes.
7. **[DECISIONS.md](DECISIONS.md)** — architectural decisions, their rationale, consequences, and revisit conditions.

## Authority rule

Do not maintain a second, competing copy of this architecture in Obsidian, Drive, or another repository.

A note elsewhere may point here, but durable system documentation belongs with the implementation and must change in the same pull request as the architecture it describes.

## Documentation update rule

Any change to one of the following must update the relevant document in this directory:

- Supabase tables, constraints, RLS policies, or RPCs
- manifest schema or generation process
- tool lifecycle/status rules
- website diagnostic layout or renderer behavior
- response collection, benchmark logic, or privacy policy
- deployment and rollback process
- source-of-truth responsibilities

When documents disagree, treat the disagreement as a defect. Resolve it explicitly in the next pull request rather than choosing whichever file is convenient.