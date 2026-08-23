# Genetic Algorithm — Warehouse Zone Assignment

Constraint-aware genetic algorithm that assigns warehouse products to storage zones while minimizing capacity and policy violations.

## Overview

AI assignment (A#02, section A) by i222327. Each chromosome encodes one zone ID per product; evolution searches for a low-penalty layout of 20 products across 8 zones.

## Problem

### Products

Twenty SKUs with weight, category, and flags (fragile, hazardous, temperature-controlled, demand). Examples: glass bottles, frozen meat, cleaning acid, rice bags, ice cream, industrial bleach, wine, paint, flour, and related items.

### Zones and capacities

| Zone | Capacity (kg) |
|------|---------------|
| Z1 | 120 |
| Z2–Z5 | 80 each |
| Z6 | 60 |
| Z7 | 150 |
| Z8 | 100 |

### Penalty rules (fitness)

Lower total penalty is better:

- Zone weight capacity overflow
- Fragile items not in Z3
- Hazardous items not in Z5
- Temperature-controlled items outside Z4 / Z8
- High-demand items not in Z6
- Heavy items not in Z1
- Unauthorized products in Z8
- Same category split across different zones
- Food and chemical items sharing a zone

## Algorithm

Implemented in pure Python (random module only):

| Operator | Detail |
|----------|--------|
| Encoding | Length-20 list; gene in {1…8} |
| Selection | Tournament (size 5) |
| Crossover | Two-point |
| Mutation | Per-gene random zone reassignment |
| Elitism | Best 2 kept each generation |
| Defaults | Population 150, generations 900, mutation rate 0.08 |

Prints the storage plan per zone, product-to-zone assignments, best fitness, and remaining violations.

## Repository Contents

| File | Description |
|------|-------------|
| `i222327_A#02_A.py` | Complete genetic algorithm solver |
| `A2.pdf` | Assignment statement |
| `i222327_A#02_Report.docx` | Written report |
| `VIVA.docx` | Viva notes |

## Getting Started

```bash
python "i222327_A#02_A.py"
```

No third-party packages required (Python 3 standard library).

```python
genetic_algorithm(population_size=150, generations=900, mutation_rate=0.08)
```

## Project Structure

```
Genetic_Algorithm/
├── i222327_A#02_A.py
├── A2.pdf
├── i222327_A#02_Report.docx
└── VIVA.docx
```

## Author

Mohammad Rohaan — i222327 · [rohaan2802](https://github.com/rohaan2802)
