# Personalized Recommendation System Based on Customer Similarity
## Project Overview

This project implements a personalized recommendation engine using transactional sales data, customer demographic features, and purchase behavior patterns.

The goal is to identify products and departments with high purchase affinity for each customer, separating the analysis into High-Ticket and Low-Ticket categories, in order to support:

Cross-selling strategies

Up-selling opportunities

Customer segmentation

Targeted marketing campaigns

The solution is data-driven, interpretable, and business-oriented, making it suitable for real-world production environments.

## Analytical Approach

The algorithm combines:

Similarity-based collaborative filtering

Demographic segmentation rules

Frequency and support analysis

Key features used

Gender

Age (± 4 years)

Payment capacity (± 200 units)

Historical purchases by product group

Product department

## Methodology

Data extraction

Connection to SQL Server using pyodbc

Optimized query with joins across customer, product, and store dimensions

Customer profile construction

Purchase history is extracted per account

Product group consumption patterns are identified

Similar customer selection

Customers are filtered based on:

Same gender

Similar age range

Similar payment capacity

Overlapping product group purchases

Ticket-based classification

High Ticket (TA): Strategically defined departments

Low Ticket (TB): Remaining departments

Metric computation

Frequency

Support

Total event count

Relevance ranking

Result generation

Top 10 recommendations per customer for:

Product groups (TA / TB)

Departments (TA / TB)

Exported as CSV files for downstream consumption (BI tools, CRM, marketing platforms)

## Output Files

The script generates four datasets:

Excel_ResultadosGpoTA_*.csv → Product groups (High Ticket)

Excel_ResultadosGpoTB_*.csv → Product groups (Low Ticket)

Excel_ResultadosTA_*.csv → Departments (High Ticket)

Excel_ResultadosTB_*.csv → Departments (Low Ticket)

Each file includes ranking, support metrics, and customer context.

## Tech Stack

* Python
* Pandas / NumPy

* SQL Server

* pyodbc

The solution is designed to be scalable, auditable, and easy to adapt for different business rules or markets.

## Business Impact

This approach enables:

* Higher conversion rates in personalized campaigns

* Reduced noise from generic recommendations

* Prioritization of high-affinity products

* Clear explainability of recommendations (interpretable logic)
