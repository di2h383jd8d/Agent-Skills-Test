---
name: doe
description: Interactively create a Design of Experiments (DOE) matrix. Supports Full Factorial (2-level, 3-level) and Central Composite Design (CCC, CCF, CCI). Outputs a randomized run-order CSV and a summary report to outputs/.
---

Guide the user through designing an experiment step by step. At the end, generate the design matrix and save outputs.

---

## Supported Designs (v1)

| Code               | Design                                  |
|--------------------|-----------------------------------------|
| `ff_2level`        | Full Factorial – 2-level (2^k)          |
| `ff_3level`        | Full Factorial – 3-level (3^k)          |
| `ccd_circumscribed`| CCD – Circumscribed (CCC), rotatable    |
| `ccd_facecentered` | CCD – Face-Centered (CCF), α = 1        |
| `ccd_inscribed`    | CCD – Inscribed (CCI), within limits    |

---

## Conversation Flow

Work through these steps in order. Ask one section at a time — do not dump all questions at once.

### Step 1 — Experiment Metadata

Ask for:
- **Experiment name** (used as the output filename slug)
- **Brief description** (optional)

### Step 2 — Factors

Collect factors one at a time. For each factor ask:
- Name
- Units
- Low level (natural units)
- High level (natural units)

After each factor ask "Any more factors?" until the user is done. Require at least 2 factors.

### Step 3 — Design Type

Present the options clearly. Advise on run counts before the user chooses:

- 2-level FF: **2^k** factorial runs (e.g., 3 factors → 8 runs)
- 3-level FF: **3^k** runs — warn if k > 3 (e.g., 4 factors → 81 runs, likely impractical)
- CCD (any): **2^k + 2k + center points** runs (e.g., 3 factors + defaults → ~20 runs)

Guidance to offer:
- Use **2-level FF** for studying main effects and interactions, especially for screening
- Use **3-level FF** only for small k (≤ 3) when quadratic terms matter and run count is acceptable
- Use **CCC** when you need rotatability and axial points outside factor limits are acceptable
- Use **CCF** when you cannot exceed factor limits (most common lab scenario)
- Use **CCI** when the factor limits are absolute hard boundaries and the design must stay entirely within them

### Step 4 — Design-Specific Options

**Full Factorial (2-level):**
- Center point replicates (default: 3) — used to estimate pure error and detect curvature
- Full design replication count (default: 1)

**Full Factorial (3-level):**
- Full design replication count (default: 1)
- (Center is already included as the 0-level; no additional center points needed)

**CCD (any type):**
- Center points in the factorial block (default: 4)
- Center points in the axial block (default: 4)
- For CCC: inform the user that axial points will exceed their stated factor limits. Show the rotatable alpha value (α = k^0.25) and ask if that is acceptable. If not, suggest CCF.
- For CCF: confirm that α = 1 means axial points sit exactly at the factor boundaries.
- For CCI: confirm that the factorial cube is scaled inward and the factor limits become the axial points.

### Step 5 — Responses

Ask for the measured responses. For each:
- Name
- Units

Continue until the user is done.

### Step 6 — Confirm

Show a confirmation table before generating:

```
Experiment:  <name>
Design:      <design label>
Factors:     <k>
Responses:   <n>
Est. runs:   <n>

Factors:
  - <Name> (<units>): <low> to <high>
  ...

Responses:
  - <Name> (<units>)
  ...
```

Ask: "Does this look correct? Generate the design?"

### Step 7 — Generate

Once confirmed:

1. Build the config JSON (schema below).
2. Write it to a temp file: `outputs/<slug>_config.json`
3. Run the script:
   ```bash
   uv run python .claude/skills/doe/scripts/generate_doe.py outputs/<slug>_config.json
   ```
4. Parse the JSON output from the script.
5. Display the `summary_content` field to the user.
6. Report the output file paths (`csv` and `summary`).

---

## Config JSON Schema

```json
{
  "name": "Experiment Name",
  "description": "Optional description",
  "design_type": "ff_2level | ff_3level | ccd_circumscribed | ccd_facecentered | ccd_inscribed",
  "factors": [
    { "name": "Factor Name", "units": "unit", "low": 0, "high": 100 }
  ],
  "ff_options": {
    "center_points": 3,
    "replicates": 1
  },
  "ccd_options": {
    "center_points_factorial": 4,
    "center_points_axial": 4
  },
  "responses": [
    { "name": "Response Name", "units": "unit" }
  ],
  "randomize": true,
  "output_dir": "outputs"
}
```

Only include `ff_options` for FF designs and `ccd_options` for CCD designs.

---

## Important Rules

- Always run Python via `uv run python`, never bare `python`.
- Output files always go to `outputs/`.
- The generated CSV contains both natural-unit columns (for the technician) and coded columns (suffixed ` (coded)`) for analysis.
- Run order is randomized by default — remind the user to follow the randomized order in the lab.
- The config JSON is saved alongside the outputs for full reproducibility.
