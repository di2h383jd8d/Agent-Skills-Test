# Agent Skills Test

A Python project for testing and developing [Claude Code](https://claude.ai/code) agent skills (slash commands).

## Overview

This repo serves as a workspace for building and experimenting with Claude Code skills — reusable slash commands that guide Claude through structured tasks. Skills live in `.claude/skills/` and are automatically available as `/skill-name` commands in any Claude Code session within this project.

## Requirements

- [Claude Code](https://claude.ai/code)
- [uv](https://docs.astral.sh/uv/) (Python package manager)

## Setup

```bash
uv sync   # Install dependencies
```

## Skills

### `/commit`
Stages all changes and creates a git commit with a message that summarizes the changes and names the files involved.

### `/doe` — Design of Experiments
Interactively guides you through creating an experiment design matrix. Collects factors, factor limits, design type, and responses, then generates a randomized run-order CSV and a markdown summary report in `outputs/`.

**Supported designs (v1):**

| Design | Description |
|--------|-------------|
| Full Factorial 2-level | 2^k runs — main effects and interactions |
| Full Factorial 3-level | 3^k runs — includes quadratic effects |
| CCD Circumscribed (CCC) | Rotatable; axial points outside factor limits |
| CCD Face-Centered (CCF) | Axial points at factor boundaries (alpha = 1) |
| CCD Inscribed (CCI) | Entire design within factor limits |

**Dependencies:** `pyDOE3`, `pandas`

## Directory Structure

```
.claude/skills/     # Claude Code skills (slash commands)
src/                # Project source code
outputs/            # Generated files (design matrices, reports, etc.)
```

## Backlog

Skills planned for future implementation:

| Skill | Description | Depends On |
|-------|-------------|------------|
| `/doe` v2 | Extend DOE skill with Box-Behnken, Plackett-Burman, and Latin Hypercube designs | `/doe` |
| `/refrigerant` | Refrigerant thermodynamic property lookups using CoolProp/REFPROP (temperature, pressure, enthalpy, entropy, quality, etc.) | — |
| `/psychro` | Psychrometric property calculations using CoolProp (humidity ratio, wet-bulb, dew point, enthalpy, relative humidity, etc.) | — |
| `/vcrs` | Vapor compression refrigeration cycle plotter — plots the cycle on P-h and T-s diagrams given operating conditions and refrigerant | `/refrigerant` |
| `/psychro-report` | Analyzes psychrometric lab reports — parses measured data, calculates derived properties, and flags anomalies | `/psychro` |

## Creating a New Skill

1. Create a directory under `.claude/skills/` named after the skill
2. Add a `SKILL.md` with YAML frontmatter:

```markdown
---
name: skill-name
description: Brief description of what the skill does.
---

Instructions for Claude to follow when this skill is invoked.
```

The skill is immediately available as `/skill-name` in Claude Code.
