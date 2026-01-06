# Project Overview
Developed an end-to-end data extraction, transformation, cleaning, and enrichment pipeline for U.S.-based restaurants by integrating third-party APIs, including Yelp and Google Places. 
Built Python-based API ingestion workflows to backfill missing attributes, normalized nested JSON responses into structured analytical datasets, and filtered records to restaurant-only businesses. 
The enriched dataset enabled comparative analysis of restaurant closures before and after the COVID-19 pandemic, supporting data-driven insights into industry trends and operational impact.

## Data Cleaning & Enrichment Process

- Geographic filtering

  - Restricted the dataset to U.S.-based businesses only to ensure geographic consistency.

- Category standardization

  - Identified missing or incomplete business categories and enriched them using Yelp and Google Places APIs.

- Restaurant selection

  - Filtered records to restaurants only, removing non-food businesses from the dataset.

- Operating hours completion

  - Filled missing operating hours by retrieving additional business details from the Google Places API.

- Business status analysis

  - Classified restaurants based on closure timing: pre-pandemic vs. post-pandemic closures for trend analysis.

- JSON normalization & feature expansion

  - Converted nested API responses (JSON) into structured formats and expanded additional analytical columns.

- Price level enrichment

  - Retrieved missing price-level information from the Google Places API.

- Third-party data completion

  - Backfilled remaining missing attributes using the Yelp REST API to improve data completeness and accuracy.
