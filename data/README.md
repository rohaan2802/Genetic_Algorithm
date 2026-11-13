# Data

The twenty products and eight warehouse zones come from the assignment brief (`docs/assignment/A2-Warehouse-Storage-Optimization-Using-Genetic-Algorithm.pdf`, originally `A2.pdf`) and are hard-coded the same way in `src/i222327_A02_A.py`. There is no external or purchased dataset.

`products.csv` is that table, plus columns that record which named sets the original fitness function uses. Those sets follow the “affected products” lists in the brief, which is not always the same as the column flags:

- Ice Cream is marked High demand in the product table, but it is not on the section 5.5 high-demand list, and the code does not penalise it for sitting outside Z6.
- Wheat Sacks weigh 40 kg. Heavy items are defined as greater than 40 kg, so they are not in the heavy set.
- Hand Sanitizer is fragile and chemical, but not hazardous, so it is pushed toward Z3 by one rule and toward the other chemicals (Z5) by another.

`zones.csv` is the eight zones and their capacities from section 3 of the brief.

The genetic algorithm does not read these CSVs — they are here so the table is easy to inspect. The script that writes them is `src/warehouse_ga.py`.
