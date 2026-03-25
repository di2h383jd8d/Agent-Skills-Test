# Full Factorial Design — 3-Level (3^k)

## Overview

A 3-level full factorial design tests all possible combinations of k factors, each at three levels (low = -1, center = 0, high = +1). With k factors the design produces **3^k** runs.

| Factors (k) | Runs |
|:-----------:|:----:|
| 2 | 9 |
| 3 | 27 |
| 4 | 81 |
| 5 | 243 |

Run count grows very rapidly. This design is generally only practical for k <= 3. For k >= 4 with a need for quadratic terms, use a CCD instead.

## What It Estimates

A 3-level full factorial supports fitting a full second-order model including:

- All main effects (linear and quadratic)
- All two-factor interactions (linear x linear)

The second-order model for k = 2:

```
y = b0 + b1*x1 + b2*x2 + b11*x1^2 + b22*x2^2 + b12*x1*x2 + error
```

Unlike a 2-level FF, the 3-level FF can independently estimate pure quadratic effects because each factor appears at three levels. However, CCD designs are generally preferred for RSM because they achieve similar estimation with fewer runs.

## Center Points

The center (0-level) is built into the design — every combination of levels including the center is included. No additional center point replicates are needed to estimate curvature. Additional replicates of specific runs may still be added to estimate pure error.

## When to Use

- k = 2 or k = 3 and a full quadratic model is needed
- When the experimental region is a cube and all interior points are of interest
- When a simple, fully symmetric design is preferred over a CCD

## When NOT to Use

- k >= 4 — run count becomes prohibitive (81+ runs); use CCD instead
- When only main effects and interactions are needed — use 2-level FF instead
- When the factor space is not well-defined at the center — use CCD with explicit center point control

## Comparison with CCD

| Property | 3-level FF | CCD (CCF) |
|----------|-----------|-----------|
| Runs (k=3) | 27 | ~20 |
| Quadratic terms | Yes | Yes |
| Rotatability | No | Partial (CCF) |
| Flexibility | Low | High |

For most RSM applications, a CCD is preferred over a 3-level FF due to the lower run count.

## Key Parameters in /doe

| Parameter | Default | Notes |
|-----------|---------|-------|
| `replicates` | 1 | Full replication of the design |
