# tallent-match-intelligence
Study Case Data Analyst - Achmad Nurs Syururi Arifin

# Talent Match Intelligence — Company X (Case Study 2025)

This project builds an explainable **SuccessScore** (SQL in BigQuery) and an **AI-powered dashboard** (Streamlit) to identify what differentiates top performers and support succession planning.

## Repository Map
- `app/app.py` — Streamlit dashboard (reads precomputed `success_score` from BigQuery)
- `sql/success_explore.sql` — Step-1 exploration queries (gap/heatmap basis)
- `sql/match.sql` — Step-2 SuccessScore logic (weighted)
- `reports/Case_Study_Report.pdf` — Final consulting-grade deck
- `example.env` — Sample `.env` format (no real keys)

## Tech Stack
- **Data Warehouse:** Google BigQuery
- **Analytics:** Python (pandas/numpy)
- **App:** Streamlit
- **AI:** OpenRouter API (for job profile text)

## Local Setup (no code changes)
1. Python 3.10+  
2. (Optional) Virtual env:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
