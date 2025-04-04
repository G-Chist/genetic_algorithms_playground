# Genetic Algorithms Playground

This repository contains various applications of genetic algorithms (GAs), demonstrating their use in solving different optimization problems. The code is well-documented with clear comments explaining each step.

## Contents

### Box Optimization with Pymunk
- Uses the pymunk physics engine to simulate falling balls inside a box.
- The genetic algorithm optimizes the box dimensions to be as small as possible while keeping the balls inside.
- Includes comments explaining physics simulation, fitness evaluation, and genetic operations.

### Basketball Optimization with Pymunk
- Uses the pymunk physics engine to simulate a ball being thrown at a box
- Can be tuned for trickshots, high angle shots, etc.

### Knapsack Problem
- Implements a GA to solve the 0/1 knapsack problem, maximizing value while staying within a weight limit.
- Selection, crossover, and mutation are clearly documented.

### Polynomial Approximation
- Uses a genetic algorithm to approximate mathematical functions with polynomials.
- Shows how GAs can be applied to curve fitting and symbolic regression.

### Power Plant Revenue Optimization
- Simulates a power plant adjusting its output to maximize revenue given fluctuating electricity prices.
- The GA optimizes production levels while considering market constraints.
- This problem is very similar to the knapsack problem!
  - The solution has the same form, but the fitness function is different.

## Code Documentation

Each file contains inline comments explaining:
- How the genetic algorithm is structured
- How fitness functions are designed for each problem

The goal is to make the code easy to follow, even for those new to genetic algorithms.

## Requirements & Setup

Install dependencies using:

```bash
pip install pygame pymunk pygad pillow matplotlib numpy
