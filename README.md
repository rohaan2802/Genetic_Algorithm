<div align="center">

# Warehouse storage with a genetic algorithm

**A genetic algorithm that places twenty products into eight warehouse zones under nine storage constraints.**

[![Python](https://img.shields.io/badge/Python-3-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://github.com/rohaan2802/Genetic_Algorithm)
[![Stdlib](https://img.shields.io/badge/Algorithm-Python%20stdlib-informational?style=for-the-badge)](https://github.com/rohaan2802/Genetic_Algorithm/blob/main/src/i222327_A02_A.py)
[![matplotlib](https://img.shields.io/badge/Plots-matplotlib-11557C?style=for-the-badge)](https://github.com/rohaan2802/Genetic_Algorithm/blob/main/requirements.txt)
[![Website](https://img.shields.io/badge/Website-GitHub%20Pages-222222?style=for-the-badge&logo=github&logoColor=white)](https://rohaan2802.github.io/Genetic_Algorithm/)
[![Last commit](https://img.shields.io/github/last-commit/rohaan2802/Genetic_Algorithm?style=for-the-badge)](https://github.com/rohaan2802/Genetic_Algorithm/commits/main)
[![Repo Size](https://img.shields.io/github/repo-size/rohaan2802/Genetic_Algorithm?style=for-the-badge)](https://github.com/rohaan2802/Genetic_Algorithm)
[![Stars](https://img.shields.io/github/stars/rohaan2802/Genetic_Algorithm?style=for-the-badge)](https://github.com/rohaan2802/Genetic_Algorithm/stargazers)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**Mohammad Rohaan** · 22I-2327

</div>

---

I used a genetic algorithm to place twenty products into eight warehouse zones, under the constraints from Assignment 2. The fitness function is a penalty total: lower is better, and zero would mean every rule is satisfied. In the written report, and again on a seeded re-run that uses the same operators, the best score is **82**. That is not a perfect plan. Several of the rules pull the same product toward different zones, so the search is really about the cheapest combination of leftover penalties.

## Live Links

| What | Link |
| --- | --- |
| Repository | [https://github.com/rohaan2802/Genetic_Algorithm](https://github.com/rohaan2802/Genetic_Algorithm) |
| Website | [https://rohaan2802.github.io/Genetic_Algorithm/](https://rohaan2802.github.io/Genetic_Algorithm/) |
| Download ZIP | [https://github.com/rohaan2802/Genetic_Algorithm/archive/refs/heads/main.zip](https://github.com/rohaan2802/Genetic_Algorithm/archive/refs/heads/main.zip) |

## Contents

1. [Overview](#overview)
2. [What's inside](#whats-inside)
3. [The data](#the-data)
4. [Constraints and penalties](#constraints-and-penalties)
5. [Why the score does not reach zero](#why-the-score-does-not-reach-zero)
6. [How the algorithm is built](#how-the-algorithm-is-built)
7. [Results](#results)
8. [Twelve seeded runs](#twelve-seeded-runs)
9. [Folder structure](#folder-structure)
10. [How to use](#how-to-use)
11. [Running the search](#running-the-search)
12. [Screenshots](#screenshots)
13. [License](#license)
14. [Author](#author)

## Overview

The brief is *Assignment 2: Warehouse Storage Optimization Using Genetic Algorithm*. Twenty named products, with a weight, a category, and flags for fragile, hazardous, temperature-controlled and demand, have to be assigned to eight zones. Each zone has a weight capacity. Nine kinds of violation add to a penalty score, and the genetic algorithm tries to bring that score down.

I submitted a single Python 3 file, a short written report, and viva notes. The file uses only the standard library (`random`). Tournament selection of size 5, two-point crossover, per-gene mutation at rate 0.08, and elitism of two chromosomes run for up to 900 generations on a population of 150. The report records a best fitness of 82. The original file has no `random.seed`, so a fresh run of that file will not land on the same chromosome every time. The companion script in this repository, `src/warehouse_ga.py`, uses the same operators and, with `--seed 0` (the default), reaches 82 at generation 45 and keeps it through generation 900. That is the plan the tables and screenshots describe.

## What's inside

- The original assignment file, kept byte-for-byte, under a slightly quieter name: `src/i222327_A02_A.py` (submitted as `i222327_A#02_A.py`). Running it starts the search immediately; there is no `if __name__` guard, and no seed.
- A companion script, `src/warehouse_ga.py`, with the same fitness function and the same operators, plus a seed, a per-generation log, CSV output, and optional plots. Matplotlib is only needed for the figures.
- The 20-product table and the eight zones as CSV, copied from the brief and from the original file (`data/`).
- The assignment PDF, the written report, and the viva questions (`docs/`).
- Results from the seed-0 run: the best plan, the twenty leftover violations, the penalty breakdown, fitness against generation, and zone loads (`results/`).
- A GitHub Pages site for the same material, and 24 screenshots of the data, the code, the charts and the site.

## The data

These are the twenty products from section 4 of the brief, used as-is. The genetic algorithm does not read a file; the same records are hard-coded in both Python scripts.

| Product | Weight | Category | Fragile | Hazardous | Temp | Demand |
| --- | ---: | --- | --- | --- | --- | --- |
| P1 – Glass Bottles | 20 kg | Beverage | Yes | No | No | Medium |
| P2 – Frozen Meat | 30 kg | Food | No | No | Yes | High |
| P3 – Cleaning Acid | 10 kg | Chemical | No | Yes | No | Low |
| P4 – Rice Bags | 50 kg | Grocery | No | No | No | High |
| P5 – Ceramic Plates | 15 kg | Kitchenware | Yes | No | No | Medium |
| P6 – Ice Cream | 25 kg | Food | No | No | Yes | High |
| P7 – Detergent | 12 kg | Chemical | No | Yes | No | Medium |
| P8 – Chips Carton | 8 kg | Snacks | No | No | No | High |
| P9 – Olive Oil Bottles | 18 kg | Grocery | Yes | No | No | Medium |
| P10 – Industrial Bleach | 22 kg | Chemical | No | Yes | No | Low |
| P11 – Yogurt Cartons | 14 kg | Food | No | No | Yes | High |
| P12 – Flour Bags | 45 kg | Grocery | No | No | No | High |
| P13 – Wine Bottles | 16 kg | Beverage | Yes | No | No | Medium |
| P14 – Paint Cans | 28 kg | Chemical | No | Yes | No | Low |
| P15 – Biscuit Boxes | 6 kg | Snacks | No | No | No | High |
| P16 – Motor Oil | 35 kg | Chemical | No | Yes | No | Low |
| P17 – Frozen Fish | 20 kg | Food | No | No | Yes | High |
| P18 – Bubble Wrap Rolls | 10 kg | Packaging | Yes | No | No | Medium |
| P19 – Wheat Sacks | 40 kg | Grocery | No | No | No | High |
| P20 – Hand Sanitizer | 8 kg | Chemical | Yes | No | No | Medium |

The eight zones, from section 3:

| Zone | Description | Capacity |
| --- | --- | ---: |
| Z1 | Heavy Item Floor Storage | 120 kg |
| Z2 | Standard Rack Storage | 80 kg |
| Z3 | Fragile Item Shelf | 80 kg |
| Z4 | Temperature Controlled Storage | 80 kg |
| Z5 | Hazardous Material Storage | 80 kg |
| Z6 | Fast-Moving Product Area (Near Exit) | 60 kg |
| Z7 | Bulk Dry Storage | 150 kg |
| Z8 | Refrigerated Loading Dock | 100 kg |

Two small mismatches between the table columns and the “affected products” lists are worth knowing, because the fitness function follows the lists, just as the original file does:

- Ice Cream is High in the Demand column, but it is not on the section 5.5 list, so sitting outside Z6 does not cost it a high-demand penalty.
- Wheat Sacks weigh 40 kg. Heavy items are “heavier than 40 kg”, so only Rice Bags (50) and Flour Bags (45) pick up the heavy-item penalty.

Hand Sanitizer is fragile and chemical, but not hazardous. It is pulled toward Z3 by one rule and toward the other chemicals in Z5 by another.

## Constraints and penalties

These are the nine rules from section 6, with the same weights the code uses.

| Violation | Penalty |
| --- | --- |
| Zone weight over the cap | +2 per extra kilogram |
| Fragile item not in Z3 | +8 per product |
| Hazardous item not in Z5 | +10 per product |
| Temperature-controlled item not in Z4 or Z8 | +9 per product |
| High-demand item not in Z6 | +5 per product |
| Heavy item (over 40 kg) not in Z1 | +4 per product |
| Same-category products in different zones | +3 per separated pair |
| A food item and a chemical item in the same zone | +15 per pair |
| A product in Z8 that is not on the loading-dock whitelist | +12 per product |

Z8 is only for products that are both temperature-controlled and high-demand: Frozen Meat, Yogurt Cartons, and Frozen Fish. Ice Cream needs refrigeration, but it is not on that whitelist, so Z8 would cost it +12; Z4 is the legal cold shelf. The brief also says a product can be charged independently for more than one rule — a frozen high-demand item in Z8, for example, still pays +5 for not being in Z6.

The fitness function in the original file walks named sets (`fragile_products`, `hazardous_products`, and so on), not the boolean flags on each product dict, except for `weight`, `category` and `name`. The companion script does the same.

## Why the score does not reach zero

The viva notes put this clearly, and the numbers back it up. Some rules cannot all be true at once.

The six fragile items weigh 87 kg; Z3 holds 80 kg. Putting all six on that shelf costs +14 for the overflow. Leaving the lightest one off costs +8, which is cheaper, and that is what the 82-point plan does (Hand Sanitizer goes to Z5).

The five hazardous items weigh 107 kg; Z5 holds 80 kg. Parking all five there would cost +54. Taking Motor Oil (35 kg) out costs +10, and the remaining four, plus Hand Sanitizer at 8 kg, fill Z5 to the kilogram.

Eight high-demand items weigh 213 kg together, and Z6 holds 60 kg. Five of those eight also have to satisfy a colder or a heavier rule: Frozen Meat, Yogurt and Frozen Fish want Z4 or Z8, Rice and Flour want Z1. The cheaper choice for those five is to pay the +5 high-demand penalty rather than the +9 temperature or (for both heavies in Z6) a capacity problem. That is already +25, before anything else.

Category cohesion then adds more. Grocery is split across Z1, Z3 and Z6 because Olive Oil is fragile, Rice and Flour are heavy, and Wheat is the high-demand sack that actually fits near the exit. Food is split because Ice Cream has to stay in Z4 while the three whitelist items can sit together in Z8. Chemical is split because Motor Oil no longer fits in Z5. Those 13 separated pairs are +39.

None of that is a bug in the search. It is what the penalty table does when the rules disagree. The algorithm’s job is to pick the cheaper leftovers.

## How the algorithm is built

A chromosome is a list of twenty integers, one zone per product, in order P1 to P20. The report’s example `[3, 8, 5, 1, 3, 4, 5, 6, 3, 5, 8, 1, 3, 5, 6, 7, 8, 3, 6, 5]` is, as it happens, also the best chromosome from the seed-0 re-run: P1 in Z3, P2 in Z8, P3 in Z5, and so on.

The initial population is 150 random chromosomes, each gene a uniform `randint(1, 8)`. I used tournament selection of size 5: five chromosomes are drawn, and the one with the lowest penalty is the parent. The report prefers this over roulette-wheel or rank selection because it is simple and it already treats lower fitness as better, with no probability weights to build. The function’s default argument is 3; the actual call passes 5.

Two-point crossover cuts at `point1` in `[1, n-2]` and `point2` in `[point1+1, n-1]`, so the two cuts are distinct and interior. Each child takes the middle segment from one parent and the two outer segments from the other.

Mutation walks every gene and, with probability 0.08, replaces it with a fresh `randint(1, 8)`, which can be the same zone. The viva notes keep the rate low so good plans are not undone at random.

After each generation is sorted, the two best chromosomes are copied unchanged into the next population (elitism). The rest is filled with tournament, crossover and mutation. The loop stops at 900 generations, or earlier if a fitness of 0 appears. In every run I have done, it uses the full 900.

The original file prints `Generation k Best Fitness = …` on every generation and then the plan, the assignments, the score, and the remaining violations. The companion script prints the same sections, then a penalty breakdown, and writes the CSVs.

Parameters actually used, against the function defaults:

| Parameter | Function default | This run |
| --- | ---: | ---: |
| Population | 100 | **150** |
| Generations | 200 | **900** |
| Mutation rate | 0.1 | **0.08** |
| Tournament size | 3 | **5** |
| Elitism | — | **2** chromosomes |
| Random seed | none | **0** in the companion script (the original file is unseeded) |

## Results

These figures are from `src/warehouse_ga.py --seed 0`, which is the default. The operators match the original file. The written report also gives a best fitness of 82; this re-run reaches that score at generation 45 and holds it.

**Best fitness: 82**, after 900 generations. The first generation’s best was 247, with a mean of 384.2. The curve drops quickly through the first thirty-odd generations (91 by generation 31, 87 by 43) and hits 82 at generation 45. After that the best does not move. The population mean at the end is still around 124 — mutation keeps stirring the rest of the population, and elitism is what holds on to 82.

The 82 points break down as follows. There is no overflow and no food-chemical clash.

| Rule | Penalty | What it is in this plan |
| --- | ---: | --- |
| Capacity overflow | 0 | Every zone is at or under its cap |
| Fragile, not in Z3 | 8 | Hand Sanitizer is in Z5 |
| Hazardous, not in Z5 | 10 | Motor Oil is in Z7 |
| Temperature, not in Z4/Z8 | 0 | All four cold items are on a cold shelf |
| High demand, not in Z6 | 25 | Five conflicting items, +5 each |
| Heavy, not in Z1 | 0 | Rice and Flour are on the floor |
| Illegal Z8 | 0 | Only the three whitelist items are on the dock |
| Same-category split | 39 | Thirteen pairs, listed below |
| Food and chemical together | 0 | Food and chemicals do not share a zone |
| **Total** | **82** | |

The storage plan:

| Zone | Products | Weight / cap |
| --- | --- | ---: |
| Z1 Heavy Item Floor Storage | Rice Bags, Flour Bags | 95 / 120 kg |
| Z2 Standard Rack Storage | *(empty)* | 0 / 80 kg |
| Z3 Fragile Item Shelf | Glass Bottles, Ceramic Plates, Olive Oil Bottles, Wine Bottles, Bubble Wrap Rolls | 79 / 80 kg |
| Z4 Temperature Controlled Storage | Ice Cream | 25 / 80 kg |
| Z5 Hazardous Material Storage | Cleaning Acid, Detergent, Industrial Bleach, Paint Cans, Hand Sanitizer | 80 / 80 kg |
| Z6 Fast-Moving Product Area | Chips Carton, Biscuit Boxes, Wheat Sacks | 54 / 60 kg |
| Z7 Bulk Dry Storage | Motor Oil | 35 / 150 kg |
| Z8 Refrigerated Loading Dock | Frozen Meat, Yogurt Cartons, Frozen Fish | 64 / 100 kg |

The chromosome is `[3, 8, 5, 1, 3, 4, 5, 6, 3, 5, 8, 1, 3, 5, 6, 7, 8, 3, 6, 5]`.

Twenty violations remain. The first seven are the product-level ones (five high-demand misses, Motor Oil out of Z5, Hand Sanitizer out of Z3). The other thirteen are the category splits: three Food pairs around Ice Cream in Z4 versus the three items in Z8; five Chemical pairs around Motor Oil in Z7; five Grocery pairs around Olive Oil in Z3, Rice and Flour in Z1, and Wheat in Z6. Beverages (Glass and Wine) both sit in Z3, and both snacks sit in Z6, so those categories are together.

I would not read this as “the” unique optimum. It is a strong plan that the report found, that seed 0 finds, and that several other seeds find as well. I have not proved that nothing under 82 exists.

## Twelve seeded runs

The original file is unseeded. To see how stable 82 is, I ran the same operators twelve times with seeds `0, 1, 7, 13, 21, 42, 99, 123, 2026, 2327, 4090, 9001`. Seven of the twelve finished at 82, five at 88. The mean was 84.5, the median 82. No run in that set beat 82, and every 82-point run used the same leftover-penalty mix (0 overflow, +8 fragile, +10 hazardous, +25 high-demand, +39 category, nothing else). The chromosomes differ only in where Motor Oil sits (Z7 or Z2 — both isolated, same split cost) and, in one case, in whether the three whitelist foods share Z8 or sit with Ice Cream’s side of Z4. Seed 0’s plan is the most common of the 82s.

Those twelve runs are in `results/seeded_runs.csv`. They are an extra check, not something the original assignment file prints.

## Folder structure

```
Genetic_Algorithm/
├── LICENSE
├── README.md
├── index.html                  GitHub Pages site
├── requirements.txt            matplotlib, for the plots only
├── assets/                     site CSS, JS, favicon
├── data/
│   ├── products.csv
│   ├── zones.csv
│   └── README.md
├── docs/
│   ├── assignment/A2-Warehouse-Storage-Optimization-Using-Genetic-Algorithm.pdf
│   ├── i222327_A02_Report.docx
│   └── VIVA.docx
├── src/
│   ├── i222327_A02_A.py        original file, exact bytes (was i222327_A#02_A.py)
│   └── warehouse_ga.py         same algorithm, seed, CSVs, plots
├── results/
│   ├── fitness_history.csv
│   ├── best_plan.csv
│   ├── product_assignments.csv
│   ├── violations.csv
│   ├── penalty_breakdown.csv
│   ├── zone_loads.csv
│   ├── chromosome.csv
│   ├── seeded_runs.csv
│   ├── run_info.json
│   └── figures/
└── screenshots/                24 × 1600×1000
```

The original PDF was named `A2.pdf`. The original report was `i222327_A#02_Report.docx`. Both are the same files, with quieter names.

## How to use

Python 3. The original file needs nothing else. The companion script needs matplotlib only if you want the figures.

**Linux / macOS**

```bash
git clone https://github.com/rohaan2802/Genetic_Algorithm.git
cd Genetic_Algorithm
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 src/warehouse_ga.py
```

**Windows**

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python src\warehouse_ga.py
```

To run the original assignment file instead (unseeded, 900 printed generations, no CSV):

```bash
python3 src/i222327_A02_A.py
```

## Running the search

The default companion call is population 150, 900 generations, mutation 0.08, tournament 5, seed 0. It prints the running best, the final plan, the twenty violations, and the penalty breakdown, and it writes the files under `results/`. Useful flags:

```bash
python3 src/warehouse_ga.py --seed 21
python3 src/warehouse_ga.py --no-seed
python3 src/warehouse_ga.py --population 150 --generations 900 --mutation-rate 0.08
python3 src/warehouse_ga.py --no-plots --quiet
python3 src/warehouse_ga.py --data-dir data --results-dir results
```

`--quiet` skips the 900 generation lines and still prints the plan. `--no-seed` leaves the RNG alone, which is how the original file behaves. `--no-plots` is enough if you do not want to install matplotlib; the CSVs are still written.

On this machine a seeded run takes a few seconds. The original file is slower to watch only because it prints a line on every generation and rebuilds the violation list inside every fitness call.

## Screenshots

All 24 images are 1600×1000.

### 1. Repository folder structure

[![Repository folder structure](screenshots/01-repo-structure.png)](screenshots/01-repo-structure.png)

The original file, the companion script, the brief, the results and the site.

### 2. The problem

[![The problem](screenshots/02-problem.png)](screenshots/02-problem.png)

Twenty products, eight zones, nine penalty rules, a minimising genetic algorithm.

### 3. The product table

[![The product table](screenshots/03-products-table.png)](screenshots/03-products-table.png)

All twenty products, every column from the brief.

### 4. The eight zones

[![The eight zones](screenshots/04-zones.png)](screenshots/04-zones.png)

Capacities and what each zone is for, including the Z8 whitelist.

### 5. Penalty weights

[![Penalty weights](screenshots/05-penalties.png)](screenshots/05-penalties.png)

The nine rules and the points they add, as the code applies them.

### 6. Why zero is out of reach

[![Conflicting constraints](screenshots/06-conflicts.png)](screenshots/06-conflicts.png)

Fragile weight versus Z3, hazardous weight versus Z5, and the high-demand pile versus Z6.

### 7. Chromosome representation

[![Chromosome representation](screenshots/07-chromosome.png)](screenshots/07-chromosome.png)

Twenty genes, the seed-0 chromosome, and how it maps onto products.

### 8. The fitness function

[![The fitness function, source code](screenshots/08-fitness-code.png)](screenshots/08-fitness-code.png)

The real penalty code from the original file.

### 9. Selection, crossover, mutation, elitism

[![Genetic operators, source code](screenshots/09-operators-code.png)](screenshots/09-operators-code.png)

The operators as they are written, including the call that passes tournament size 5.

### 10. Parameters

[![Parameters](screenshots/10-parameters.png)](screenshots/10-parameters.png)

Population, generations, mutation, tournament size, elitism, and the seed.

### 11. Fitness over 900 generations

[![Fitness curve](screenshots/11-fitness-curve.png)](screenshots/11-fitness-curve.png)

Best-so-far, generation best, and generation mean, seed 0.

### 12. The early descent

[![Early descent](screenshots/12-early-descent.png)](screenshots/12-early-descent.png)

The same curve through generation 80, with the step down to 82 at generation 45.

### 13. The best storage plan

[![Best storage plan](screenshots/13-best-plan.png)](screenshots/13-best-plan.png)

Zone by zone, with weights against capacity.

### 14. Product assignments

[![Product assignments](screenshots/14-product-assignments.png)](screenshots/14-product-assignments.png)

All twenty products and the zone each one landed in.

### 15. Zone loads

[![Zone loads](screenshots/15-zone-loads.png)](screenshots/15-zone-loads.png)

Assigned kilograms against each cap. Z2 is empty; Z5 is filled to 80.

### 16. Remaining violations

[![Remaining violations](screenshots/16-violations.png)](screenshots/16-violations.png)

All twenty leftover penalties that add up to 82.

### 17. How the 82 is made up

[![Penalty breakdown](screenshots/17-penalty-breakdown.png)](screenshots/17-penalty-breakdown.png)

The nine rules, the points on this plan, and which ones are zero.

### 18. The thirteen category splits

[![Category splits](screenshots/18-category-splits.png)](screenshots/18-category-splits.png)

Every same-category pair that sits in two different zones.

### 19. Twelve seeds

[![Twelve seeded runs](screenshots/19-seeded-runs.png)](screenshots/19-seeded-runs.png)

Seven runs at 82, five at 88. None in this set came in under 82.

### 20. Website, dark theme

[![Website home, dark theme](screenshots/20-website-home-dark.png)](screenshots/20-website-home-dark.png)

The graphite-and-coral Pages site, dark theme.

### 21. Website, light theme

[![Website home, light theme](screenshots/21-website-home-light.png)](screenshots/21-website-home-light.png)

The same page in the chalk light theme.

### 22. Website on a phone

[![Website on a phone](screenshots/22-website-phone.png)](screenshots/22-website-phone.png)

The mobile layout, hamburger menu and stats.

### 23. Website · results

[![Website results](screenshots/23-website-results.png)](screenshots/23-website-results.png)

The breakdown, the plan and the leftover violations on the site.

### 24. Website · how to run

[![Website how to run](screenshots/24-website-how-to-run.png)](screenshots/24-website-how-to-run.png)

A virtualenv, the companion script, and the original file.

## License

The code in this repository is under the [MIT License](LICENSE), Copyright (c) 2026 Mohammad Rohaan.

## Author

**Mohammad Rohaan** — 22I-2327 · [rohaan2802](https://github.com/rohaan2802)
