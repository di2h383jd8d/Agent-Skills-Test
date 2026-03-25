#!/usr/bin/env python3
"""
DOE Generation Script - v1
Supports: Full Factorial (2-level, 3-level) and Central Composite Design (CCD)

Usage:
    uv run python .claude/skills/doe/scripts/generate_doe.py <config.json>
"""

import json
import math
import os
import sys
from datetime import datetime
from itertools import product

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Design generation
# ---------------------------------------------------------------------------

def generate_design(config):
    design_type = config["design_type"]
    k = len(config["factors"])
    ff_opts = config.get("ff_options", {})
    ccd_opts = config.get("ccd_options", {})

    if design_type == "ff_2level":
        from pyDOE3 import ff2n
        coded = ff2n(k).astype(float)
        n_center = ff_opts.get("center_points", 0)
        if n_center > 0:
            coded = np.vstack([coded, np.zeros((n_center, k))])
        replicates = ff_opts.get("replicates", 1)
        if replicates > 1:
            coded = np.vstack([coded] * replicates)

    elif design_type == "ff_3level":
        coded = np.array(list(product([-1.0, 0.0, 1.0], repeat=k)))
        replicates = ff_opts.get("replicates", 1)
        if replicates > 1:
            coded = np.vstack([coded] * replicates)

    elif design_type in ("ccd_circumscribed", "ccd_facecentered", "ccd_inscribed"):
        from pyDOE3 import ccdesign
        face_map = {
            "ccd_circumscribed": "ccc",
            "ccd_facecentered": "ccf",
            "ccd_inscribed":    "cci",
        }
        cp_factorial = ccd_opts.get("center_points_factorial", 4)
        cp_axial     = ccd_opts.get("center_points_axial", 4)
        alpha        = "rotatable" if design_type == "ccd_circumscribed" else "orthogonal"
        coded = ccdesign(k, center=(cp_factorial, cp_axial), alpha=alpha,
                         face=face_map[design_type]).astype(float)

    else:
        raise ValueError(f"Unknown design_type: {design_type!r}")

    return coded


# ---------------------------------------------------------------------------
# Unit conversion
# ---------------------------------------------------------------------------

def coded_to_natural(val, low, high):
    """Map coded value in [-1, 1] to natural units [low, high]."""
    return low + (val + 1) / 2 * (high - low)


# ---------------------------------------------------------------------------
# DataFrame assembly
# ---------------------------------------------------------------------------

def build_dataframe(coded, config):
    factors   = config["factors"]
    responses = config["responses"]
    randomize = config.get("randomize", True)
    seed      = config.get("random_seed", None)

    nat_cols   = {f["name"]: [] for f in factors}
    coded_cols = {f"{f['name']} (coded)": [] for f in factors}

    for run in coded:
        for i, factor in enumerate(factors):
            nat_cols[factor["name"]].append(
                round(coded_to_natural(run[i], factor["low"], factor["high"]), 4)
            )
            coded_cols[f"{factor['name']} (coded)"].append(round(float(run[i]), 4))

    df = pd.DataFrame({**nat_cols, **coded_cols})

    for resp in responses:
        df[resp["name"]] = ""

    if randomize:
        rng = np.random.default_rng(seed)
        df = df.iloc[rng.permutation(len(df))].reset_index(drop=True)

    df.insert(0, "Run", range(1, len(df) + 1))
    return df


# ---------------------------------------------------------------------------
# Summary document
# ---------------------------------------------------------------------------

DESIGN_LABELS = {
    "ff_2level":          "Full Factorial - 2-level (2^k)",
    "ff_3level":          "Full Factorial - 3-level (3^k)",
    "ccd_circumscribed":  "Central Composite Design - Circumscribed (CCC)",
    "ccd_facecentered":   "Central Composite Design - Face-Centered (CCF)",
    "ccd_inscribed":      "Central Composite Design - Inscribed (CCI)",
}

DESIGN_NOTES = {
    "ff_2level":
        "Estimates all main effects and interaction effects. "
        "Add center points to check for curvature.",
    "ff_3level":
        "Estimates main effects, two-factor interactions, and pure quadratic effects.",
    "ccd_circumscribed":
        "Rotatable design. Axial points (alpha > 1) fall outside the factorial cube - "
        "verify these settings are experimentally feasible.",
    "ccd_facecentered":
        "Axial points sit on the faces of the factorial cube (alpha = 1). "
        "All points are within factor limits. Not rotatable.",
    "ccd_inscribed":
        "Entire design fits within factor limits. "
        "The factorial cube is scaled inward to accommodate the axial distance.",
}


def _md_table(headers, rows):
    col_w = [max(len(str(h)), max((len(str(r[i])) for r in rows), default=0))
             for i, h in enumerate(headers)]
    fmt_row = lambda cells: "| " + " | ".join(str(c).ljust(w) for c, w in zip(cells, col_w)) + " |"
    sep = "|" + "|".join("-" * (w + 2) for w in col_w) + "|"
    return "\n".join([fmt_row(headers), sep] + [fmt_row(r) for r in rows])


def build_summary(config, df, coded):
    factors     = config["factors"]
    responses   = config["responses"]
    design_type = config["design_type"]
    now         = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Axial distance (CCD only)
    alpha_str = ""
    if "ccd" in design_type:
        alpha_val = round(float(np.abs(coded).max()), 4)
        alpha_str = f"\n**Axial distance (alpha):** {alpha_val}  "

    # Factor table
    factor_table = _md_table(
        ["Factor", "Units", "Low (-1)", "Center (0)", "High (+1)"],
        [
            [
                f["name"],
                f.get("units", "-"),
                f["low"],
                round((f["low"] + f["high"]) / 2, 4),
                f["high"],
            ]
            for f in factors
        ],
    )

    # Response table
    resp_table = _md_table(
        ["Response", "Units"],
        [[r["name"], r.get("units", "-")] for r in responses],
    )

    # Design preview (first 8 runs, natural + response cols only)
    preview_cols = ["Run"] + [f["name"] for f in factors] + [r["name"] for r in responses]
    preview_df   = df[preview_cols].head(8)
    preview_rows = [list(row) for _, row in preview_df.iterrows()]
    preview_table = _md_table(list(preview_df.columns), preview_rows)

    lines = [
        f"# DOE Summary: {config['name']}",
        f"",
        f"**Generated:** {now}  ",
        f"**Design:** {DESIGN_LABELS.get(design_type, design_type)}  ",
        f"**Factors:** {len(factors)}  ",
        f"**Responses:** {len(responses)}  ",
        f"**Total runs:** {len(df)}  ",
        alpha_str,
        f"",
        f"> {DESIGN_NOTES.get(design_type, '')}",
        f"",
        f"## Factors",
        f"",
        factor_table,
        f"",
        f"## Responses",
        f"",
        resp_table,
        f"",
        f"## Design Preview (first 8 runs, natural units)",
        f"",
        preview_table,
        f"",
        f"_Full randomized design (with coded columns) saved to CSV._",
    ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: uv run python generate_doe.py <config.json>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        config = json.load(f)

    output_dir = config.get("output_dir", "outputs")
    os.makedirs(output_dir, exist_ok=True)

    slug = config["name"].strip().lower().replace(" ", "_")

    coded   = generate_design(config)
    df      = build_dataframe(coded, config)
    summary = build_summary(config, df, coded)

    csv_path     = os.path.join(output_dir, f"{slug}_design.csv")
    summary_path = os.path.join(output_dir, f"{slug}_summary.md")
    config_path  = os.path.join(output_dir, f"{slug}_config.json")

    df.to_csv(csv_path, index=False)

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)

    # Re-save config alongside outputs for reproducibility
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    result = {
        "runs":            len(df),
        "csv":             csv_path,
        "summary":         summary_path,
        "config":          config_path,
        "summary_content": summary,
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()
