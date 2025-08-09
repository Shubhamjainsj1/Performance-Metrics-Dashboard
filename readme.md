# Performance Metrics Dashboard

## Overview
Simple pipeline: Generate sample data → Upload to BigQuery → Build Power BI report on top of BigQuery views.

## Prereqs
- Python 3.9+
- Google Cloud project & BigQuery enabled
- Service account JSON with BigQuery DataEditor role (or set up ADC)
- Power BI Desktop (to build report), or Power BI Service to publish

## Quickstart
1. Install deps
