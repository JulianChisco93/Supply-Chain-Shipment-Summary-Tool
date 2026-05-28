# Supply Chain Shipment Summary Tool

A Python-based data analysis tool developed for **Assignment 2: Agile Software Development** in the Master of Data Analytics program at the **University of Niagara Falls Canada**.

This project analyzes a healthcare supply chain shipment dataset and provides modular summaries related to shipment activity, countries, products, vendors, and data quality.


## Project Overview

The project uses the `supply_delivery_history.csv` dataset, which contains shipment line-item records for healthcare commodities such as ARVs, HIV test kits, and related medical products. Each row in the dataset represents one shipped line item, including destination country, vendor, product group, shipment mode, delivery dates, quantity, value, freight cost, weight, and insurance.

The codebase provides modular, reusable Python functions that loads, cleans, and analyzes the dataset to generate meaningful insights for supply chain stakeholders, including shipment volume, shipment value, vendor performance, country distribution, and product-level activity.


## Sprint Goal

Develop a functional Python tool that can clean, summarize, and analyze Supply Chain Shipment data using Agile collaboration through GitHub, Taiga, user stories, branches, commits, pull requests, and peer review.


## Team

| Team Member | Role / Responsibilities |
|---|---|
| Chisco Henao, Julian David | Data Loading & Cleaning, and Shipping Analysis |
| Sierra Garzon, Cesar | Country Analysis & Test |
| Leon Granados, Daniela | Product Analysis & Test |
| Cuenca Bejar, Jorge Henry | Vendor Analysis and Documentation |


## Dataset

- **File:** `supply_delivery_history.csv`
- **Description:** Shipment line-item level data for health commodities across multiple countries and vendors.
- **Note:** Some fields may contain missing values, inconsistent date formats, or non-numeric text in cost and weight columns. Data cleaning is expected before analysis.


## Main Features

- Load raw and cleaned shipment datasets.
- Clean inconsistent dates, numeric fields, missing values, and categorical values.
- Generate shipment-level summaries.
- Analyze shipment activity by country.
- Analyze shipment activity by product group and product description.
- Analyze vendor performance by shipment quantity and shipment value.
- Generate charts and visual summaries using Python.
- Integrate all analysis modules through the main workflow.


## Project Structure

The project is organized into separate folders and files to keep the code modular, reusable, and easy to maintain.

- **`data/`**: Contains the original dataset and the cleaned dataset used for analysis.
- **`notebooks/`**: Contains Jupyter notebooks used to test, validate, and demonstrate individual analysis modules.
- **`reports/screenshots/`**: Stores project's visuals: Taiga board progress, GitHub commit history, pull requests, and sample tool outputs
- **`src/`**: Contains the main Python source code, organized by analysis area.  
- **`main.py`**: Runs the complete workflow and integrates all analysis modules.
- **`requirements.txt`**: Lists the Python dependencies required to run the project.
- **`.gitignore`**: Defines files and folders that should not be uploaded to GitHub.
- **`README.md`**: Provides project documentation, setup instructions, workflow description, and team information.


```Text
Supply-Chain-Shipment-Summary-Tool/
│
├── data/
│   ├── supply_delivery_history.csv
│   └── supply_delivery_history_clean.csv
│
├── notebooks/
│   ├── demo_country.ipynb
│   ├── demo_data_loader.ipynb
│   ├── demo_vendor.ipynb
│   └── test1.ipynb
│
├── Reports/
│   └── screenshots/
│
├── src/
│   ├── cleaning.py
│   ├── country_analysis.py
│   ├── data_loader.py
│   ├── product_analysis.py
│   ├── shipment_summary.py
│   └── vendor_analysis.py
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Requirements

This project requires Python 3.10 or higher.

Install the required dependencies with:

```bash
pip install -r requirements.txt
```

Main dependencies:
```Text
pandas
numpy
matplotlib
seaborn
jupyter
```

## How to Run

From the project root folder, run:

```bash
python main.py
```

This will:

1. Load the raw shipment dataset.
2. Clean the data.
3. Save the cleaned dataset.
4. Run country analysis.
5. Run product analysis.
6. Run vendor analysis.
7. Run shipment summary analysis.
8. Display the generated charts.


## Analysis Modules

### Data Cleaning

The cleaning module prepares the raw dataset by:
- Handling missing or inconsistent values.
- Standardizing categorical fields.
- Cleaning numeric columns.
- Parsing date columns.
- Creating a cleaned CSV file for analysis.

### Shipment Analysis

The shipment analysis module summarizes shipment activity by:
- Shipment mode.
- Fulfillment type.
- Delivery year.
- Shipment volume.
- Shipment value.
- Freight cost.
- Delivery delay.

### Country Analysis

The country analysis module provides insights such as:
- Shipment quantity by country.
- Shipment value by country.
- Shipment count by country.
- Top countries by revenue.

### Product Analysis

The product analysis module summarizes:
- Product group performance.
- Sub-classification performance.
- Top products by shipment quantity.
- Product category distribution.

### Vendor Analysis

The vendor analysis module evaluates vendor performance by:
- Total shipment records.
- Total line item quantity.
- Total line item value.
- Top vendors by revenue.
- Bottom vendors by revenue.
- Vendor revenue and quantity visualizations.



## Agile Collaboration Workflow

The team followed an Agile workflow using GitHub and Taiga.

The workflow included:

- **Taiga:** Create User Stories and Sprint backlog and task tracking on our Taiga board.
- **Tasks:** Each User Story is broken down into tasks and assigned to Team Members.
- **Branch-per-feature:** Each user story is developed on its own branch.
- **Pull requests:** All changes are merged via PRs with peer review.
- **Traceability:** Commits and PRs reference Taiga user story IDs and Github Issue (e.g. `US-01`).


## GitHub Branching Strategy

Each feature was developed in a separate branch, for example:

```Text
feature/data-cleaning
feature/shipment-analysis
feature/country-analysis
feature/product-analysis
feature/vendor-analysis
docs/update-project-documentation
```
After development, each branch was reviewed and merged into the main branch through pull requests.

## User Stories

| ID | Stub |  Story | Points | Responsible |
|----|------|--------|--------|-------------|
| US-01 | Data Cleaning | As a supply chain stakeholder, I want the raw shipment data to be cleaned so that the analysis is accurate and reliable. | 2 | Chisco Henao, Julian David |
| US-02 | Shipment Analysis | As a logistics manager, I want to view shipment activity summaries so that I can understand shipment volume, delivery patterns, and fulfillment performance. | 3 | Chisco Henao, Julian David |
| US-03 | Country Analysis | As an operations manager, I want to analyze shipments by country so that I can compare shipment distribution across locations. | 5 | Sierra Garzon, Cesar |
| US-04 | Product Analysis | As a product category manager, I want to analyze shipment activity by product so that I can identify high-volume products and product groups. | 5 | Leon Granados, Daniela |
| US-05 | Vendor Analysis | As a vendor relationship manager, I want to view shipment activity by vendor so that I can identify which vendors handle the highest shipment volume and value. | 5 | Cuenca Bejar, Jorge Henry |
| US-06 | Integrated Analysis |As a supply chain manager, I want to run all analysis modules from one main workflow so that I can review the complete supply chain summary in a single execution. | 1 | Cuenca Bejar, Jorge Henry |


## Notebooks

The notebooks folder contains demo notebooks used to test and validate individual modules before integration.

Examples:
```Text
demo_data_loader.ipynb
demo_country.ipynb
demo_vendor.ipynb
```

These notebooks help demonstrate that individual functions work correctly before being integrated into `main.py`.

## Outputs

The project generates:
- Cleaned CSV dataset.
- Printed summary tables.
- Country analysis charts.
- Product analysis charts.
- Vendor performance charts.
- Shipment summary dashboard.


## Academic Context

This project was completed as part of the **Agile Software Development** course in the **Master of Data Analytics** program at the **University of Niagara Falls Canada**.

The objective was not only to build a working Python tool, but also to demonstrate Agile teamwork, iterative development, GitHub collaboration, and traceability between user stories, tasks, commits, and pull requests.

## License

Academic project for educational purposes only.
