# Full Factorial Design — 2-Level (2^k)

## Overview

A 2-level full factorial design tests all possible combinations of k factors, each at two levels (low = -1, high = +1). With k factors the design produces **2^k** runs (plus any center points or replicates).

| Factors (k) | Factorial runs | + 3 center points |
|:-----------:|:--------------:|:-----------------:|
| 2 | 4 | 7 |
| 3 | 8 | 11 |
| 4 | 16 | 19 |
| 5 | 32 | 35 |
| 6 | 64 | 67 |

Run count grows exponentially. For k > 5, consider a fractional factorial instead.

## What It Estimates

A 2-level full factorial estimates all **main effects** and all **interaction effects** (2FI, 3FI, up to k-FI) without aliasing. It does **not** estimate pure quadratic (curvature) effects from factorial points alone — center points are required to detect curvature.

The linear model fitted to a 2-level FF (without center points) is:

```
y = b0 + b1*x1 + b2*x2 + ... + b12*x1*x2 + b13*x1*x3 + ... + error
```

## Center Points

Adding center point replicates (all factors at coded 0) to a 2-level FF serves two purposes:

1. **Curvature detection**: A significant difference between the mean response at center points and the mean predicted by the linear model indicates that at least one factor has a quadratic effect.
2. **Pure error**: Repeated center point runs provide an estimate of experimental variability independent of model assumptions.

Typical recommendation: 3–5 center point replicates.

If curvature is detected and a quadratic model is needed, augment the design with axial points to form a CCD (circumscribed or face-centered).

## When to Use

- Screening: identifying which factors among many have significant effects
- Full characterization of a small factor set (k <= 5) including all interactions
- First experiment in a sequential strategy before RSM

## When NOT to Use

- When a quadratic model is needed from the start — use CCD instead
- When k > 5 and run count is prohibitive — use fractional factorial (v2)

## Design Matrix Example (k = 2)

| Run | x1 | x2 |
|-----|----|----|
| 1 | -1 | -1 |
| 2 | +1 | -1 |
| 3 | -1 | +1 |
| 4 | +1 | +1 |

Run order is randomized in practice.

## Key Parameters in /doe

| Parameter | Default | Notes |
|-----------|---------|-------|
| `center_points` | 3 | Number of center point replicates |
| `replicates` | 1 | Full replication of the factorial portion |
