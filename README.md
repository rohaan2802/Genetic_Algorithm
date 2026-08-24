# Warehouse Zone Assignment — Genetic Algorithm

Constraint-aware genetic algorithm that assigns **20 warehouse products** to **8 storage zones** while minimizing a weighted penalty (capacity overflow, policy, category split, food/chemical mixing). Chromosomes are length-20 integer lists (zone IDs 1–8). Implemented in pure Python for FAST-NUCES AI Assignment **A#02 section A** (`i222327_A#02_A.py`) by **Mohammad Rohaan (i222327)**.

## Table of contents

- [Problem statement / academic context](#problem-statement--academic-context)
- [Features](#features)
- [Architecture / design](#architecture--design)
- [Algorithms and data structures](#algorithms-and-data-structures)
- [File-by-file reference](#file-by-file-reference)
- [Data formats](#data-formats)
- [Tech stack](#tech-stack)
- [Project structure](#project-structure)
- [Prerequisites and install](#prerequisites-and-install)
- [How to build and run](#how-to-build-and-run)
- [Usage walkthrough](#usage-walkthrough)
- [Configuration / constants](#configuration--constants)
- [Results / metrics](#results--metrics)
- [Controls / CLI](#controls--cli)
- [Known limitations / bugs](#known-limitations--bugs)
- [How to extend](#how-to-extend)
- [Author](#author)

## Problem statement / academic context

Place every SKU into exactly one zone. Zones have kilogram capacities; products have weight, category, and flags (fragile, hazardous, temperature-controlled, demand). Fitness is **total penalty** (lower is better). A perfect layout scores **0**, which the GA treats as an early-stop. Many rules **conflict** (e.g. high-demand items want Z6 which only holds 60 kg; fragile items must be Z3; same-category items must share a zone; food cannot sit with chemicals), so a zero-penalty genome is typically infeasible — the search returns the lowest-penalty compromise found in 900 generations.

## Features

- Integer encoding: gene `i` ∈ `{1…8}` is the zone of `products[i]`.
- Full penalty breakdown printed as human-readable violation strings.
- Tournament selection (size **5** in the evolutionary loop).
- Two-point crossover with ordered cut points.
- Per-gene mutation (rate **0.08** at the entry-point call).
- Elitism: copy the two best chromosomes unchanged each generation.
- Population **150**, generations **900**, stop if fitness hits 0.
- Reports: per-zone packing list + utilized kg / capacity, product→zone map, best fitness, generations run, remaining violations.

## Architecture / design

No classes. Global tables (`products`, `zones`, named sets) plus functions:

| Function | Role |
|----------|------|
| `fitness(chromosome)` | Returns `(total_penalty: int, violations: list[str])`. |
| `create_chromosome()` | 20 uniform random genes `randint(1,8)`. |
| `create_population(n)` | List of chromosomes. |
| `tournament_selection(pop, tournament_size=3)` | Sample, return lowest fitness. **Called with size 5.** |
| `two_point_crossover(p1, p2)` | Two children. |
| `mutate(chrom, mutation_rate=0.1)` | Independent gene re-rolls. **Called with 0.08.** |
| `genetic_algorithm(population_size=100, generations=200, mutation_rate=0.1)` | Main loop. **Invoked as 150 / 900 / 0.08.** |
| `print_storage_plan(chrom)` | Zone contents and weights. |
| `print_product_assignments(chrom)` | `name -> Zk`. |

The script **runs the GA at import** (no `if __name__ == "__main__"`).

## Algorithms and data structures

### Product catalog (index = gene index)

| # | Name | kg | Category | Flags used by fitness |
|---|------|----|----------|------------------------|
| P1 | Glass Bottles | 20 | Beverage | fragile |
| P2 | Frozen Meat | 30 | Food | temp, high demand, food, Z8-eligible |
| P3 | Cleaning Acid | 10 | Chemical | hazardous, chemical |
| P4 | Rice Bags | 50 | Grocery | high demand, **heavy** |
| P5 | Ceramic Plates | 15 | Kitchenware | fragile |
| P6 | Ice Cream | 25 | Food | temp, high demand, food (**not** Z8-eligible) |
| P7 | Detergent | 12 | Chemical | hazardous, chemical |
| P8 | Chips Carton | 8 | Snacks | high demand |
| P9 | Olive Oil Bottles | 18 | Grocery | fragile |
| P10 | Industrial Bleach | 22 | Chemical | hazardous, chemical |
| P11 | Yogurt Cartons | 14 | Food | temp, high demand, food, Z8-eligible |
| P12 | Flour Bags | 45 | Grocery | high demand, **heavy** |
| P13 | Wine Bottles | 16 | Beverage | fragile |
| P14 | Paint Cans | 28 | Chemical | hazardous, chemical |
| P15 | Biscuit Boxes | 6 | Snacks | high demand |
| P16 | Motor Oil | 35 | Chemical | hazardous, chemical |
| P17 | Frozen Fish | 20 | Food | temp, high demand, food, Z8-eligible |
| P18 | Bubble Wrap Rolls | 10 | Packaging | fragile |
| P19 | Wheat Sacks | 40 | Grocery | high demand (**not** in `heavy_products`; 40 kg is not >40) |
| P20 | Hand Sanitizer | 8 | Chemical | fragile, chemical (**not** hazardous) |

Total catalog weight = 432 kg. Total zone capacity = 120+80×4+60+150+100 = **750 kg**, so overflow is local, not global.

### Zone capacities

| Zone | Capacity (kg) | Implied policy (from penalties) |
|------|---------------|----------------------------------|
| Z1 | 120 | Heavy items (P4, P12) |
| Z2 | 80 | General |
| Z3 | 80 | All fragile SKUs |
| Z4 | 80 | Temperature-controlled (with Z8) |
| Z5 | 80 | All hazardous SKUs |
| Z6 | 60 | High-demand SKUs (tight) |
| Z7 | 150 | General / overflow |
| Z8 | 100 | Temp + **whitelist only**: Frozen Meat, Yogurt, Frozen Fish |

### Fitness penalties (this code)

| Rule | Penalty | Notes |
|------|---------|--------|
| Zone weight overflow | `2 × excess_kg` | Per overflowing zone. |
| Fragile not in Z3 | +8 each | Six fragile SKUs. |
| Hazardous not in Z5 | +10 each | Five hazardous SKUs. |
| Temp-controlled not in {Z4, Z8} | +9 each | Four frozen/chilled foods. |
| High demand not in Z6 | +5 each | Eight SKUs; Z6 is only 60 kg. |
| Heavy not in Z1 | +4 each | P4 (50 kg), P12 (45 kg) only. |
| Product in Z8 but not on whitelist | +12 each | Ice cream in Z8 is illegal even though it needs temp control. |
| Same category, different zones | +3 **per pair** | Nested `i < j` over all 20 products. Categories with many members (Chemical, Grocery, Food) dominate. |
| Food and chemical **same** zone | +15 **per pair** | Food set is the four chilled foods; chemical set includes sanitizer. |

Fitness uses **named sets**, not the boolean flags on each product dict (`fragile`/`hazardous` on the dict are unused by `fitness` except `weight` and `category`/`name`).

### Genetic operators

**Selection.** `random.sample(population, 5)` then pick min `fitness(...)[0]`. Lower is better (minimization). Default parameter `tournament_size=3` is unused by the main loop.

**Crossover.** `point1 ∈ [1, n-2]`, `point2 ∈ [point1+1, n-1]`. Child1 = `p1[:point1] + p2[point1:point2] + p1[point2:]` (and swapped for child2). Guarantees two distinct interior cuts.

**Mutation.** For each gene, with probability `mutation_rate`, replace with `randint(1, 8)` (may re-assign the same zone).

**Elitism.** After sorting the population ascending by fitness, copy `population[0]` and `population[1]` into the new generation. Fill the rest with tournament → crossover → mutate pairs.

**Tracking.** `best_chromosome` is a **copy** of the best-so-far, updated whenever the current generation’s best improves. Prints `Generation k Best Fitness = …` every generation.

## File-by-file reference

| File | Description |
|------|-------------|
| `i222327_A#02_A.py` | Products, constraints, GA, printing, auto-run. |
| `A2.pdf` | Assignment statement. |
| `i222327_A#02_Report.docx` | Written report. |
| `VIVA.docx` | Viva notes. |

## Data formats

There is no external CSV. Encoding is a Python list of 20 ints. Example genome:

```text
[3, 4, 5, 1, 3, 4, 5, 6, 3, 5, 8, 1, 3, 5, 6, 5, 8, 3, 7, 3]
```

meaning P1→Z3, P2→Z4, …, P20→Z3.

Stdout sections:

```
===== Optimal Storage Plan =====
Z1:
  - P4 - Rice Bags
  Total Weight: 50 kg / 120 kg
...
===== Product Assignments =====
P1 - Glass Bottles -> Z3
...
===== Final Result =====
Best Fitness Score: <int>
Number of Generations Run: <1..900>
===== Remaining Violations =====
1. Z6 exceeds capacity by … -> +…
```

## Tech stack

- Python 3
- `random` only (no NumPy, no DEAP)

## Project structure

```
Genetic_Algorithm/
├── i222327_A#02_A.py
├── A2.pdf
├── i222327_A#02_Report.docx
└── VIVA.docx
```

## Prerequisites and install

Python 3. No third-party packages.

## How to build and run

```bash
cd Genetic_Algorithm
python "i222327_A#02_A.py"
```

Expect ~900 lines of `Generation k Best Fitness = …` then the storage plan. Runtime is seconds to a couple of minutes depending on the machine (each generation sorts 150 chromosomes and each `fitness` is O(n²) pair checks).

## Usage walkthrough

1. Run the script; do not import it from another module unless you want the GA to fire immediately.
2. Watch fitness fall (or plateau). If it hits 0, evolution stops early (`generation_reached` < 900).
3. Read zone loads against capacities; remaining violations list every still-broken rule with its exact `+penalty`.
4. Re-run for another stochastic result (no `random.seed`).

To try other hyperparameters, edit the bottom call:

```python
genetic_algorithm(population_size=150, generations=900, mutation_rate=0.08)
```

## Configuration / constants

| Parameter | Function default | **Actual run** |
|-----------|------------------|----------------|
| `population_size` | 100 | **150** |
| `generations` | 200 | **900** |
| `mutation_rate` | 0.1 (`mutate` default) | **0.08** |
| Tournament size | 3 | **5** |
| Elitism | — | **2** chromosomes |
| Gene alphabet | — | `{1,2,…,8}` |
| Chromosome length | — | `len(products)` = 20 |

Penalty weights: overflow ×2, fragile +8, hazardous +10, temp +9, high-demand +5, heavy +4, illegal Z8 +12, category split +3/pair, food-chemical co-storage +15/pair.

## Results / metrics

The script does not save a CSV of fitness-per-generation. Best fitness is **run-dependent** (unseeded). Because Z6 is 60 kg vs eight high-demand items (sum ≫ 60), high-demand + category-cohesion + temp/fragile/hazardous rules cannot all be satisfied; expect a **positive** best fitness and a non-empty violation list unless the assignment’s intended weights differ.

## Controls / CLI

None. All knobs are function arguments / globals in the `.py` file.

## Known limitations / bugs

- **No random seed** — results are not reproducible.
- **`fitness` ignores product dict flags** and uses parallel sets; P19 (40 kg) is not “heavy”; P20 is chemical+fragile but not hazardous; P6 (ice cream) needs Z4/Z8 but is **not** Z8-eligible, so it is forced toward Z4.
- **Pairwise same-category penalty** grows combinatorially; splitting a 6-item category is expensive even when capacity requires it.
- **Duplicate comment block** above the food/chemical loop (section 4 is pasted twice).
- **`tournament_selection` default 3** disagrees with the call site (5) and with some report text that might cite the default.
- Running as an imported module **starts evolution immediately**.
- Elitism copies references’ `.copy()` of lists but does not re-evaluate uniqueness; two elites can be identical.
- Mutation can produce a gene equal to the old one (wasted mutation).

## How to extend

- `random.seed(42)` for labs/vivas.
- Log `best_fitness` per generation to CSV and plot a convergence curve.
- Repair operators: force hazardous→Z5, fragile→Z3 after crossover instead of only penalizing.
- Weighted sum with normalized terms, or NSGA-II if treating constraints as multiple objectives.
- Wrap the bottom call in `if __name__ == "__main__":`.

## Author

**Mohammad Rohaan** — i222327 · [rohaan2802](https://github.com/rohaan2802)
