# Supply Chain Shipment Summary Tool

A Python tool for summarizing and analyzing supply chain shipment data. Built as part of **Assignment 2: Agile Software Development** — a one-week collaborative sprint using GitHub and Taiga.

## Project Overview

This project processes the `supply_delivery_history.csv` dataset to produce simple, meaningful summaries and insights about health commodity shipments (ARVs, HIV rapid test kits, and related products). Each row in the dataset represents one shipped line item, including destination country, vendor, product group, shipment mode, delivery dates, quantity, value, freight cost, weight, and insurance.

The codebase provides modular, reusable Python functions that return ready-to-use results (data objects or plot objects) for potential use in dashboards or visualization tools later.

## Sprint Goal

> _Update this section with your team's sprint goal after Sprint Planning (Step 3)._

Example: *"Deliver a working Python module that loads, cleans, and summarizes the supply delivery dataset with shipment, country, vendor, and product group reports."*

## Team

| Name | Role / Responsibilities |
|------|-------------------------|
| _Team member 1_ | _e.g. Data loading & cleaning_ |
| _Team member 2_ | _e.g. Summary functions_ |
| _Team member 3_ | _e.g. Tests & documentation_ |

## Dataset

- **File:** `supply_delivery_history.csv`
- **Description:** Shipment line-item level data for health commodities across multiple countries and vendors.
- **Note:** Some fields may contain missing values, inconsistent date formats, or non-numeric text in cost and weight columns. Data cleaning is expected before analysis.

## Project Structure

```
.
├── README.md
├── supply_delivery_history.csv
├── .gitignore
└── src/                    # Python source code (to be added during sprint)
    └── ...
```

## Requirements

- Python 3.10+
- pandas
- matplotlib (optional, for plot functions)

Install dependencies:

```bash
pip install pandas matplotlib
```

## How to Run

> _Update these instructions as your tool is built during the sprint._

```bash
# Example (once code is in place):
python -m src.main
```

Or import functions directly:

```python
# Example (once modules are in place):
# from src.summaries import get_country_summary
# summary = get_country_summary("supply_delivery_history.csv")
# print(summary)
```

## Collaboration Workflow

- **Branch-per-feature:** Each user story is developed on its own branch.
- **Pull requests:** All changes are merged via PRs with peer review.
- **Traceability:** Commits and PRs reference Taiga user story IDs (e.g. `US-01`).
- **Taiga:** Sprint backlog and task tracking on our private Taiga board.

## User Stories

> _Add your sprint user stories here after Step 3 planning._

| ID | Story | Points | Status |
|----|-------|--------|--------|
| US-01 | _As a ..., I want ..., so that ..._ | _?_ | Backlog |
| US-02 | | | |
| US-03 | | | |
| US-04 | | | |
| US-05 | | | |

## License

Academic project — University of New Brunswick (Data Analytics / Agile Software Development).
