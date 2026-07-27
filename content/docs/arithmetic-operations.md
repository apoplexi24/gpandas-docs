---
title: "Arithmetic & Comparison"
description: "Element-wise arithmetic and comparison across DataFrame columns and scalars"
icon: "calculate"
weight: 38
---

Learn how to perform element-wise arithmetic and comparisons in GPandas. Column-column methods combine two columns, scalar methods apply a constant to a column, and comparison methods produce boolean columns. Every method returns a standalone `Series` that you attach with `Assign`; the DataFrame is never mutated.

<!-- IMAGE_PLACEHOLDER: Visual showing two columns combined element-wise into a result column -->

&nbsp;

## Overview

| Category | Methods | Result |
|----------|---------|--------|
| Column arithmetic | `Add()`, `Sub()`, `Mul()`, `Div()`, `Pow()` | Numeric Series |
| Scalar arithmetic | `AddScalar()`, `SubScalar()`, `MulScalar()`, `DivScalar()`, `PowScalar()` | Numeric Series |
| Column comparison | `Gt()`, `Lt()`, `Ge()`, `Le()`, `Eq()`, `Ne()` | Boolean Series |
| Scalar comparison | `GtScalar()`, `LtScalar()`, `GeScalar()`, `LeScalar()`, `EqScalar()`, `NeScalar()` | Boolean Series |

Each method returns a `collection.Series` (plus an `error`). Because the result is a standalone Series, combine it with [`Assign`]({{< ref "adding-columns" >}}) to attach it as a new column:

```go
sum, err := df.Add("Q1", "Q2")
if err != nil {
    log.Fatal(err)
}
_ = df.Assign("TotalUnits", sum)
```

&nbsp;

---

&nbsp;

## Type Promotion

Arithmetic results follow pandas-like promotion rules:

| Operation | Operands | Result type |
|-----------|----------|-------------|
| `Add` / `Sub` / `Mul` | both integer | `int64` |
| `Add` / `Sub` / `Mul` | any float involved | `float64` |
| `Div` | any numeric | `float64` (always) |
| `Pow` | any numeric | `float64` (always) |

For the scalar variants, an integer column stays `int64` only when the operation is `Add`/`Sub`/`Mul` **and** the scalar is a whole number; otherwise the result is promoted to `float64`.

**Division and powers** always yield `float64`. Division by zero produces `+Inf`, `-Inf`, or `NaN` rather than an error, matching IEEE-754 float semantics.

&nbsp;

---

&nbsp;

## Null Handling

A null in either operand yields a null in that position of the result. Comparisons behave the same way: comparing against a null produces a null (not `false`).

&nbsp;

---

&nbsp;

## Sample Data

All arithmetic examples use this product DataFrame:

### Products DataFrame

| Product | Q1 | Q2 | Price |
|---------|----|----|-------|
| Widget | 100 | 150 | 9.99 |
| Gadget | 80 | 90 | 14.50 |
| Gizmo | 120 | 110 | 7.25 |
| Doohickey | 60 | 75 | 19.00 |

&nbsp;

### Setup Code

```go
package main

import (
    "fmt"
    "log"

    "github.com/apoplexi24/gpandas"
)

func main() {
    gp := gpandas.GoPandas{}

    df, err := gp.DataFrame(
        []string{"Product", "Q1", "Q2", "Price"},
        []gpandas.Column{
            {"Widget", "Gadget", "Gizmo", "Doohickey"},
            {int64(100), int64(80), int64(120), int64(60)},
            {int64(150), int64(90), int64(110), int64(75)},
            {9.99, 14.50, 7.25, 19.00},
        },
        map[string]any{
            "Product": gpandas.StringCol{},
            "Q1":      gpandas.IntCol{},
            "Q2":      gpandas.IntCol{},
            "Price":   gpandas.FloatCol{},
        },
    )
    if err != nil {
        log.Fatalf("Failed to create DataFrame: %v", err)
    }

    // Examples follow...
}
```

&nbsp;

---

&nbsp;

## Column-Column Arithmetic

Combine two numeric columns element-wise.

&nbsp;

### Function Signatures

```go
func (df *DataFrame) Add(left, right string) (collection.Series, error)
func (df *DataFrame) Sub(left, right string) (collection.Series, error)
func (df *DataFrame) Mul(left, right string) (collection.Series, error)
func (df *DataFrame) Div(left, right string) (collection.Series, error)
func (df *DataFrame) Pow(left, right string) (collection.Series, error)
```

&nbsp;

### Example

`Q1 + Q2` stays `int64` (both operands are integers); `Q2 - Q1` gives per-quarter growth:

```go
total, _ := df.Add("Q1", "Q2")
_ = df.Assign("TotalUnits", total)

growth, _ := df.Sub("Q2", "Q1")
_ = df.Assign("Growth", growth)

fmt.Println(df.String())
```

&nbsp;

### Output

```
+-----------+-----+-----+-------+------------+--------+
| Product   | Q1  | Q2  | Price | TotalUnits | Growth |
+-----------+-----+-----+-------+------------+--------+
| Widget    | 100 | 150 | 9.99  | 250        | 50     |
| Gadget    | 80  | 90  | 14.5  | 170        | 10     |
| Gizmo     | 120 | 110 | 7.25  | 230        | -10    |
| Doohickey | 60  | 75  | 19    | 135        | 15     |
+-----------+-----+-----+-------+------------+--------+
[4 rows x 6 columns]
```

&nbsp;

### Mixed Types Promote to Float

Multiplying the integer `TotalUnits` by the float `Price` promotes the result to `float64`:

```go
revenue, _ := df.Mul("TotalUnits", "Price")
_ = df.Assign("Revenue", revenue)
```

`Revenue` becomes `2497.5`, `2465`, `1667.5`, `2565`.

&nbsp;

---

&nbsp;

## Scalar Arithmetic

Apply a `float64` constant to every value of a numeric column.

&nbsp;

### Function Signatures

```go
func (df *DataFrame) AddScalar(column string, scalar float64) (collection.Series, error)
func (df *DataFrame) SubScalar(column string, scalar float64) (collection.Series, error)
func (df *DataFrame) MulScalar(column string, scalar float64) (collection.Series, error)
func (df *DataFrame) DivScalar(column string, scalar float64) (collection.Series, error)
func (df *DataFrame) PowScalar(column string, scalar float64) (collection.Series, error)
```

&nbsp;

### Example

Apply a 10% discount to `Price`:

```go
discounted, _ := df.MulScalar("Price", 0.90)
_ = df.Assign("DiscountPrice", discounted)
```

`DiscountPrice` becomes `8.991`, `13.05`, `6.525`, `17.1`. Because the scalar is fractional, the result is `float64` even where the source column is integer-typed.

&nbsp;

---

&nbsp;

## Comparisons

Comparison methods return a boolean Series, ideal for building masks or flag columns. Column-column comparisons require both columns to be numeric or both to be string; equality (`Eq`/`Ne`) additionally works across matching value types.

&nbsp;

### Function Signatures

```go
// Column vs column
func (df *DataFrame) Gt(left, right string) (collection.Series, error)
func (df *DataFrame) Lt(left, right string) (collection.Series, error)
func (df *DataFrame) Ge(left, right string) (collection.Series, error)
func (df *DataFrame) Le(left, right string) (collection.Series, error)
func (df *DataFrame) Eq(left, right string) (collection.Series, error)
func (df *DataFrame) Ne(left, right string) (collection.Series, error)

// Column vs scalar
func (df *DataFrame) GtScalar(column string, scalar any) (collection.Series, error)
func (df *DataFrame) LtScalar(column string, scalar any) (collection.Series, error)
func (df *DataFrame) GeScalar(column string, scalar any) (collection.Series, error)
func (df *DataFrame) LeScalar(column string, scalar any) (collection.Series, error)
func (df *DataFrame) EqScalar(column string, scalar any) (collection.Series, error)
func (df *DataFrame) NeScalar(column string, scalar any) (collection.Series, error)
```

&nbsp;

### Example

Flag products that grew quarter-over-quarter and those priced above 10:

```go
grew, _ := df.Gt("Q2", "Q1")
_ = df.Assign("Grew", grew)

premium, _ := df.GtScalar("Price", 10.0)
_ = df.Assign("Premium", premium)

fmt.Println(df.String())
```

&nbsp;

### Output

```
+-----------+-----+-----+-------+------------+--------+---------+---------------+-------+---------+
| Product   | Q1  | Q2  | Price | TotalUnits | Growth | Revenue | DiscountPrice | Grew  | Premium |
+-----------+-----+-----+-------+------------+--------+---------+---------------+-------+---------+
| Widget    | 100 | 150 | 9.99  | 250        | 50     | 2497.5  | 8.991         | true  | false   |
| Gadget    | 80  | 90  | 14.5  | 170        | 10     | 2465    | 13.05         | true  | true    |
| Gizmo     | 120 | 110 | 7.25  | 230        | -10    | 1667.5  | 6.525         | false | false   |
| Doohickey | 60  | 75  | 19    | 135        | 15     | 2565    | 17.1          | true  | true    |
+-----------+-----+-----+-------+------------+--------+---------+---------------+-------+---------+
[4 rows x 10 columns]
```

&nbsp;

### Comparison Semantics

| Situation | Behavior |
|-----------|----------|
| Both numeric | Compared numerically (`int` and `float64` interoperate) |
| Both strings | Ordered lexicographically |
| `Eq` / `Ne` on matching non-numeric types | Compared by value |
| `Eq` / `Ne` on mismatched types | Treated as not equal (no error) |
| Ordering (`Gt`/`Lt`/`Ge`/`Le`) on incompatible types | Returns an error |
| A `nil` scalar in a scalar comparison | Returns an error |

&nbsp;

---

&nbsp;

## Null Propagation

A null in either operand always yields a null result:

```go
ndf, _ := gp.DataFrame(
    []string{"X", "Y"},
    []gpandas.Column{
        {1.0, nil, 3.0},
        {10.0, 20.0, nil},
    },
    map[string]any{"X": gpandas.FloatCol{}, "Y": gpandas.FloatCol{}},
)

sum, _ := ndf.Add("X", "Y")
_ = ndf.Assign("X_plus_Y", sum)
fmt.Println(ndf.String())
```

&nbsp;

### Output

```
+------+------+----------+
| X    | Y    | X_plus_Y |
+------+------+----------+
| 1    | 10   | 11       |
| null | 20   | null     |
| 3    | null | null     |
+------+------+----------+
[3 rows x 3 columns]
```

&nbsp;

---

&nbsp;

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "...: DataFrame is nil" | Operating on a nil DataFrame | Check DataFrame initialization |
| "...: column 'X' not found" | Invalid column name | Verify the column exists |
| "...: length mismatch..." | Columns have different row counts | Ensure both columns have equal length |
| "non-numeric value ... at row N" | Arithmetic on a non-numeric column | Use a numeric column or cast with `AsType` |
| "cannot order-compare T1 and T2" | Ordering incompatible types | Compare numbers with numbers, strings with strings |
| "...: scalar must not be nil" | `nil` passed to a scalar comparison | Provide a non-nil scalar |

&nbsp;

### Error Handling Example

```go
result, err := df.Add("Q1", "Q2")
if err != nil {
    switch {
    case strings.Contains(err.Error(), "not found"):
        log.Fatal("A column doesn't exist in the DataFrame")
    case strings.Contains(err.Error(), "non-numeric"):
        log.Fatal("Both columns must be numeric")
    case strings.Contains(err.Error(), "length mismatch"):
        log.Fatal("Columns must have the same number of rows")
    default:
        log.Fatalf("Arithmetic error: %v", err)
    }
}
```

&nbsp;

---

&nbsp;

## Thread Safety

All arithmetic and comparison methods take a read lock on the DataFrame while extracting column values and return a brand-new Series. The source DataFrame is never mutated, so concurrent reads are safe.

&nbsp;

---

&nbsp;

## Complete Example

```go
package main

import (
    "fmt"
    "log"

    "github.com/apoplexi24/gpandas"
)

func main() {
    gp := gpandas.GoPandas{}

    df, err := gp.DataFrame(
        []string{"Product", "Q1", "Q2", "Price"},
        []gpandas.Column{
            {"Widget", "Gadget", "Gizmo", "Doohickey"},
            {int64(100), int64(80), int64(120), int64(60)},
            {int64(150), int64(90), int64(110), int64(75)},
            {9.99, 14.50, 7.25, 19.00},
        },
        map[string]any{
            "Product": gpandas.StringCol{},
            "Q1":      gpandas.IntCol{},
            "Q2":      gpandas.IntCol{},
            "Price":   gpandas.FloatCol{},
        },
    )
    if err != nil {
        log.Fatalf("Failed to create DataFrame: %v", err)
    }

    // Derived numeric columns
    total, _ := df.Add("Q1", "Q2")
    _ = df.Assign("TotalUnits", total)

    revenue, _ := df.Mul("TotalUnits", "Price")
    _ = df.Assign("Revenue", revenue)

    // Boolean flags
    grew, _ := df.Gt("Q2", "Q1")
    _ = df.Assign("Grew", grew)

    premium, _ := df.GtScalar("Price", 10.0)
    _ = df.Assign("Premium", premium)

    fmt.Println(df.String())
}
```

See `examples/arithmetic/` in the repository for a runnable version.

&nbsp;

---

&nbsp;

## See Also

- [Adding Columns]({{< ref "adding-columns" >}}) - Attach the resulting Series with `Assign`
- [Transforming Columns]({{< ref "transforming-data" >}}) - Element-wise transforms with arbitrary functions
- [Filtering Data]({{< ref "filtering-data" >}}) - Use boolean results to subset rows
- [Summary Statistics]({{< ref "summary-statistics" >}}) - Aggregate numeric columns
- [Series]({{< ref "series" >}}) - The fundamental column type
