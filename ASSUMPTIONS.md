# Project Assumptions and Design Decisions

## Overview
This document outlines assumptions made during the development of the FastBox Delivery System when faced with ambiguous scenarios not explicitly defined in the assignment specification.

---

## 1. Package Assignment Logic

### Assumption: Nearest Agent by Warehouse Distance
**Scenario:** The assignment states "assign packages to the nearest agent" but doesn't specify whether this is based on:
- Distance from agent to warehouse, OR
- Distance from agent to destination

**Decision Made:** Distance is calculated from **agent's current position to the warehouse** where the package is located.

**Rationale:** 
- Agents must first travel to the warehouse to pick up the package
- This represents the most realistic logistics scenario
- Minimizes initial travel time for pickup

---

## 2. Agent Position Updates

### Assumption: Agent Position Updates After Each Delivery
**Scenario:** Not explicitly stated whether agents return to base or stay at delivery location.

**Decision Made:** Agent's position is **updated to the destination** after each delivery (not returning to starting point or warehouse).

**Rationale:**
- More efficient routing (no backtracking)
- Real-world delivery systems optimize by chaining deliveries
- Minimizes total distance traveled

---

## 3. Multiple Packages at Same Warehouse

### Assumption: Sequential Processing
**Scenario:** When multiple packages from the same warehouse are assigned to the same agent, order of delivery is not specified.

**Decision Made:** Packages are delivered in the **order they appear in the input JSON**.

**Rationale:**
- Maintains deterministic, reproducible results
- Preserves package priority based on data order
- Simple to implement and verify

---

## 4. Tie-Breaking in Assignment

### Assumption: First Agent Wins
**Scenario:** When two agents are equidistant from a warehouse, which agent gets the package?

**Decision Made:** The agent that appears **first in the data structure** is assigned the package.

**Rationale:**
- Deterministic behavior
- Prevents random assignment variations
- Consistent with dictionary iteration order in Python 3.7+

---

## 5. Efficiency Calculation for Idle Agents

### Assumption: Zero Efficiency for Zero Deliveries
**Scenario:** How to calculate efficiency for agents who delivered no packages?

**Decision Made:** Agents with 0 packages show **efficiency = 0.0** (not division by zero or infinity).

**Rationale:**
- Prevents mathematical errors
- Idle agents are excluded from "best agent" calculation
- Clear indication of non-participation

---

## 6. Best Agent Selection

### Assumption: Active Agents Only
**Scenario:** Can an agent with 0 deliveries be considered "best"?

**Decision Made:** Only agents who **delivered at least 1 package** are eligible for "best agent".

**Rationale:**
- An idle agent hasn't performed any work
- Efficiency metric is only meaningful with actual deliveries
- Reflects real-world performance evaluation

---

## 7. Distance Calculation Precision

### Assumption: Round to 2 Decimal Places
**Scenario:** Assignment shows distances like "85.32" but doesn't specify rounding rules.

**Decision Made:** All distances are **rounded to 2 decimal places** in the final report.

**Rationale:**
- Matches format shown in assignment examples
- Sufficient precision for logistics planning
- Maintains clean, readable output

---

## 8. Coordinate System

### Assumption: Standard Cartesian Coordinates
**Scenario:** Coordinate interpretation not specified.

**Decision Made:** Using standard **2D Cartesian coordinates** where:
- [x, y] represents a point in 2D space
- Euclidean distance: √((x₂-x₁)² + (y₂-y₁)²)

**Rationale:**
- Standard mathematical convention
- Matches formula provided in assignment
- No negative coordinates in test data observed

---

## 9. Input Data Validation

### Assumption: Input Data is Valid
**Scenario:** Assignment doesn't specify handling of invalid/corrupt data.

**Decision Made:** Assume all input JSON files are **well-formed and valid**:
- All warehouse/agent IDs referenced in packages exist
- Coordinates are valid numbers
- Required fields are present

**Rationale:**
- Test cases provided are all valid
- Focus on core algorithm implementation
- Error handling can be added in production version

---

## 10. File Output Behavior

### Assumption: Overwrite Existing Reports
**Scenario:** What happens if report files already exist?

**Decision Made:** **Overwrite** existing report files with same name.

**Rationale:**
- Ensures latest results are always available
- Prevents accumulation of stale data
- Standard behavior for automated systems

---

## 11. Visualization Scaling

### Assumption: Auto-Scale to Fit Terminal
**Scenario:** ASCII visualization may need to fit different screen sizes.

**Decision Made:** Automatically **scale coordinates** to fit within ~70 columns × 25 rows.

**Rationale:**
- Ensures readability on standard terminals
- Maintains relative positioning
- Prevents line wrapping issues

---

## 12. Batch Processing Error Handling

### Assumption: Continue on Individual Failures
**Scenario:** In batch mode, should one failure stop all processing?

**Decision Made:** **Continue processing** remaining test cases even if one fails.

**Rationale:**
- Maximizes useful output
- Allows partial completion
- Easier to identify specific problem cases

---

## Additional Notes

- All assumptions are documented in code comments
- Test cases validated against assumptions
- Alternative approaches considered but not implemented for simplicity
- Design prioritizes clarity and maintainability

