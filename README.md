# A Modified Genetic Algorithm for Balanced Academic Curriculum Problem with Semester-Specific Availability Constraint

## Overview
This project implements a Modified Genetic Algorithm (MGA) approach to solve the Balanced Academic Curriculum Problem (BACP) with semester-specific availability constraints. The algorithm optimizes course scheduling across academic semesters while respecting prerequisites, course limit, credit limits, and unit availability constraints.

## Problem Description
The Balanced Academic Curriculum Problem involves distributing academic units across multiple semesters under the following constraints:
- **Prerequisite constraints**: A course can only be taken after all its prerequisites have been completed
- **Credit load balancing**: The number of credits per semester should be balanced and within specified limits
- **Unit limits**: Each semester must have a minimum and maximum number of units
- **Availability constraints**: Units are only available in specific semesters (a real-world constraint extension to the classic BACP)

## Features
- Direct integer encoding for chromosome representation
- Constraint-aware guided mutation operation
- Penalty-based fitness function for constraint violations
- Tournament selection for parent selection
- Single-point crossover for genetic material exchange
- Support for both classic BACP datasets and real-world university course data

## Requirements
- Python 3.x
- NumPy
- Matplotlib
- DEAP (Distributed Evolutionary Algorithms in Python)
- JSON

## Installation
1. Clone this repository
2. Create a virtual environment (optional but recommended):
   ```
   python -m venv .venv
   ```
3. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Unix/MacOS: `source .venv/bin/activate`
4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage
Run the main script:
```
python MGA.py
```

When prompted, select one of the available JSON files:
- MJ-IAID.json (Murdoch University dataset)
- bacp08.json (CSPLib benchmark)
- bacp10.json (CSPLib benchmark)
- bacp12.json (CSPLib benchmark)

The program will execute the genetic algorithm and save results to a file in the `results` directory.

## Dataset Format
Input data should be in JSON format with the following structure:
```json
{
  "units": {
    "course_code1": {
      "credits": 3,
      "available": [1, 3]
    },
    "course_code2": {
      "credits": 4,
      "available": [1, 2, 3, 4]
    },
    ...
  },
  "prerequisites": {
    "course_code2": ["course_code1"],
    ...
  },
  "parameters": {
    "Total_Semesters": 4,
    "Min_Credits_Sem": 10,
    "Max_Credits_Sem": 14,
    "Min_Units_Sem": 3,
    "Max_Units_Sem": 5
  }
}
```

## Algorithm Parameters
- Population size: 100
- Generations: 300
- Tournament size: 10
- Crossover probability: 0.9
- Mutation probability: 0.1

These parameters can be adjusted in the main script.

## Output
The algorithm produces:
1. A text file containing:
   - Parameter settings
   - Statistics for each run (fitness metrics, execution time)
   - Overall statistics across all runs
   - The best course schedule found
2. A convergence plot showing fitness evolution over generations

## Project Structure
```
MGA/
├── MGA.py                  # Main script
├── requirements.txt        # Dependencies
├── bacp08.json             # BACP benchmark dataset
├── bacp10.json             # BACP benchmark dataset
├── bacp12.json             # BACP benchmark dataset
├── MJ-IAID.json            # Murdoch University dataset
└── results/                # Results directory
```

## Algorithm Description
The modified genetic algorithm works as follows:
1. Initialize population with random but available semester assignments
2. Evaluate fitness based on constraint violations and load balancing
3. Select parents using tournament selection
4. Apply crossover and mutation operators to generate offspring
5. Repeat evaluation and selection for the specified number of generations
6. Return the best solution found

## Fitness Function
The fitness value is calculated based on:
- Availability violations (highest penalty)
- Prerequisite violations
- Credit limit violations
- Course limit violations
- Maximum credit load (the main objective to minimize)


## References
- The BACP benchmark datasets are from the CSPLib library (https://www.csplib.org/Problems/prob030/data/)
- The real-world datasets are from Murdoch University's School of Science, Technology, Engineering and Mathematics (https://handbook.murdoch.edu.au/)

