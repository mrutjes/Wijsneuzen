# Chips and Circuits Project

## Overview
This repository contains our project for the *Algorithms and Heuristics* course. The primary focus is on solving the **Chips and Circuits** problem, a computational challenge involving the efficient wiring of gates on a grid to minimize costs. The project explores algorithms and heuristics to achieve optimal solutions within the constraints of the problem.

---

## Problem Description
Integrated circuits, commonly known as chips, are essential components in modern technology. These circuits consist of gates that need to be connected through a grid. The goal is to:

1. **Minimize wire length**: Shorter connections lead to faster and cheaper circuits.
2. **Avoid collisions**: Wires cannot share grid segments to prevent circuit failures.
3. **Minimize intersections**: Crossings between wires increase costs and complexity.

### Cost Function
The total cost of a solution is calculated as:

\[
C = n + 300 * k
\]

Where:
- \( n \): Total wire length (in units).
- \( k \): Number of intersections between wires.

---

## Approach
### Key Steps:
1. **Grid Representation**: Create a data structure to represent the grid and fixed gate positions (only on base layer)
2. **Netlist Handling**: Implement a data structure to manage connections (nets) between gates.
3. **Algorithms**: Develop and test various algorithms and heuristics to minimize costs, such as:
   - Greedy approaches
   - A* search
   - Simulated annealing
4. **Layered Design**: Use multiple grid layers (up to 8) to resolve collisions and optimize layouts.
5. **Random Netlists**: Test performance on randomly generated netlists to evaluate robustness and scalability.

### Output
The solution is outputted in a standardized `.csv` format, detailing the wiring and associated costs.

---

## Results
Our project includes solutions for:
- **Predefined netlists**: Provided by the course.
- **Randomly generated netlists**: Created to test algorithm performance and limitations.

We document the results of each approach, including:
- Percentage of nets successfully connected.
- Total cost and breakdown (wire length and intersections).
- Computational efficiency.

---

## Getting Started
### Prerequisites
- Python 3.8+
- Required libraries (also listed in requirements.txt):
  - `numpy`
  - `matplotlib`
  - `pandas`