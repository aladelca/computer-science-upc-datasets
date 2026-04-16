---
name: weekly-material-authoring
description: Create weekly course material for `big_data_course_content`. Use when asked to build or update a weekly presentation, weekly slides, a presentation generator, an AI-beautified deck, or a class script for a specific week. This includes reading the week markdown and notebook first, generating a deterministic base PDF/PPTX deck similar to `scripts/generate_week_3_presentation.py`, stopping for user approval before AI beautification, inspecting tracked or untracked redesign pipeline files under `src/upc_datasets/`, `big_data_course_content/presentations/`, `tests/`, and `plans/`, and then writing the final instructor class script in English from the approved slides. Also applies to requests like "material semanal", "presentacion de la semana", "weekly material", "lecture deck for week N", or "class script for this week".
---

# Weekly Material Authoring

Use this skill to create a full weekly teaching package for a course week in this repository.

For the file map, standard commands, and approval-gate checklist, read `references/weekly-material-runbook.md` when you need the operational details. Keep this `SKILL.md` focused on the core workflow.

The workflow is ordered and has an approval gate:

1. Read the week content.
2. Build the deterministic base presentation.
3. Stop and wait for approval.
4. After approval, beautify the slides with AI.
5. Based on the final slides, write the class script.

Do not skip the approval boundary unless the user explicitly tells you to.

## First-pass inspection

Before touching code, inspect the actual week assets and resolve the exact week slug from the repository:

- `big_data_course_content/week_XX_*.md`
- `big_data_course_content/notebooks/week_XX_*.ipynb`
- `big_data_course_content/presentations/`
- `big_data_course_content/README.md`
- `big_data_14_week_plan.md`
- any existing week presentation generator in `scripts/`

Also inspect the current worktree, because presentation beautification code may be untracked:

- run `git status --short`
- search `scripts/`, `src/`, `tests/`, `plans/`, and `big_data_course_content/presentations/` for `week_*_presentation`

When creating material for a new week, inspect the reusable week-agnostic scaffold first:

- `src/upc_datasets/weekly_presentation.py`
- `scripts/scaffold_week_presentation.py`

When beautification is part of the request, inspect these existing Week 3 pipeline files first if they exist, even if untracked:

- `scripts/generate_week_3_presentation.py`
- `src/upc_datasets/week_3_presentation_redesign.py`
- `src/upc_datasets/week_3_presentation_ai.py`
- `src/upc_datasets/week_3_presentation_openai.py`
- `src/upc_datasets/week_3_presentation_gemini.py`
- `big_data_course_content/presentations/week_3_redesign_profile.json`
- `.env.week3.example`
- `tests/test_generate_week_3_presentation.py`
- `tests/test_week_3_presentation_redesign.py`
- `plans/*week3*slide*redesign*`

Treat those files as the preferred starting point for the AI-polish stage. Adapt or generalize them; do not rebuild the same pipeline from scratch without a reason.

## Deliverables

Default deliverables for a week are:

- a week presentation generator script under `scripts/`
- a base presentation in `big_data_course_content/presentations/` as `.pdf`
- a matching flattened `.pptx`
- after approval, an AI-polished version or polished export path for the same deck
- an instructor class script saved beside the week content in `big_data_course_content/`

Preferred naming pattern:

- generator: `scripts/generate_week_<n>_presentation.py`
- presentation outputs: `big_data_course_content/presentations/week_<n>.pdf` and `.pptx`
- class script: `big_data_course_content/week_<n>_<topic>_class_script.md`

## Workflow

### 1. Read the week content first

Read the week markdown and notebook before designing any slides.

Extract:

- learning objectives
- theory blocks
- mathematical derivations
- dataset anchors
- examples and analogies
- notebook checkpoints that should become speaking cues

If the repo already has a narrative style for the course, preserve it. For this repo, that includes recurring characters and dialogue-based openings when the week series already uses them.

### 2. Create the deterministic base deck

Build the first version of the presentation without AI beautification.

Requirements:

- follow the actual week content, not a guessed outline
- keep the teaching order coherent with the markdown and notebook
- include mathematically correct formulas and notation
- prefer rendered formulas over ASCII approximations when working with image-based slides
- export both `.pdf` and `.pptx`

Use `scripts/generate_week_3_presentation.py` as the pattern when a similar generator is needed.

If the week does not yet have its own generator, use `scripts/scaffold_week_presentation.py` to create `scripts/generate_week_<n>_presentation.py` from the actual week markdown and notebook, then refine that scaffold into the real deck.

If a new week needs the same deck architecture, reuse and generalize that script instead of inventing a disconnected implementation.

### 3. Stop and wait for approval

After the base deck exists:

- render or inspect the slides
- check ordering, text fit, formulas, and output files
- present the result to the user
- explicitly stop for approval before beautification

Do not proceed to AI beautification or to the class script until the user approves the base deck, unless the user clearly waives the approval step.

### 4. Beautify with AI after approval

Only after approval, inspect and reuse the redesign pipeline if present.

Preferred approach in this repo:

- reuse the provider abstraction and redesign orchestration in `src/upc_datasets/week_3_presentation_redesign.py`
- reuse or adapt the image-edit adapters in:
  - `src/upc_datasets/week_3_presentation_openai.py`
  - `src/upc_datasets/week_3_presentation_gemini.py`
- reuse or adapt the style profile JSON under `big_data_course_content/presentations/`
- respect dry-run, cache, work-dir, and manifest behavior when available

Constraints for the AI-polish step:

- preserve all teaching meaning
- preserve chart geometry, formulas, and labels
- preserve readable text exactly where the pipeline supports it
- keep the deck structure and slide count stable unless the user asks for a content change

Use the local `.env.*.example` file if present to discover environment variables and provider selection.

### 5. Create the class script from the final slides

After the final slide flow is settled, create the class script in English.

The script should:

- follow the slide order
- deepen the theoretical concepts
- include mathematical verification and proof sketches where appropriate
- connect to the notebook and its empirical checkpoints
- include transitions, questions to ask students, and interpretation warnings
- end by linking the week to the next week in the course arc

Default tone:

- instructor-facing
- technically rigorous
- not casual lecture notes

## Validation

Before handing off:

- compile or run the presentation generator
- verify the expected output files exist
- inspect representative slides for layout, formulas, and clipping
- if a beautification pipeline was used, inspect the review artifacts or side-by-side outputs
- if tests exist for the presentation pipeline, run the relevant ones

At minimum, look for:

- broken formula rendering
- clipped callout boxes
- broken page order
- missing output files
- mismatch between slide content and class script

## Final handoff

In the final response, report:

- what was created or updated
- where the generator lives
- where the `.pdf` and `.pptx` live
- whether the approval gate was respected
- whether AI beautification was applied
- where the class script was saved

If approval has not yet been given, stop after the base deck and say so clearly.
