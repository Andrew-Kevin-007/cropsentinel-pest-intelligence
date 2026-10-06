# Contributor Brief: FieldGuard Brand Exploration

This task is intentionally isolated so a second agent can work without conflicts with the CropSentinel application.

## Context

The production application is currently branded **CropSentinel**. Do not rename the application or edit its runtime code in this task.

Your independent brand concept is **FieldGuard**: a calm, trustworthy field-observation product for growers and agricultural students.

## Your task

Create a brand exploration package for FieldGuard. The package should help the main project decide whether to adopt a new public name later.

### Files you own

Create or edit only these files:

```text
docs/brand/fieldguard-brand.md
docs/brand/fieldguard-copy.json
```

Create the `docs/brand/` directory if it does not exist. Do not edit `app.py`, `train.py`, `data/recommendations.json`, dependency files, Docker files, or existing documentation.

## Deliverable requirements

`fieldguard-brand.md` must contain:

- One-sentence positioning statement.
- Three naming alternatives and why FieldGuard is preferred.
- Brand voice: trustworthy, practical, calm, and evidence-aware.
- A light-mode color palette with accessible contrast intent.
- Typography direction using available web-safe or open fonts.
- Logo and icon direction described in words, not copyrighted artwork.
- Five short UI headline options.
- Five safety-aware empty-state or error messages.

`fieldguard-copy.json` must contain this shape:

```json
{
  "brand": "FieldGuard",
  "tagline": "...",
  "headlines": ["..."],
  "empty_states": ["..."],
  "safety_notice": "..."
}
```

## Acceptance criteria

- Only the two owned files are changed.
- JSON parses successfully.
- No pesticide dosage, product prescription, or unsupported accuracy claim is added.
- Copy is concise and suitable for a student agricultural product.
- The document is a proposal, not a request to rename the current app.

## Git workflow

Create a branch named `brand/fieldguard-exploration`. Commit only your owned files with:

```text
docs: add FieldGuard brand exploration
```

Before handing back the work, run:

```powershell
python -c "import json; json.load(open('docs/brand/fieldguard-copy.json', encoding='utf-8'))"
git diff --name-only main...HEAD
```

The final diff should contain only `docs/brand/fieldguard-brand.md` and `docs/brand/fieldguard-copy.json`.

## Integration rule

Do not merge or cherry-pick your branch yourself. Report the commit hash to the main agent. The main agent will review the brand proposal and decide whether any part should be integrated into CropSentinel.