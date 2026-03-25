# Central Composite Design — Inscribed (CCI)

## Overview

The Central Composite Inscribed (CCI) design is a scaled-down version of the CCC that fits entirely within the specified factor limits. Instead of extending the axial points outside the cube, the CCI uses the stated factor limits as the axial points and scales the factorial block **inward**.

In effect, the CCI takes a CCC and divides all coded coordinates by alpha so that what were the axial points (at +/-alpha) become the new +/-1 boundaries. The factorial cube therefore contracts to sit inside the axial sphere.

- **Axial points** sit exactly at the stated factor limits (+/-1 in natural units)
- **Factorial points** sit at +/-(1/alpha) in coded units — inside the factor limits
- Each factor requires **5 distinct levels**, but all within the stated range

## Run Count

```
Total runs = 2^k + 2k + n_center
```

Same run count as CCC and CCF.

With default center points (4 factorial + 4 axial):

| Factors (k) | Factorial | Axial | Center | Total |
|:-----------:|:---------:|:-----:|:------:|:-----:|
| 2 | 4 | 4 | 8 | 16 |
| 3 | 8 | 6 | 8 | 22 |
| 4 | 16 | 8 | 8 | 32 |
| 5 | 32 | 10 | 8 | 50 |

## Factorial Point Positions

The factorial points are located at +/-(1/alpha) in the original coded space. For a rotatable alpha:

| Factors (k) | alpha | Factorial points (coded) |
|:-----------:|:-----:|:------------------------:|
| 2 | 1.414 | +/- 0.707 |
| 3 | 1.682 | +/- 0.595 |
| 4 | 2.000 | +/- 0.500 |
| 5 | 2.378 | +/- 0.421 |

These are interior points — the corners of the design do not reach the stated factor limits.

## Rotatability

The CCI is **rotatable** (it is geometrically equivalent to a CCC, just scaled). Prediction variance is uniform at all points equidistant from the center.

## What It Estimates

Like all CCD variants, the CCI fits a full second-order response surface model:

```
y = b0 + sum(bi*xi) + sum(bii*xi^2) + sum(bij*xi*xj) + error
```

## When to Use

- Response surface modeling where factor limits are **absolute hard limits** that cannot be exceeded under any circumstances
- When the entire experimental region must lie within a predefined safe operating envelope
- When rotatability is desired but factor limits are non-negotiable

## When NOT to Use

- When the factor range midpoint is not physically accessible — the CCI places many runs in the interior of the range, which may not be informative if the interesting behavior is near the limits
- When 3-level simplicity is acceptable — CCF is simpler and more commonly used
- When the full factor limits themselves need to be tested — CCI never tests the corner combinations at full factor limits

## Comparison of CCD Variants

| Property | CCC | CCF | CCI |
|----------|-----|-----|-----|
| Axial points | Outside limits | At limits | At limits |
| Factorial points | At limits (+/-1) | At limits (+/-1) | Inside limits (+/-1/alpha) |
| Levels per factor | 5 | 3 | 5 |
| Rotatable | Yes | No | Yes |
| Stays within limits | No | Yes | Yes |
| Corner points tested at full limits | Yes | Yes | No |

## Key Parameters in /doe

| Parameter | Default | Notes |
|-----------|---------|-------|
| `center_points_factorial` | 4 | Center runs in the factorial block |
| `center_points_axial` | 4 | Center runs in the axial block |
| alpha | Computed (rotatable) | Same formula as CCC: `(2^k)^0.25` |
