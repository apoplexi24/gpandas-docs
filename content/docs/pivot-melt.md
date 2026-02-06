---
title: "Pivot and Melt"
description: "Reshape DataFrames between wide and long formats using pivot tables and melt operations"
icon: "pivot_table_chart"
weight: 45
---

Learn how to reshape DataFrames using pivot tables and melt operations in GPandas, enabling powerful data analysis workflows.

<!-- IMAGE_PLACEHOLDER: Visual showing wide-to-long and long-to-wide data transformations -->

&nbsp;

## Overview

GPandas provides two complementary reshaping operations:

| Operation | Method | Description |
|-----------|--------|-------------|
| Pivot Table | `PivotTable()` | Aggregate and reshape data into a spreadsheet-style pivot table |
| Melt | `Melt()` | Unpivot data from wide format to long format |

&nbsp;

---

&nbsp;

## PivotTable

Creates a spreadsheet-style pivot table that groups data by index columns, spreads values across new columns, and applies aggregation functions.

&nbsp;

### Function Signature

```go
func (df *DataFrame) PivotTable(opts PivotTableOptions) (*DataFrame, error)
```

&nbsp;

### PivotTableOptions

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `Index` | `[]string` | Column(s) for row grouping | Yes |
| `Columns` | `string` | Column whose unique values become new column headers | Yes |
| `Values` | `[]string` | Column(s) to aggregate | Yes |
| `AggFunc` | `AggFunc` | Aggregation function to apply | No (default: `AggMean`) |
| `FillValue` | `any` | Value for missing combinations | No (default: `nil`) |

&nbsp;

### Aggregation Functions

| Constant | Description |
|----------|-------------|
| `AggSum` | Sum of values |
| `AggMean` | Mean of values (default) |
| `AggCount` | Count of non-null values |
| `AggMin` | Minimum value |
| `AggMax` | Maximum value |

&nbsp;

---

&nbsp;

## Sample Data

All pivot examples use this sales DataFrame:

### Sales DataFrame

| Region | Quarter | Product | Sales |
|--------|---------|---------|-------|
| North | Q1 | Widgets | 100 |
| North | Q1 | Gadgets | 150 |
| North | Q2 | Widgets | 120 |
| South | Q1 | Widgets | 90 |
| South | Q2 | Widgets | 110 |
| South | Q2 | Gadgets | 130 |

&nbsp;

### Setup Code

```go
package main

import (
    "fmt"
    "log"

    "github.com/apoplexi24/gpandas"
    "github.com/apoplexi24/gpandas/dataframe"
)

func main() {
    gp := gpandas.GoPandas{}
    
    // Create sales DataFrame
    df, _ := gp.DataFrame(
        []string{"Region", "Quarter", "Product", "Sales"},
        []gpandas.Column{
            {"North", "North", "North", "South", "South", "South"},
            {"Q1", "Q1", "Q2", "Q1", "Q2", "Q2"},
            {"Widgets", "Gadgets", "Widgets", "Widgets", "Widgets", "Gadgets"},
            {100.0, 150.0, 120.0, 90.0, 110.0, 130.0},
        },
        map[string]any{
            "Region":  gpandas.StringCol{},
            "Quarter": gpandas.StringCol{},
            "Product": gpandas.StringCol{},
            "Sales":   gpandas.FloatCol{},
        },
    )
    
    // Examples follow...
}
```

&nbsp;

---

&nbsp;

## PivotTable with Sum

Create a pivot table showing total sales by region and quarter:

```mermaid
flowchart LR
    subgraph Input["Original DataFrame"]
        I1[Region: North/South]
        I2[Quarter: Q1/Q2]
        I3[Sales: values]
    end
    
    subgraph Pivot["PivotTable Operation"]
        OP[Group by Region<br/>Spread by Quarter<br/>Sum Sales]
    end
    
    subgraph Result["Pivot Table"]
        R1[Region | Q1 | Q2]
        R2[North  | 250| 120]
        R3[South  | 90 | 240]
    end
    
    I1 --> OP
    I2 --> OP
    I3 --> OP
    OP --> R1
    OP --> R2
    OP --> R3
    
    style Input fill:#1e293b,stroke:#3b82f6,stroke-width:2px
    style Pivot fill:#1e293b,stroke:#f59e0b,stroke-width:2px
    style Result fill:#1e293b,stroke:#22c55e,stroke-width:2px
```

&nbsp;

### Example

```go
pivot, err := df.PivotTable(dataframe.PivotTableOptions{
    Index:   []string{"Region"},
    Columns: "Quarter",
    Values:  []string{"Sales"},
    AggFunc: dataframe.AggSum,
})
if err != nil {
    log.Fatalf("Pivot failed: %v", err)
}
fmt.Println(pivot.String())
```

&nbsp;

### Output

```
+--------+-----+-----+
| Region | Q1  | Q2  |
+--------+-----+-----+
| North  | 250 | 120 |
| South  | 90  | 240 |
+--------+-----+-----+
[2 rows x 3 columns]
```

&nbsp;

---

&nbsp;

## PivotTable with Mean

Calculate average sales by region and quarter:

```go
pivot, err := df.PivotTable(dataframe.PivotTableOptions{
    Index:   []string{"Region"},
    Columns: "Quarter",
    Values:  []string{"Sales"},
    AggFunc: dataframe.AggMean,
})
if err != nil {
    log.Fatalf("Pivot failed: %v", err)
}
fmt.Println(pivot.String())
```

&nbsp;

### Output

```
+--------+-----+-----+
| Region | Q1  | Q2  |
+--------+-----+-----+
| North  | 125 | 120 |
| South  | 90  | 120 |
+--------+-----+-----+
[2 rows x 3 columns]
```

&nbsp;

---

&nbsp;

## PivotTable with Count

Count the number of transactions by region and quarter:

```go
pivot, err := df.PivotTable(dataframe.PivotTableOptions{
    Index:   []string{"Region"},
    Columns: "Quarter",
    Values:  []string{"Sales"},
    AggFunc: dataframe.AggCount,
})
if err != nil {
    log.Fatalf("Pivot failed: %v", err)
}
fmt.Println(pivot.String())
```

&nbsp;

### Output

```
+--------+----+----+
| Region | Q1 | Q2 |
+--------+----+----+
| North  | 2  | 1  |
| South  | 1  | 2  |
+--------+----+----+
[2 rows x 3 columns]
```

&nbsp;

---

&nbsp;

## PivotTable with Multiple Values

Pivot with multiple value columns creates combined column names:

```go
// Assuming DataFrame has both Sales and Units columns
pivot, err := df.PivotTable(dataframe.PivotTableOptions{
    Index:   []string{"Region"},
    Columns: "Quarter",
    Values:  []string{"Sales", "Units"},
    AggFunc: dataframe.AggSum,
})
```

&nbsp;

### Output

```
+--------+----------+----------+----------+----------+
| Region | Sales_Q1 | Sales_Q2 | Units_Q1 | Units_Q2 |
+--------+----------+----------+----------+----------+
| North  | 250      | 120      | 10       | 5        |
| South  | 90       | 240      | 4        | 12       |
+--------+----------+----------+----------+----------+
[2 rows x 5 columns]
```

&nbsp;

---

&nbsp;

## PivotTable with FillValue

Use `FillValue` to replace missing combinations instead of null:

```go
pivot, err := df.PivotTable(dataframe.PivotTableOptions{
    Index:     []string{"Product"},
    Columns:   "Quarter",
    Values:    []string{"Sales"},
    AggFunc:   dataframe.AggSum,
    FillValue: 0.0,  // Use 0 instead of null for missing combinations
})
if err != nil {
    log.Fatalf("Pivot failed: %v", err)
}
fmt.Println(pivot.String())
```

&nbsp;

### Output

```
+---------+-----+-----+
| Product | Q1  | Q2  |
+---------+-----+-----+
| Gadgets | 150 | 130 |
| Widgets | 190 | 230 |
+---------+-----+-----+
[2 rows x 3 columns]
```

&nbsp;

---

&nbsp;

## Melt

Transforms a DataFrame from wide format to long format by unpivoting columns into rows.

&nbsp;

### Function Signature

```go
func (df *DataFrame) Melt(opts MeltOptions) (*DataFrame, error)
```

&nbsp;

### MeltOptions

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `IdVars` | `[]string` | Identifier columns to keep fixed | - |
| `ValueVars` | `[]string` | Columns to unpivot | All non-id columns |
| `VarName` | `string` | Name for the variable column | `"variable"` |
| `ValueName` | `string` | Name for the value column | `"value"` |

&nbsp;

---

&nbsp;

## Melt Sample Data

### Wide Format DataFrame (Grades)

| Student | Math | Science | English |
|---------|------|---------|---------|
| Alice | 90 | 85 | 88 |
| Bob | 80 | 75 | 92 |
| Charlie | 95 | 90 | 85 |

&nbsp;

### Setup Code

```go
gp := gpandas.GoPandas{}

grades, _ := gp.DataFrame(
    []string{"Student", "Math", "Science", "English"},
    []gpandas.Column{
        {"Alice", "Bob", "Charlie"},
        {90.0, 80.0, 95.0},
        {85.0, 75.0, 90.0},
        {88.0, 92.0, 85.0},
    },
    map[string]any{
        "Student": gpandas.StringCol{},
        "Math":    gpandas.FloatCol{},
        "Science": gpandas.FloatCol{},
        "English": gpandas.FloatCol{},
    },
)
```

&nbsp;

---

&nbsp;

## Basic Melt

Transform from wide to long format:

```mermaid
flowchart LR
    subgraph Wide["Wide Format"]
        W1[Student | Math | Science | English]
        W2[Alice   | 90   | 85      | 88]
        W3[Bob     | 80   | 75      | 92]
    end
    
    subgraph Melt["Melt Operation"]
        OP[Keep: Student<br/>Unpivot: Math, Science, English]
    end
    
    subgraph Long["Long Format"]
        L1[Student | Subject | Score]
        L2[Alice   | Math    | 90]
        L3[Alice   | Science | 85]
        L4[Alice   | English | 88]
        L5[Bob     | Math    | 80]
        L6[...]
    end
    
    W1 --> OP
    W2 --> OP
    W3 --> OP
    OP --> L1
    OP --> L2
    OP --> L3
    OP --> L4
    OP --> L5
    OP --> L6
    
    style Wide fill:#1e293b,stroke:#3b82f6,stroke-width:2px
    style Melt fill:#1e293b,stroke:#f59e0b,stroke-width:2px
    style Long fill:#1e293b,stroke:#22c55e,stroke-width:2px
```

&nbsp;

### Example

```go
melted, err := grades.Melt(dataframe.MeltOptions{
    IdVars:    []string{"Student"},
    VarName:   "Subject",
    ValueName: "Score",
})
if err != nil {
    log.Fatalf("Melt failed: %v", err)
}
fmt.Println(melted.String())
```

&nbsp;

### Output

```
+---------+---------+-------+
| Student | Subject | Score |
+---------+---------+-------+
| Alice   | Math    | 90    |
| Alice   | Science | 85    |
| Alice   | English | 88    |
| Bob     | Math    | 80    |
| Bob     | Science | 75    |
| Bob     | English | 92    |
| Charlie | Math    | 95    |
| Charlie | Science | 90    |
| Charlie | English | 85    |
+---------+---------+-------+
[9 rows x 3 columns]
```

&nbsp;

---

&nbsp;

## Melt with Specific ValueVars

Unpivot only specific columns:

```go
melted, err := grades.Melt(dataframe.MeltOptions{
    IdVars:    []string{"Student"},
    ValueVars: []string{"Math", "Science"},  // Exclude English
    VarName:   "Subject",
    ValueName: "Score",
})
if err != nil {
    log.Fatalf("Melt failed: %v", err)
}
fmt.Println(melted.String())
```

&nbsp;

### Output

```
+---------+---------+-------+
| Student | Subject | Score |
+---------+---------+-------+
| Alice   | Math    | 90    |
| Alice   | Science | 85    |
| Bob     | Math    | 80    |
| Bob     | Science | 75    |
| Charlie | Math    | 95    |
| Charlie | Science | 90    |
+---------+---------+-------+
[6 rows x 3 columns]
```

&nbsp;

---

&nbsp;

## Melt Without IdVars

Melt all columns into long format:

```go
melted, err := df.Melt(dataframe.MeltOptions{
    // No IdVars - all columns unpivoted
    VarName:   "column",
    ValueName: "data",
})
```

&nbsp;

---

&nbsp;

## Pivot and Melt Relationship

Pivot and Melt are inverse operations:

```mermaid
flowchart TB
    subgraph Long["Long Format"]
        LData[Student | Subject | Score]
    end
    
    subgraph Wide["Wide Format"]
        WData[Student | Math | Science | English]
    end
    
    Long -->|PivotTable| Wide
    Wide -->|Melt| Long
    
    style Long fill:#1e293b,stroke:#3b82f6,stroke-width:2px
    style Wide fill:#1e293b,stroke:#22c55e,stroke-width:2px
```

&nbsp;

### Round-Trip Example

```go
// Start with wide format
wideDF := grades  // Student | Math | Science | English

// Convert to long format
longDF, _ := wideDF.Melt(dataframe.MeltOptions{
    IdVars:    []string{"Student"},
    VarName:   "Subject",
    ValueName: "Score",
})

// Convert back to wide format
wideAgain, _ := longDF.PivotTable(dataframe.PivotTableOptions{
    Index:   []string{"Student"},
    Columns: "Subject",
    Values:  []string{"Score"},
    AggFunc: dataframe.AggSum,
})

// wideAgain has same structure as original wideDF
```

&nbsp;

---

&nbsp;

## Aggregation Comparison

Visual comparison of all aggregation functions:

| AggFunc | Formula | Use Case |
|---------|---------|----------|
| `AggSum` | Σ values | Total sales, counts |
| `AggMean` | Σ values / n | Averages, ratings |
| `AggCount` | Count non-null | Transaction counts |
| `AggMin` | min(values) | Lowest price, first date |
| `AggMax` | max(values) | Highest score, peak value |

&nbsp;

---

&nbsp;

## Error Handling

### PivotTable Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "Index column(s) must be specified" | Empty `Index` | Provide at least one index column |
| "Columns parameter must be specified" | Empty `Columns` | Specify column for headers |
| "Values column(s) must be specified" | Empty `Values` | Specify columns to aggregate |
| "index column 'X' not found" | Invalid column name | Check column exists |

&nbsp;

### Melt Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "id_vars column 'X' not found" | Invalid IdVars | Check column exists |
| "value_vars column 'X' not found" | Invalid ValueVars | Check column exists |
| "no columns to melt" | All columns in IdVars | Leave some columns to unpivot |

&nbsp;

### Error Handling Example

```go
pivot, err := df.PivotTable(dataframe.PivotTableOptions{
    Index:   []string{"Region"},
    Columns: "Quarter",
    Values:  []string{"Sales"},
    AggFunc: dataframe.AggSum,
})
if err != nil {
    switch {
    case strings.Contains(err.Error(), "not found"):
        log.Fatal("Column doesn't exist in DataFrame")
    case strings.Contains(err.Error(), "must be specified"):
        log.Fatal("Missing required option")
    default:
        log.Fatalf("Pivot error: %v", err)
    }
}
```

&nbsp;

---

&nbsp;

## Complete Example: Sales Analysis

```go
package main

import (
    "fmt"
    "log"

    "github.com/apoplexi24/gpandas"
    "github.com/apoplexi24/gpandas/dataframe"
)

func main() {
    gp := gpandas.GoPandas{}
    
    // Load sales data
    sales, err := gp.Read_csv("sales_data.csv")
    if err != nil {
        log.Fatalf("Failed to load data: %v", err)
    }
    
    fmt.Println("Original Data:")
    fmt.Println(sales.String())
    
    // Create pivot table: Total sales by product and region
    pivot, err := sales.PivotTable(dataframe.PivotTableOptions{
        Index:     []string{"Product"},
        Columns:   "Region",
        Values:    []string{"Revenue"},
        AggFunc:   dataframe.AggSum,
        FillValue: 0.0,
    })
    if err != nil {
        log.Fatalf("Pivot failed: %v", err)
    }
    
    fmt.Println("\nSales by Product and Region:")
    fmt.Println(pivot.String())
    
    // Export pivot table
    _, err = pivot.ToCSV("sales_pivot.csv", ",")
    if err != nil {
        log.Printf("Export warning: %v", err)
    }
    
    // Melt the pivot table back to long format for visualization
    melted, err := pivot.Melt(dataframe.MeltOptions{
        IdVars:    []string{"Product"},
        VarName:   "Region",
        ValueName: "TotalRevenue",
    })
    if err != nil {
        log.Fatalf("Melt failed: %v", err)
    }
    
    fmt.Println("\nMelted for Visualization:")
    fmt.Println(melted.String())
}
```

&nbsp;

## See Also

- [DataFrame Operations]({{< ref "dataframe-operations" >}}) - Select and transform data
- [Merging Data]({{< ref "merging-data" >}}) - Join multiple DataFrames
- [SQL Integration]({{< ref "sql-integration" >}}) - Use SQL for data manipulation

