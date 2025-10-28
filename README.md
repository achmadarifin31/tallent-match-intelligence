# tallent-match-intelligence
Study Case Data Analyst - Achmad Nurs Syururi Arifin

# Talent Match Intelligence — Company X (Case Study 2025)

This project builds an explainable **SuccessScore** model (SQL in BigQuery) and an **AI-powered dashboard** (Streamlit) to identify what differentiates top performers and support succession planning.

---

## 🚀 Project Overview

**Goal:**  
Help Company X identify traits of high-performing employees and find individuals who share those traits for succession planning.

**Key Deliverables:**
1. Success Pattern Discovery (exploratory analysis in Colab)
2. SQL-based SuccessScore computation (BigQuery)
3. Streamlit dashboard with AI Job Profile Generator (OpenRouter)

---

## 🧩 Repository Structure
talent-match-intelligence/
├─ sql/
│ ├─ Success-Score-DA-Rakamin.sql # create success_score table
│ └─ input-user.sql # create talent_benchmarks table
├─ reports/
│ └─ Case_Study_Report.pdf
├─ app.py
├─ requirements.txt
├─ service-account.json # GCP credentials 
├─ example.env # stores only OPENROUTER_API_KEY
└─ README.md

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
3. Create virtual environment & install dependencies:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
   pip install -r app/requirements.txt
4. Set Environment Variables
   Create .env file in the project root:
   ```bash
   OPENROUTER_API_KEY=sk-yourkey
   ```
   Place your Google Cloud Service Account JSON file (named service-account.json) in the root folder.
   Set the BigQuery credential path in terminal:
   ```bash
   Windows (PowerShell)
   $env:GOOGLE_APPLICATION_CREDENTIALS = "$PWD\service-account.json"

   macOS / Linux
   export GOOGLE_APPLICATION_CREDENTIALS="$PWD/service-account.json"
   ```
5. Prepare BigQuery Tables
   Run the SQL scripts in this order inside BigQuery Console:
   1️⃣ sql/Success-Score-DA-Rakamin.sql
   → Creates and populates table Study_Case_DA.success_score
   2️⃣ sql/input-user.sql
   → Creates table Study_Case_DA.talent_benchmarks for user benchmark input
   Ensure both tables exist in your dataset before running the dashboard.
6. Run the App
   ```bash
   streamlit run app/app.py
   ```
