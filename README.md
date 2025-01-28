# Chips and Circuits Project

## Overview
This repository contains our project for the *Algorithms and Heuristics* course. The primary focus is on solving the **Chips and Circuits** problem, a computational challenge involving the efficient wiring of gates on a grid to minimize costs. The project explores algorithms and heuristics to achieve (optimal) solutions within the constraints of the problem.

---

## Problem Description
Integrated circuits, commonly known as chips, are essential components in modern technology. These circuits consist of gates that need to be connected through a grid. The goal is to:

1. **Avoid short circuits**: Wires cannot share grid segments to prevent circuit failures.
2. **Minimize intersections**: Crossings between wires increase costs and complexity.

### Cost Function
The total cost of a solution is calculated as:

\[
C = n + 300 * k
\]

Where:
- \( n \): Total wire length (in units).
- \( k \): Number of intersections between wires.

### Baseline
An algorithm is evaluated based on how many netlists it can successfully connect. Because a chip can be wired in various orders, the chosen sequence of connections can greatly influence the feasibility of a solution. To address this, we test the most promising netlist orders and look for any configurations that meet the requirements—specifically, that there is no short circuit. This will be our primary focus. Once we confirm that a valid wiring exists (i.e., no short circuits), we then aim to minimize the cost. 


---

## Approach
### Key Steps:
1. **Grid Representation**: Create a data structure to represent the grid and fixed gate positions (only on base layer)
2. **Netlist Handling**: Implement a data structure to manage connections (nets) between gates.
3. **Algorithms**: Develop and test various algorithms and heuristics to minimize costs, such as:
   - Manhattan distance based
   - Breadth First Search (Lee's algorithm)
   - Depth First Search
   - A* algorithm
4. **Layered Design**: Use multiple grid layers (up to 8) to resolve collisions and optimize layouts.
5. **Cost System**: Use a cost system to make sure that certain areas on the grid are more and less expensive to avoid collisions.
5. **Optimize Parameters**: Optimize the parameters of the cost of the grid to ensure that obtimal routing is achieved.
6. **Random Netlists**: Test performance on randomly generated netlists to evaluate robustness and scalability.

### Output
The solution is visualized in a 3D grid. 

---

## Results
Our project includes solutions for:
- **Predefined netlists**: Provided by the course.

We document the results of each approach, including:
- Percentage of nets succesfully conneted when testing different orders of netlists
- Total cost and breakdown (wire length and intersections).
- The time it has taken the algorithm to complete 250 iterations of a netlist.

---

## Getting Started

### Running the code

0. **Install the requirements in a unix environment**
   ```bash
   pip install -r requirements.txt

1. **Clone the repository**:
   ```bash
   git clone https://github.com/[your-repo]/Wijsneuzen.git
2. **Navitage to the main directory**
   ```bash 
   cd Wijsneuzen
3. **Run the code**
   ```bash
   python main.py

4. **To use a different algorithm, simply uncomment the desired algorithm, and comment the other ones in main.py**  
   You will be prompted for how many iterations the script has to run, which algorithm to use and how the netlist needs to be sorted.

---

### Prerequisites
- Python 3.8+
- Required libraries (also listed in requirements.txt):
  - `numpy`
  - `matplotlib`
  - `pandas`

---
### Structure of the Directory

- **gates_netlists**  
  This folder contains all the chip configurations along with their corresponding netlists. You will find multiple `.csv` files that define the gates’ positions (chip conformations) and the connections (netlists).

- **code**  
  The main codebase resides here:
  - **classes**  
    Contains all Python classes used throughout the project (e.g., data models, utility classes).
  - **algorithms**  
    Holds the core algorithmic functions and heuristics for solving the wiring problem.
   - **visualisation**  
   Contains the function to plot the wires in the grid.
   - **functions**  
   Contains helper functions in order to succesfully run the main.py
   - **imports**  
   This file bundles essential functions for tasks such as loading netlists, parsing CSV data, and setting up project resources.
   - **experiments**  
   This is a bash script to run 250 iterations of each combination of algorithm, netlist and sorting method used for the experiment. Run with the command below from the main directory. You will find the results in this directory.
   ```bash
   bash code/experiments/time_script.sh
