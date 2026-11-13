#!/usr/bin/env python3
"""Warehouse storage optimisation with a genetic algorithm.

This is the same algorithm as src/i222327_A02_A.py (the original
assignment file, which was submitted as i222327_A#02_A.py): tournament
selection of size 5, two-point crossover, per-gene mutation, and elitism
of two chromosomes. The fitness function and the nine penalty weights
match that file, and they follow the assignment brief (A2.pdf).

What this script adds is a random seed so a run can be repeated, a log
of best / mean / worst fitness every generation, CSV tables, and optional
plots. The original file is unseeded and prints only a running best.

Default flags (population 150, 900 generations, mutation 0.08, seed 0)
reproduce a best fitness of 82, which is the score in the written report.
The original script has no seed, so a direct run of that file will wander.

Python 3, standard library only, unless you want the plots (matplotlib).
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import sys
import time
from collections import OrderedDict
from pathlib import Path

# ---------------------------------------------------------------------------
# Data — 20 products and eight zones, taken from the assignment brief and
# encoded the same way as the original script.
# ---------------------------------------------------------------------------

PRODUCTS = [
    {"id": "P1",  "name": "P1 - Glass Bottles",      "weight": 20, "category": "Beverage",    "fragile": True,  "hazardous": False, "temp": False, "demand": "Medium"},
    {"id": "P2",  "name": "P2 - Frozen Meat",        "weight": 30, "category": "Food",        "fragile": False, "hazardous": False, "temp": True,  "demand": "High"},
    {"id": "P3",  "name": "P3 - Cleaning Acid",      "weight": 10, "category": "Chemical",    "fragile": False, "hazardous": True,  "temp": False, "demand": "Low"},
    {"id": "P4",  "name": "P4 - Rice Bags",          "weight": 50, "category": "Grocery",     "fragile": False, "hazardous": False, "temp": False, "demand": "High"},
    {"id": "P5",  "name": "P5 - Ceramic Plates",     "weight": 15, "category": "Kitchenware", "fragile": True,  "hazardous": False, "temp": False, "demand": "Medium"},
    {"id": "P6",  "name": "P6 - Ice Cream",          "weight": 25, "category": "Food",        "fragile": False, "hazardous": False, "temp": True,  "demand": "High"},
    {"id": "P7",  "name": "P7 - Detergent",          "weight": 12, "category": "Chemical",    "fragile": False, "hazardous": True,  "temp": False, "demand": "Medium"},
    {"id": "P8",  "name": "P8 - Chips Carton",       "weight": 8,  "category": "Snacks",      "fragile": False, "hazardous": False, "temp": False, "demand": "High"},
    {"id": "P9",  "name": "P9 - Olive Oil Bottles",  "weight": 18, "category": "Grocery",     "fragile": True,  "hazardous": False, "temp": False, "demand": "Medium"},
    {"id": "P10", "name": "P10 - Industrial Bleach", "weight": 22, "category": "Chemical",    "fragile": False, "hazardous": True,  "temp": False, "demand": "Low"},
    {"id": "P11", "name": "P11 - Yogurt Cartons",    "weight": 14, "category": "Food",        "fragile": False, "hazardous": False, "temp": True,  "demand": "High"},
    {"id": "P12", "name": "P12 - Flour Bags",        "weight": 45, "category": "Grocery",     "fragile": False, "hazardous": False, "temp": False, "demand": "High"},
    {"id": "P13", "name": "P13 - Wine Bottles",      "weight": 16, "category": "Beverage",    "fragile": True,  "hazardous": False, "temp": False, "demand": "Medium"},
    {"id": "P14", "name": "P14 - Paint Cans",        "weight": 28, "category": "Chemical",    "fragile": False, "hazardous": True,  "temp": False, "demand": "Low"},
    {"id": "P15", "name": "P15 - Biscuit Boxes",     "weight": 6,  "category": "Snacks",      "fragile": False, "hazardous": False, "temp": False, "demand": "High"},
    {"id": "P16", "name": "P16 - Motor Oil",         "weight": 35, "category": "Chemical",    "fragile": False, "hazardous": True,  "temp": False, "demand": "Low"},
    {"id": "P17", "name": "P17 - Frozen Fish",       "weight": 20, "category": "Food",        "fragile": False, "hazardous": False, "temp": True,  "demand": "High"},
    {"id": "P18", "name": "P18 - Bubble Wrap Rolls", "weight": 10, "category": "Packaging",   "fragile": True,  "hazardous": False, "temp": False, "demand": "Medium"},
    {"id": "P19", "name": "P19 - Wheat Sacks",       "weight": 40, "category": "Grocery",     "fragile": False, "hazardous": False, "temp": False, "demand": "High"},
    {"id": "P20", "name": "P20 - Hand Sanitizer",    "weight": 8,  "category": "Chemical",    "fragile": True,  "hazardous": False, "temp": False, "demand": "Medium"},
]

ZONES = {1: 120, 2: 80, 3: 80, 4: 80, 5: 80, 6: 60, 7: 150, 8: 100}

ZONE_NAMES = {
    1: "Heavy Item Floor Storage",
    2: "Standard Rack Storage",
    3: "Fragile Item Shelf",
    4: "Temperature Controlled Storage",
    5: "Hazardous Material Storage",
    6: "Fast-Moving Product Area (Near Exit)",
    7: "Bulk Dry Storage",
    8: "Refrigerated Loading Dock",
}

# Named sets used by fitness(), identical to the original script. The
# assignment's "affected products" lists are what matter here, not always
# the Demand column: Ice Cream is High in the table but is not on the
# section 5.5 list, so it is not in HIGH_DEMAND. Wheat Sacks are 40 kg
# and heavy items are defined as greater than 40 kg, so they are not heavy.
FRAGILE = {
    "P1 - Glass Bottles", "P5 - Ceramic Plates", "P9 - Olive Oil Bottles",
    "P13 - Wine Bottles", "P18 - Bubble Wrap Rolls", "P20 - Hand Sanitizer",
}
HAZARDOUS = {
    "P3 - Cleaning Acid", "P7 - Detergent", "P10 - Industrial Bleach",
    "P14 - Paint Cans", "P16 - Motor Oil",
}
TEMP = {
    "P2 - Frozen Meat", "P6 - Ice Cream",
    "P11 - Yogurt Cartons", "P17 - Frozen Fish",
}
HIGH_DEMAND = {
    "P2 - Frozen Meat", "P4 - Rice Bags", "P8 - Chips Carton",
    "P11 - Yogurt Cartons", "P12 - Flour Bags", "P15 - Biscuit Boxes",
    "P17 - Frozen Fish", "P19 - Wheat Sacks",
}
HEAVY = {"P4 - Rice Bags", "P12 - Flour Bags"}
FOOD = {
    "P2 - Frozen Meat", "P6 - Ice Cream",
    "P11 - Yogurt Cartons", "P17 - Frozen Fish",
}
CHEMICAL = {
    "P3 - Cleaning Acid", "P7 - Detergent", "P10 - Industrial Bleach",
    "P14 - Paint Cans", "P16 - Motor Oil", "P20 - Hand Sanitizer",
}
ELIGIBLE_Z8 = {
    "P2 - Frozen Meat", "P11 - Yogurt Cartons", "P17 - Frozen Fish",
}

N = len(PRODUCTS)

# Default run — the values in the original file's bottom call, plus a seed
# so this companion script is repeatable. Tournament size 5 is what the
# original actually passes; the function default of 3 is unused.
DEFAULTS = dict(
    population_size=150,
    generations=900,
    mutation_rate=0.08,
    tournament_size=5,
    elite=2,
    seed=0,
)


# ---------------------------------------------------------------------------
# Fitness — same penalties as the original and as section 6 of the brief.
# ---------------------------------------------------------------------------

def fitness(chromosome, collect_violations=True):
    """Return (total_penalty, violations). Lower is better."""
    total = 0
    violations = [] if collect_violations else None

    zone_weights = {z: 0 for z in ZONES}
    for i, zone in enumerate(chromosome):
        zone_weights[zone] += PRODUCTS[i]["weight"]
    for zone, weight in zone_weights.items():
        if weight > ZONES[zone]:
            excess = weight - ZONES[zone]
            penalty = excess * 2
            total += penalty
            if violations is not None:
                violations.append(
                    "Z%d exceeds capacity by %d kg -> +%d" % (zone, excess, penalty)
                )

    for i, zone in enumerate(chromosome):
        name = PRODUCTS[i]["name"]
        if name in FRAGILE and zone != 3:
            total += 8
            if violations is not None:
                violations.append("%s is fragile but not in Z3 -> +8" % name)
        if name in HAZARDOUS and zone != 5:
            total += 10
            if violations is not None:
                violations.append("%s is hazardous but not in Z5 -> +10" % name)
        if name in TEMP and zone not in (4, 8):
            total += 9
            if violations is not None:
                violations.append(
                    "%s needs temperature control but not in Z4/Z8 -> +9" % name
                )
        if name in HIGH_DEMAND and zone != 6:
            total += 5
            if violations is not None:
                violations.append("%s is high demand but not in Z6 -> +5" % name)
        if name in HEAVY and zone != 1:
            total += 4
            if violations is not None:
                violations.append("%s is heavy but not in Z1 -> +4" % name)
        if zone == 8 and name not in ELIGIBLE_Z8:
            total += 12
            if violations is not None:
                violations.append("%s is not allowed in Z8 -> +12" % name)

    for i in range(N):
        for j in range(i + 1, N):
            if PRODUCTS[i]["category"] == PRODUCTS[j]["category"]:
                if chromosome[i] != chromosome[j]:
                    total += 3
                    if violations is not None:
                        violations.append(
                            "%s and %s same category but different zones -> +3"
                            % (PRODUCTS[i]["name"], PRODUCTS[j]["name"])
                        )

    for i in range(N):
        for j in range(i + 1, N):
            n1, n2 = PRODUCTS[i]["name"], PRODUCTS[j]["name"]
            pair = (n1 in FOOD and n2 in CHEMICAL) or (n2 in FOOD and n1 in CHEMICAL)
            if pair and chromosome[i] == chromosome[j]:
                total += 15
                if violations is not None:
                    violations.append(
                        "%s and %s stored together in same zone -> +15" % (n1, n2)
                    )

    return total, (violations or [])


def fitness_score(chromosome):
    """Penalty only — used inside the loop so we don't build strings 150 times a generation."""
    return fitness(chromosome, collect_violations=False)[0]


def penalty_breakdown(chromosome):
    parts = OrderedDict()
    zone_weights = {z: 0 for z in ZONES}
    for i, zone in enumerate(chromosome):
        zone_weights[zone] += PRODUCTS[i]["weight"]
    cap = 0
    for zone, weight in zone_weights.items():
        if weight > ZONES[zone]:
            cap += (weight - ZONES[zone]) * 2
    parts["capacity"] = cap
    parts["fragile"] = sum(8 for i, z in enumerate(chromosome) if PRODUCTS[i]["name"] in FRAGILE and z != 3)
    parts["hazardous"] = sum(10 for i, z in enumerate(chromosome) if PRODUCTS[i]["name"] in HAZARDOUS and z != 5)
    parts["temp"] = sum(9 for i, z in enumerate(chromosome) if PRODUCTS[i]["name"] in TEMP and z not in (4, 8))
    parts["high_demand"] = sum(5 for i, z in enumerate(chromosome) if PRODUCTS[i]["name"] in HIGH_DEMAND and z != 6)
    parts["heavy"] = sum(4 for i, z in enumerate(chromosome) if PRODUCTS[i]["name"] in HEAVY and z != 1)
    parts["illegal_z8"] = sum(
        12 for i, z in enumerate(chromosome)
        if z == 8 and PRODUCTS[i]["name"] not in ELIGIBLE_Z8
    )
    cat = 0
    for i in range(N):
        for j in range(i + 1, N):
            if PRODUCTS[i]["category"] == PRODUCTS[j]["category"] and chromosome[i] != chromosome[j]:
                cat += 3
    parts["category_split"] = cat
    fc = 0
    for i in range(N):
        for j in range(i + 1, N):
            n1, n2 = PRODUCTS[i]["name"], PRODUCTS[j]["name"]
            pair = (n1 in FOOD and n2 in CHEMICAL) or (n2 in FOOD and n1 in CHEMICAL)
            if pair and chromosome[i] == chromosome[j]:
                fc += 15
    parts["food_chemical"] = fc
    parts["total"] = sum(parts.values())
    return parts, zone_weights


# ---------------------------------------------------------------------------
# Operators — same random calls as the original, so a seed is meaningful.
# ---------------------------------------------------------------------------

def create_chromosome():
    return [random.randint(1, 8) for _ in range(N)]


def create_population(population_size):
    return [create_chromosome() for _ in range(population_size)]


def tournament_selection(population, tournament_size=3):
    tournament = random.sample(population, tournament_size)
    best = tournament[0]
    best_fit = fitness_score(best)
    for chromosome in tournament[1:]:
        current = fitness_score(chromosome)
        if current < best_fit:
            best = chromosome
            best_fit = current
    return best


def two_point_crossover(parent1, parent2):
    point1 = random.randint(1, len(parent1) - 2)
    point2 = random.randint(point1 + 1, len(parent1) - 1)
    child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
    return child1, child2


def mutate(chromosome, mutation_rate=0.1):
    new_chromosome = chromosome.copy()
    for i in range(len(new_chromosome)):
        if random.random() < mutation_rate:
            new_chromosome[i] = random.randint(1, 8)
    return new_chromosome


def genetic_algorithm(
    population_size=150,
    generations=900,
    mutation_rate=0.08,
    tournament_size=5,
    elite=2,
    seed=None,
    quiet=False,
):
    if seed is not None:
        random.seed(seed)

    started = time.perf_counter()
    population = create_population(population_size)

    best_chromosome = None
    best_fitness = float("inf")
    first_reached_at = None
    generation_reached = 0
    history = []

    for generation in range(generations):
        scored = [(fitness_score(c), c) for c in population]
        scored.sort(key=lambda row: row[0])
        population = [c for _, c in scored]

        gen_best = scored[0][0]
        gen_mean = sum(s for s, _ in scored) / len(scored)
        gen_worst = scored[-1][0]
        gen_median = scored[len(scored) // 2][0]

        if gen_best < best_fitness:
            best_fitness = gen_best
            best_chromosome = population[0].copy()
            first_reached_at = generation + 1

        generation_reached = generation + 1
        history.append({
            "generation": generation_reached,
            "best_so_far": best_fitness,
            "generation_best": gen_best,
            "generation_mean": gen_mean,
            "generation_median": gen_median,
            "generation_worst": gen_worst,
        })

        if not quiet:
            print("Generation", generation_reached, "Best Fitness =", best_fitness)

        if best_fitness == 0:
            break

        new_population = [population[i].copy() for i in range(elite)]
        while len(new_population) < population_size:
            parent1 = tournament_selection(population, tournament_size=tournament_size)
            parent2 = tournament_selection(population, tournament_size=tournament_size)
            child1, child2 = two_point_crossover(parent1, parent2)
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            new_population.append(child1)
            if len(new_population) < population_size:
                new_population.append(child2)
        population = new_population

    elapsed = time.perf_counter() - started
    final_scores = sorted(fitness_score(c) for c in population)
    return {
        "chromosome": best_chromosome,
        "fitness": best_fitness,
        "violations": fitness(best_chromosome)[1] if best_chromosome is not None else [],
        "generations_run": generation_reached,
        "first_reached_at": first_reached_at,
        "history": history,
        "elapsed": elapsed,
        "seed": seed,
        "final_pop_scores": final_scores,
        "population_size": population_size,
        "generations": generations,
        "mutation_rate": mutation_rate,
        "tournament_size": tournament_size,
        "elite": elite,
    }


# ---------------------------------------------------------------------------
# Printing, tables, plots
# ---------------------------------------------------------------------------

def print_storage_plan(chromosome):
    zone_products = {i: [] for i in range(1, 9)}
    zone_total = {i: 0 for i in range(1, 9)}
    for i, zone in enumerate(chromosome):
        zone_products[zone].append(PRODUCTS[i]["name"])
        zone_total[zone] += PRODUCTS[i]["weight"]
    print("\n===== Optimal Storage Plan =====")
    for zone in range(1, 9):
        print("\nZ%d (%s):" % (zone, ZONE_NAMES[zone]))
        if not zone_products[zone]:
            print("  (empty)")
        else:
            for item in zone_products[zone]:
                print("  -", item)
        print("  Total Weight: %d kg / %d kg" % (zone_total[zone], ZONES[zone]))


def print_product_assignments(chromosome):
    print("\n===== Product Assignments =====")
    for i, zone in enumerate(chromosome):
        print(PRODUCTS[i]["name"], "-> Z" + str(zone))


def _repo_root():
    return Path(__file__).resolve().parent.parent


def write_tables(result, data_dir: Path, results_dir: Path):
    data_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)
    figures = results_dir / "figures"
    figures.mkdir(parents=True, exist_ok=True)

    with (data_dir / "products.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "name", "weight_kg", "category", "fragile", "hazardous",
                    "temp_controlled", "demand", "in_fragile_set", "in_hazardous_set",
                    "in_temp_set", "in_high_demand_set", "in_heavy_set", "z8_eligible"])
        for p in PRODUCTS:
            w.writerow([
                p["id"], p["name"], p["weight"], p["category"],
                "Yes" if p["fragile"] else "No",
                "Yes" if p["hazardous"] else "No",
                "Yes" if p["temp"] else "No",
                p["demand"],
                "Yes" if p["name"] in FRAGILE else "No",
                "Yes" if p["name"] in HAZARDOUS else "No",
                "Yes" if p["name"] in TEMP else "No",
                "Yes" if p["name"] in HIGH_DEMAND else "No",
                "Yes" if p["name"] in HEAVY else "No",
                "Yes" if p["name"] in ELIGIBLE_Z8 else "No",
            ])

    with (data_dir / "zones.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["zone", "name", "capacity_kg"])
        for z in range(1, 9):
            w.writerow(["Z%d" % z, ZONE_NAMES[z], ZONES[z]])

    ch = result["chromosome"]
    parts, zone_weights = penalty_breakdown(ch)

    with (results_dir / "fitness_history.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "generation", "best_so_far", "generation_best",
            "generation_mean", "generation_median", "generation_worst",
        ])
        w.writeheader()
        for row in result["history"]:
            w.writerow({
                **row,
                "generation_mean": "%.6f" % row["generation_mean"],
            })

    with (results_dir / "best_plan.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["zone", "zone_name", "products", "weight_kg", "capacity_kg", "headroom_kg"])
        for z in range(1, 9):
            names = [PRODUCTS[i]["name"] for i, zz in enumerate(ch) if zz == z]
            w.writerow([
                "Z%d" % z, ZONE_NAMES[z],
                "; ".join(names) if names else "(empty)",
                zone_weights[z], ZONES[z], ZONES[z] - zone_weights[z],
            ])

    with (results_dir / "product_assignments.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["product", "weight_kg", "category", "assigned_zone", "flags"])
        for i, z in enumerate(ch):
            flags = []
            n = PRODUCTS[i]["name"]
            if n in FRAGILE: flags.append("fragile")
            if n in HAZARDOUS: flags.append("hazardous")
            if n in TEMP: flags.append("temp")
            if n in HIGH_DEMAND: flags.append("high-demand")
            if n in HEAVY: flags.append("heavy")
            if n in ELIGIBLE_Z8: flags.append("Z8-eligible")
            w.writerow([n, PRODUCTS[i]["weight"], PRODUCTS[i]["category"], "Z%d" % z, ", ".join(flags)])

    with (results_dir / "violations.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["n", "violation"])
        for i, v in enumerate(result["violations"], 1):
            w.writerow([i, v])

    with (results_dir / "penalty_breakdown.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["rule", "penalty"])
        for k, v in parts.items():
            w.writerow([k, v])

    with (results_dir / "zone_loads.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["zone", "zone_name", "weight_kg", "capacity_kg", "utilisation"])
        for z in range(1, 9):
            util = zone_weights[z] / ZONES[z]
            w.writerow(["Z%d" % z, ZONE_NAMES[z], zone_weights[z], ZONES[z], "%.4f" % util])

    with (results_dir / "chromosome.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["gene_index", "product", "zone"])
        for i, z in enumerate(ch):
            w.writerow([i, PRODUCTS[i]["name"], z])

    info = {
        "seed": result["seed"],
        "population_size": result["population_size"],
        "generations_requested": result["generations"],
        "generations_run": result["generations_run"],
        "mutation_rate": result["mutation_rate"],
        "tournament_size": result["tournament_size"],
        "elite": result["elite"],
        "best_fitness": result["fitness"],
        "first_reached_at": result["first_reached_at"],
        "n_violations": len(result["violations"]),
        "chromosome": result["chromosome"],
        "penalty_breakdown": dict(parts),
        "zone_weights": {"Z%d" % z: zone_weights[z] for z in range(1, 9)},
        "initial_best": result["history"][0]["best_so_far"],
        "initial_mean": result["history"][0]["generation_mean"],
        "final_mean": result["history"][-1]["generation_mean"],
        "elapsed_seconds": round(result["elapsed"], 4),
        "python": sys.version.split()[0],
        "note": (
            "Seeded re-run of the original operators. "
            "The assignment file itself has no random.seed; "
            "fitness 82 is also the score in the written report."
        ),
    }
    (results_dir / "run_info.json").write_text(json.dumps(info, indent=2) + "\n")
    return parts, zone_weights, figures


def write_plots(result, parts, zone_weights, figures: Path):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib is not installed; skipping plots. pip install -r requirements.txt", file=sys.stderr)
        return

    gens = [r["generation"] for r in result["history"]]
    best = [r["best_so_far"] for r in result["history"]]
    gbest = [r["generation_best"] for r in result["history"]]
    gmean = [r["generation_mean"] for r in result["history"]]

    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.plot(gens, gmean, color="#9aa3b0", linewidth=1.2, label="generation mean")
    ax.plot(gens, gbest, color="#ffb4a2", linewidth=1.4, label="generation best")
    ax.plot(gens, best, color="#c44536", linewidth=2.4, label="best so far")
    ax.axhline(82, color="#c44536", linestyle="--", linewidth=1, alpha=0.6)
    ax.set_xlabel("Generation", fontsize=13)
    ax.set_ylabel("Fitness  (total penalty, lower is better)", fontsize=13)
    ax.set_title("Fitness over 900 generations  (seed=0, population=150)", fontsize=15)
    ax.legend(fontsize=11, loc="upper right")
    ax.grid(True, alpha=0.35)
    ax.tick_params(labelsize=11)
    ax.set_xlim(1, result["generations_run"])
    fig.tight_layout()
    fig.savefig(figures / "fitness_curve.png", dpi=150)
    plt.close()

    # Zoomed early generations
    cut = 80
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.plot(gens[:cut], gmean[:cut], color="#9aa3b0", linewidth=1.6, label="generation mean")
    ax.plot(gens[:cut], gbest[:cut], color="#ffb4a2", linewidth=1.8, label="generation best")
    ax.plot(gens[:cut], best[:cut], color="#c44536", linewidth=2.6, label="best so far")
    ax.axvline(result["first_reached_at"], color="#1a1514", linestyle=":", linewidth=1.2)
    ax.set_xlabel("Generation", fontsize=13)
    ax.set_ylabel("Fitness  (total penalty, lower is better)", fontsize=13)
    ax.set_title(
        "Early descent: best fitness reaches %d at generation %d"
        % (result["fitness"], result["first_reached_at"]),
        fontsize=15,
    )
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.35)
    ax.tick_params(labelsize=11)
    fig.tight_layout()
    fig.savefig(figures / "fitness_early.png", dpi=150)
    plt.close()

    labels = ["Z%d" % z for z in range(1, 9)]
    weights = [zone_weights[z] for z in range(1, 9)]
    caps = [ZONES[z] for z in range(1, 9)]
    fig, ax = plt.subplots(figsize=(11, 6.5))
    x = range(8)
    ax.bar([i - 0.18 for i in x], caps, width=0.36, color="#d4cbc8", label="capacity")
    ax.bar([i + 0.18 for i in x], weights, width=0.36, color="#c44536", label="assigned weight")
    for i, (w, c) in enumerate(zip(weights, caps)):
        ax.text(i + 0.18, w + 2, "%d" % w, ha="center", va="bottom", fontsize=11)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=13)
    ax.set_ylabel("Kilograms", fontsize=13)
    ax.set_title("Zone loads against capacity  (seed=0, fitness 82)", fontsize=15)
    ax.legend(fontsize=11)
    ax.grid(True, axis="y", alpha=0.35)
    ax.tick_params(labelsize=11)
    fig.tight_layout()
    fig.savefig(figures / "zone_loads.png", dpi=150)
    plt.close()

    # breakdown excluding total
    items = [(k, v) for k, v in parts.items() if k != "total"]
    items.sort(key=lambda kv: kv[1], reverse=True)
    fig, ax = plt.subplots(figsize=(11, 6.5))
    names = [k.replace("_", " ") for k, _ in items]
    vals = [v for _, v in items]
    colors = ["#c44536" if v else "#d4cbc8" for v in vals]
    ax.barh(names[::-1], vals[::-1], color=colors[::-1])
    for i, v in enumerate(vals[::-1]):
        ax.text(v + 0.6, i, str(v), va="center", fontsize=12)
    ax.set_xlabel("Penalty points", fontsize=13)
    ax.set_title("How the fitness of 82 is made up", fontsize=15)
    ax.grid(True, axis="x", alpha=0.35)
    ax.tick_params(labelsize=12)
    fig.tight_layout()
    fig.savefig(figures / "penalty_breakdown.png", dpi=150)
    plt.close()


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Genetic algorithm for the warehouse storage assignment."
    )
    parser.add_argument("--seed", type=int, default=DEFAULTS["seed"],
                        help="random seed (default: 0, the documented re-run)")
    parser.add_argument("--no-seed", action="store_true",
                        help="leave the RNG unseeded, like the original file")
    parser.add_argument("--population", type=int, default=DEFAULTS["population_size"])
    parser.add_argument("--generations", type=int, default=DEFAULTS["generations"])
    parser.add_argument("--mutation-rate", type=float, default=DEFAULTS["mutation_rate"])
    parser.add_argument("--tournament-size", type=int, default=DEFAULTS["tournament_size"])
    parser.add_argument("--data-dir", type=Path, default=None)
    parser.add_argument("--results-dir", type=Path, default=None)
    parser.add_argument("--no-plots", action="store_true")
    parser.add_argument("--quiet", action="store_true",
                        help="do not print a line for every generation")
    args = parser.parse_args(argv)

    root = _repo_root()
    data_dir = args.data_dir or (root / "data")
    results_dir = args.results_dir or (root / "results")
    seed = None if args.no_seed else args.seed

    result = genetic_algorithm(
        population_size=args.population,
        generations=args.generations,
        mutation_rate=args.mutation_rate,
        tournament_size=args.tournament_size,
        seed=seed,
        quiet=args.quiet,
    )

    ch = result["chromosome"]
    if ch is not None:
        print_storage_plan(ch)
        print_product_assignments(ch)
        print("\n===== Final Result =====")
        print("Best Fitness Score:", result["fitness"])
        print("Number of Generations Run:", result["generations_run"])
        print("First reached at generation:", result["first_reached_at"])
        if seed is not None:
            print("Random seed:", seed)
        print("\n===== Penalty breakdown =====")
        parts, zone_weights = penalty_breakdown(ch)
        for k, v in parts.items():
            print("  %s: %s" % (k, v))
        print("\n===== Remaining Violations =====")
        if not result["violations"]:
            print("No violations. Perfect solution found.")
        else:
            for i, v in enumerate(result["violations"], 1):
                print("%d. %s" % (i, v))
    else:
        print("No solution found.")
        return 1

    parts, zone_weights, figures = write_tables(result, data_dir, results_dir)
    if not args.no_plots:
        write_plots(result, parts, zone_weights, figures)
    print("\nWrote tables under %s and %s" % (data_dir, results_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
