# Central Composite Design — Face-Centered (CCF)

## Overview

The Central Composite Face-Centered (CCF) design is a variant of the CCD where the axial (star) points are placed at the **center of each face of the factorial cube** rather than outside it. This means:

- **alpha = 1** for all factors
- Axial points sit exactly at the factor limits (the +1 and -1 boundaries)
- Each factor requires only **3 distinct levels**: -1, 0, +1
- The design stays entirely **within the specified factor limits**

## Run Count

```
Total runs = 2^k + 2k + n_center
```

Identical run count to CCC — the only difference is the position of the axial points.

With default center points (4 factorial + 4 axial):

| Factors (k) | Factorial | Axial | Center | Total |
|:-----------:|:---------:|:-----:|:------:|:-----:|
| 2 | 4 | 4 | 8 | 16 |
| 3 | 8 | 6 | 8 | 22 |
| 4 | 16 | 8 | 8 | 32 |
| 5 | 32 | 10 | 8 | 50 |

## Rotatability

The CCF is **not rotatable**. Because alpha = 1, the axial points coincide with the edges of the factorial cube rather than lying on a sphere. Prediction variance is not uniform in all directions. In practice, the loss of rotatability is often an acceptable trade-off for the benefit of staying within factor limits.

## What It Estimates

Like all CCD variants, the CCF supports fitting a full second-order response surface model:

```
y = b0 + sum(bi*xi) + sum(bii*xi^2) + sum(bij*xi*xj) + error
```

However, because each factor only appears at 3 levels, the pure quadratic coefficients (bii) are estimated less precisely than in the CCC.

## When to Use

- Response surface modeling and optimization
- When factor limits are strict and cannot be exceeded (safety limits, equipment constraints, regulatory limits)
- Most common CCD choice for laboratory experiments where extrapolation beyond tested limits is undesirable
- When 3 levels per factor is preferred for simplicity in lab setup

## When NOT to Use

- When rotatability is required — use CCC instead
- When factor limits are hard absolute boundaries with no tolerance — use CCI instead
- When the factor space is so constrained that even face-centered points are at the very edge of feasibility

## Comparison with CCC

| Property | CCC | CCF |
|----------|-----|-----|
| alpha | > 1 (e.g. 1.68 for k=3) | = 1 |
| Axial point location | Outside factor limits | At factor boundaries |
| Levels per factor | 5 | 3 |
| Rotatable | Yes | No |
| Exceeds factor limits | Yes | No |

## Key Parameters in /doe

| Parameter | Default | Notes |
|-----------|---------|-------|
| `center_points_factorial` | 4 | Center runs in the factorial block |
| `center_points_axial` | 4 | Center runs in the axial block |
| alpha | Fixed at 1 | Cannot be changed for CCF |
