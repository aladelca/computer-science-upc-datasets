# Weekly Material Runbook

Use this runbook when executing or extending the `weekly-material-authoring` skill.

## File Map

Core skill files:

- `SKILL.md`
  Purpose: trigger conditions and high-level workflow.
- `references/weekly-material-runbook.md`
  Purpose: operational file map, commands, and approval-gate procedure.

Reusable week scaffolding:

- `scripts/scaffold_week_presentation.py`
  Purpose: discover the real week files, create `scripts/generate_week_<n>_presentation.py`, and optionally export a first scaffold PDF/PPTX.
- `src/upc_datasets/weekly_presentation.py`
  Purpose: reusable helpers for week path discovery, markdown/notebook outline extraction, scaffold slide rendering, PDF/PPTX export, and generator-script templating.
- `tests/test_weekly_presentation.py`
  Purpose: smoke coverage for the reusable week scaffolding layer.

Week 3 reference implementation for the deterministic base deck:

- `scripts/generate_week_3_presentation.py`
  Purpose: full week-specific generator with narrative structure, mathematical slides, and export path.
- `big_data_course_content/presentations/week_3.pdf`
  Purpose: deterministic Week 3 PDF export.
- `big_data_course_content/presentations/week_3.pptx`
  Purpose: deterministic Week 3 PPTX export.
- `big_data_course_content/week_03_curse_of_dimensionality_class_script.md`
  Purpose: instructor script derived from the approved Week 3 slides.

Week 3 AI beautification reference pipeline:

- `src/upc_datasets/week_3_presentation_redesign.py`
  Purpose: redesign orchestration, slide metadata, manifest handling, and provider dispatch.
- `src/upc_datasets/week_3_presentation_ai.py`
  Purpose: shared AI image-edit provider contract.
- `src/upc_datasets/week_3_presentation_openai.py`
  Purpose: OpenAI image-edit adapter.
- `src/upc_datasets/week_3_presentation_gemini.py`
  Purpose: Gemini image-edit adapter.
- `big_data_course_content/presentations/week_3_redesign_profile.json`
  Purpose: redesign style profile and prompt templates.
- `.env.week3.example`
  Purpose: example environment variables for the redesign pipeline.
- `tests/test_generate_week_3_presentation.py`
  Purpose: coverage for the Week 3 deterministic deck structure.
- `tests/test_week_3_presentation_redesign.py`
  Purpose: coverage for the redesign config and dry-run behavior.
- `plans/20260415-2139-week3-slide-redesign-pipeline.md`
  Purpose: design notes for the Week 3 redesign pipeline.

## Execution Order

1. Inspect the source material for the target week.
   Read `big_data_course_content/week_XX_*.md` and `big_data_course_content/notebooks/week_XX_*.ipynb`.
2. Inspect the current worktree.
   Run `git status --short` and look for tracked or untracked presentation pipeline files.
3. Scaffold the generator if the week does not have one yet.
   Run `python3 scripts/scaffold_week_presentation.py <week-number> --skip-build`.
4. Build the deterministic base deck.
   Run `python3 scripts/generate_week_<n>_presentation.py`.
5. Validate the base deck.
   Check slide order, clipped text, formula rendering, PDF/PPTX presence, and consistency with the markdown and notebook.
6. Stop for approval.
   Do not beautify or write the class script until the user approves the base deck, unless the user explicitly waives this boundary.
7. After approval, adapt or reuse the Week 3 redesign pipeline for AI polish.
8. After the final slide order is stable, write the instructor class script in English.

## Standard Commands

Inspect a week:

```bash
rg --files big_data_course_content | rg "week_0?<n>|week_<nn>"
```

Create a scaffold generator only:

```bash
python3 scripts/scaffold_week_presentation.py <n> --skip-build
```

Create a scaffold generator and first-pass exports:

```bash
python3 scripts/scaffold_week_presentation.py <n> --force
```

Build a real week deck once `scripts/generate_week_<n>_presentation.py` exists:

```bash
python3 scripts/generate_week_<n>_presentation.py
```

Validate the reusable scaffold layer:

```bash
python3 -m py_compile src/upc_datasets/weekly_presentation.py scripts/scaffold_week_presentation.py tests/test_weekly_presentation.py
```

## Approval Gate

The approval gate is mandatory unless the user explicitly removes it.

Before asking for approval, verify:

- the deck follows the week markdown and notebook rather than a generic outline
- formulas are rendered correctly and remain legible
- the PDF and PPTX both exist
- narrative devices, characters, and dialogs stay consistent with the course series
- slide count and order are stable enough for beautification

Only after approval:

- run or adapt the redesign pipeline
- produce the final class script from the approved slide flow

## Extension Rules

- Prefer extending `src/upc_datasets/weekly_presentation.py` when adding week-agnostic scaffolding behavior.
- Prefer extending the Week 3 redesign modules when adding shared AI beautification behavior.
- Keep `SKILL.md` concise. Put procedural detail in this runbook and reference it from the skill.
- Do not stage unrelated `.DS_Store`, notebook, or user-authored experimental files when committing skill or scaffold changes.
