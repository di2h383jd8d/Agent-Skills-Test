# DOE Skill Reference

A reference guide for the `/doe` skill. Read this file for an overview of Design of Experiments concepts and implemented designs. For detailed theory on a specific design, refer to the individual files linked below.

---

## What is Design of Experiments?

Design of Experiments (DOE) is a systematic method for planning experiments to efficiently study the relationship between multiple input variables (factors) and measured outputs (responses). Rather than varying one factor at a time, DOE varies all factors simultaneously in a structured way, which:

- Reveals interactions between factors that one-at-a-time testing cannot detect
- Achieves more information per experimental run
- Supports development of empirical models (response surface models) for optimization
- Provides statistical estimates of measurement error through replication

---

## Implemented Designs (v1)

| Design | File | Best For |
|--------|------|----------|
| Full Factorial 2-level | [ff-2level.md](ff-2level.md) | Screening; estimating main effects and all interactions |
| Full Factorial 3-level | [ff-3level.md](ff-3level.md) | Estimating quadratic effects with small k |
| CCD Circumscribed (CCC) | [ccd-circumscribed.md](ccd-circumscribed.md) | Response surface modeling with rotatability |
| CCD Face-Centered (CCF) | [ccd-facecentered.md](ccd-facecentered.md) | Response surface modeling within strict factor limits |
| CCD Inscribed (CCI) | [ccd-inscribed.md](ccd-inscribed.md) | Response surface modeling within absolute factor limits |

---

## Key Concepts

### Factors and Levels

A **factor** is a controlled input variable (e.g., temperature, pressure, flow rate). A **level** is a specific setting of a factor within the experiment. In DOE, factors are typically set at a low level and a high level (and sometimes a center).

### Coded Units

Factors are mapped to a standardized **coded** scale:

- Low level → **-1**
- Center → **0**
- High level → **+1**

Coded units simplify calculations and allow fair comparison of effect sizes across factors with different physical scales. The `/doe` skill outputs both natural units (for lab use) and coded units (for analysis).

### Responses

A **response** is a measured outcome of interest (e.g., yield, purity, reaction rate). Responses are not set by the experimenter — they are measured after each run.

### Randomization

**Randomization** means running experiments in a random order rather than a systematic one. This protects against bias from time-dependent effects (equipment drift, operator fatigue, environmental changes). The `/doe` skill randomizes run order by default. Technicians should follow the randomized order exactly.

### Replication

**Replication** is running the same experimental conditions more than once. True replication (separate runs at the same conditions) provides an independent estimate of experimental error. This is different from repeated measurements of the same run.

### Center Points

**Center points** are runs at the midpoint of all factor ranges (coded value 0 for all factors). They serve two purposes:

1. **Pure error estimation** — repeated center point runs provide an estimate of experimental variability
2. **Curvature detection** — if the average response at center points differs significantly from the average predicted by a linear model, curvature (quadratic effects) is present

Center points are critical for 2-level full factorial designs, which cannot otherwise detect curvature.

### Blocking

**Blocking** groups runs that share a common source of nuisance variation (e.g., different days, operators, or batches of raw material). By explicitly accounting for block-to-block differences, blocking prevents nuisance variation from inflating the experimental error. The `/doe` v1 skill does not yet implement blocking — it is planned for a future version.

### Main Effects

A **main effect** is the average change in the response caused by moving a single factor from its low level to its high level, averaged across all levels of other factors.

### Interaction Effects

An **interaction effect** occurs when the effect of one factor on the response depends on the level of another factor. Two-factor interactions (2FI) are the most common. They are only estimable when all combinations of factor levels are included in the design (or via designed aliasing in fractional factorials).

### Aliasing (Confounding)

In fractional factorial designs (not yet implemented in v1), some effects are **aliased** (confounded) — meaning they cannot be independently estimated. The alias structure must be understood before interpreting results. Full factorial designs have no aliasing.

### Rotatability

A design is **rotatable** if the prediction variance is constant at all points equidistant from the design center. Rotatable designs are desirable for response surface exploration because the uncertainty in the model is the same in all directions from the center. The CCC design achieves rotatability; CCF and CCI do not.

### Axial Distance (alpha)

In CCD designs, **alpha** is the distance from the center to the axial (star) points in coded units. It determines the geometry of the CCD:

- **CCC**: alpha > 1, calculated for rotatability as `alpha = k^0.25`
- **CCF**: alpha = 1 (axial points at factor boundaries)
- **CCI**: alpha = 1 in natural units (the design is scaled inward)

### Response Surface Methodology (RSM)

**RSM** is a collection of techniques for building empirical polynomial models relating factors to responses, typically used to find optimal operating conditions. CCD designs are specifically tailored for RSM — they support fitting a full second-order (quadratic) model including all main effects, two-factor interactions, and pure quadratic terms.

The general second-order model for k factors:

```
y = b0 + sum(bi*xi) + sum(bii*xi^2) + sum(bij*xi*xj) + error
```

where `xi` are the coded factor values.

---

## Choosing a Design

```
Do you need to fit a quadratic model (response surface)?
├── No  → Use Full Factorial 2-level (add center points to check for curvature)
└── Yes → Use CCD
           ├── Can axial points exceed factor limits?
           │    └── Yes → CCC (rotatable, best prediction properties)
           └── No  → Must stay strictly within limits?
                     ├── Boundaries are soft → CCF (simpler, 3-level per factor)
                     └── Boundaries are hard → CCI (entire design within limits)

Is k large (> 4) and you only need to screen for important factors?
└── Consider Fractional Factorial or Plackett-Burman (planned for v2)
```
