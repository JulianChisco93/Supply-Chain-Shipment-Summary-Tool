# Supply Chain Shipment Summary Tool

A Python tool for summarizing and analyzing supply chain shipment data. Built as part of **Assignment 2: Agile Software Development** — a one-week collaborative sprint using GitHub and Taiga.

## Project Overview

This project processes the `supply_delivery_history.csv` dataset to produce simple, meaningful summaries and insights about health commodity shipments (ARVs, HIV rapid test kits, and related products). Each row in the dataset represents one shipped line item, including destination country, vendor, product group, shipment mode, delivery dates, quantity, value, freight cost, weight, and insurance.

The codebase provides modular, reusable Python functions that return ready-to-use results (data objects or plot objects) for potential use in dashboards or visualization tools later.

## Sprint Goal

Develop a functional Python-based Supply Chain Shipment Summary Tool that can load, clean, and summarize the dataset, while demonstrating Agile collaboration through GitHub workflows and Taiga tracking.

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
├── data/
│   ├── supply_delivery_history.csv
│   └── supply_delivery_history_clean.csv
├── src/
│   ├── cleaning.py
│   ├── country_analysis.py
│   ├── product_analysis.py
│   ├── vendor_analysis.py
│   └── shipment_summary.py
├── main.py
└── .gitignore
```

## Requirements

- Python 3.10+
- pandas
- matplotlib (optional, for plot functions)
- seaborn

Install dependencies:

```bash
pip install pandas matplotlib seaborn
```

## How to Run

Run the complete workflow:
```bash
python main.py
```
The application will:

1. Load the raw shipment dataset
2. Clean and standardize the data
3. Save a cleaned version of the dataset
4. Generate country-level analyses
5. Generate product-level analyses
6. Generate vendor-level analyses
7. Generate shipment summary reports
8. Display visualizations

## Collaboration Workflow

- **Branch-per-feature:** Each user story is developed on its own branch.
- **Pull requests:** All changes are merged via PRs with peer review.
- **Traceability:** Commits and PRs reference Taiga user story IDs (e.g. `US-01`).
- **Taiga:** Sprint backlog and task tracking on our private Taiga board.

## User Stories

| ID | Story | Points | Status |
|----|-------|--------|--------|
| US-01 | _As a user, I want the supply delivery history dataset to be cleaned and standardized, so that I can perform reliable analysis without issues caused by inconsistent dates, mixed data types, missing values, duplicate formatting, or messy categorical labels._ | _3_ | Closed |
| US-02 | _As a supply chain analyst, I want to analyze shipment data by country so that I can compare shipment volume and value across destinations and identify key distribution trends._ | _5_ | Closed  |
| US-03 | _As a supply chain analyst, I want to analyze shipment activity by product group, product category, and item type so that I can identify the most shipped products, understand product demand patterns, and evaluate the overall value of shipped commodities._ | _3_ | Closed  |
| US-04 | _As a vendor relationship manager, I want to view shipment activity by vendor so that I can identify which vendors handle the highest shipment volume and generate the highest shipment value._ | _5_ | Closed  |
| US-05 | _As a Supply Chain Manager, I want to run all shipment analysis modules from one main workflow so that I can review the complete supply chain summary in a single execution._ | _3_ | Closed  |
| US-06 | _As a Supply Chain Manager, I want to run all shipment analysis modules from one main workflow so that I can review the complete supply chain summary in a single execution._ | _3_ | Closed  |

## License

Academic project — University of New Brunswick (Data Analytics / Agile Software Development).
