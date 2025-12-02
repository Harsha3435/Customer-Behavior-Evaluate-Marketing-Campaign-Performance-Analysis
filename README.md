# Data Analysis Project

This project simulates a retail e-commerce environment to perform comprehensive data analysis on customer behavior and marketing campaign performance. It includes scripts for data generation, cleaning, metric calculation, and visualization.

## Project Overview

The goal of this project is to derive actionable insights from transaction and marketing data. Key areas of analysis include:
- **Customer Behavior**: Retention, churn, segmentation, and purchasing patterns.
- **Marketing Performance**: ROI, CTR, conversion rates, and campaign efficiency.

## Installation

1. Clone the repository.
2. Install the required Python packages:
   ```bash
   pip install pandas numpy matplotlib seaborn
   ```

## Usage

1. **Generate Data**:
   Run the data generation script to create the mock datasets (`customer_transactions.csv` and `marketing_campaigns.csv`).
   ```bash
   python generate_data.py
   ```

2. **Run Analysis**:
   Execute the analysis scripts to process the data, calculate metrics, and generate visualizations.
   ```bash
   python analyze_customers.py
   python analyze_campaigns.py
   ```



## Project Structure

- `generate_data.py`: Script to generate mock datasets.
- `analyze_customers.py`: Script for customer behavior analysis.
- `analyze_campaigns.py`: Script for marketing campaign analysis.
- `final_report.md`: Comprehensive report with insights and visualizations.
- `*.csv`: Generated data files.
- `*.png`: Generated visualization charts.
- `*.json`: Exported metrics for reporting.

## Key Insights

- **High Retention**: 96.9% customer retention rate.
- **Strong ROI**: Marketing campaigns generate a 359% ROI.
- **Optimization Opportunity**: Significant performance gap between top and bottom campaigns suggests room for budget reallocation.


