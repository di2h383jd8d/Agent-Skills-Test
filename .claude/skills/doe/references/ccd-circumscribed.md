# Central Composite Design — Circumscribed (CCC)

## Overview

The Central Composite Circumscribed (CCC) design is the original form of the CCD. It consists of three parts:

1. **Factorial block**: A 2^k full factorial (or resolution V fractional factorial) — the corner points of the hypercube
2. **Axial (star) points**: 2k points along each factor axis at distance alpha from the center
3. **Center points**: Replicate runs at the center of the design space

The axial distance alpha > 1 means the **axial points extend beyond the factorial cube**, requiring 5 distinct levels per factor: `-alpha, -1, 0, +1, +alpha`.

## Run Count

```
Total runs = 2^k + 2k + n_center
```

With default center points (4 factorial + 4 axial):

| Factors (k) | Factorial | Axial | Center | Total |
|:-----------:|:---------:|:-----:|:------:|:-----:|
| 2 | 4 | 4 | 8 | 16 |
| 3 | 8 | 6 | 8 | 22 |
| 4 | 16 | 8 | 8 | 32 |
| 5 | 32 | 10 | 8 | 50 |

## Axial Distance (alpha)

For a rotatable CCC, alpha is determined by:

```
alpha = (2^k)^0.25 = k^0.25  [for full factorial block]
```

| Factors (k) | alpha (rotatable) |
|:-----------:|:-----------------:|
| 2 | 1.414 |
| 3 | 1.682 |
| 4 | 2.000 |
| 5 | 2.378 |

These axial points lie **outside the original factor limits** specified by the user. Before using CCC, confirm that running experiments at these extended conditions is physically feasible and safe.

## Rotatability

The CCC with the rotatable alpha is a **rotatable design**: the prediction variance depends only on the distance from the center, not the direction. This means the model is equally reliable in all directions from the center, which is ideal for exploring an unknown response surface.

## What It Estimates

The CCC supports fitting a full second-order response surface model:

```
y = b0 + sum(bi*xi) + sum(bii*xi^2) + sum(bij*xi*xj) + error
```

This includes all main effects (linear), pure quadratic effects, and two-factor interactions.

## When to Use

- Response surface modeling and optimization
- When rotatability and uniform prediction variance are important
- When the experiment can be run outside the original factor limits (axial points)
- When augmenting an existing 2-level factorial with axial points

## When NOT to Use

- When factor limits are strict and cannot be exceeded — use CCF or CCI instead
- When the extended axial conditions are dangerous or physically impossible

## Key Parameters in /doe

| Parameter | Default | Notes |
|-----------|---------|-------|
| `center_points_factorial` | 4 | Center runs in the factorial block |
| `center_points_axial` | 4 | Center runs in the axial block |
| `alpha` | rotatable | Computed as `(2^k)^0.25`; can be overridden |

## Relationship to Other CCDs

```
CCC: alpha > 1  →  axial points outside factor limits  →  5 levels per factor
CCF: alpha = 1  →  axial points at factor boundaries   →  3 levels per factor
CCI: alpha < 1  →  factorial points scaled inward      →  5 levels per factor (within limits)
```
