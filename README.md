# Job Shop Scheduling Optimization Using a Genetic Algorithm

A Python-based artificial intelligence project that applies a genetic algorithm to optimize job shop scheduling in a manufacturing environment.

## Overview

The system schedules multiple jobs across a set of machines while respecting operation order and machine-capacity constraints. Its goal is to reduce the total production time by generating and evolving possible schedules.

Each job contains a sequence of operations. Every operation specifies the required machine and processing time.

## Main Features

- Accepts a custom number of jobs and machines
- Parses job operations and processing times
- Generates valid machine schedules
- Prevents overlapping operations on the same machine
- Preserves the required operation order within each job
- Applies tournament selection, crossover, and mutation
- Displays the resulting schedule and total production time

## Technologies

- Python
- Genetic Algorithms
- Artificial Intelligence
- Optimization
- Job Shop Scheduling

## Genetic Algorithm Components

- **Chromosome representation:** Encodes job operations, assigned machines, and scheduling times
- **Population initialization:** Generates an initial set of candidate schedules
- **Selection:** Uses tournament selection to choose parent schedules
- **Crossover:** Combines selected parents to generate new candidates
- **Mutation:** Swaps operations to maintain population diversity
- **Fitness objective:** Evaluates schedules based on total production time

## Project Structure

```text
job-shop-scheduling-genetic-algorithm/
├── README.md
├── .gitignore
├── sample_input.txt
├── docs/
│   └── project-requirements.pdf
└── src/
    └── job_shop_scheduling_ga.py
```

## How to Run

1. Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
```

2. Open the project folder:

```bash
cd job-shop-scheduling-genetic-algorithm
```

3. Run the Python program:

```bash
python src/job_shop_scheduling_ga.py
```

4. Enter the number of jobs and machines, followed by the job data.

Example:

```text
Enter number of Jobs:
2

Enter number of Machines:
4

Enter Jobs data:
Job_1: M1[10] -> M2[5] -> M4[12]
Job_2: M2[7] -> M3[15] -> M1[8]
```

Press Enter on an empty line after entering the final job.

## Example Output

The program prints a schedule containing:

- Job number
- Machine assignment
- Start time
- End time
- Total production time

## Academic Context

Developed for the **Artificial Intelligence (ENCS3340)** course at Birzeit University.

## Author

**Masa Jalamneh**

## License

This project was developed for educational purposes.
