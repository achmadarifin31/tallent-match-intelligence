import os
import requests
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import altair as alt
from dotenv import load_dotenv
from google.cloud import bigquery

# ===================== LOAD ENV & CONFIG =====================

# 1️⃣ Load environment dulu
load_dotenv(dotenv_path=r"D:/Projects/Study Case Rakamin/ai_talent_app/.env")

# 2️⃣ Baru ambil key setelah .env diload
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Debug print untuk memastikan key kebaca
if not OPENROUTER_KEY:
    st.error("❌ OPENROUTER_API_KEY belum terbaca dari .env")
else:
    st.success(f"🔑 OPENROUTER_API_KEY terdeteksi: {OPENROUTER_KEY[:10]}...")

# 3️⃣ Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"D:/Projects/Study Case Rakamin/rakamin-study-case-da-fbce82b3a782.json"
client = bigquery.Client(project="rakamin-study-case-da")

# 4️⃣ Streamlit app setup
st.set_page_config(page_title="AI Talent Dashboard", layout="wide")
st.title("AI Talent App — Step 3 Dashboard 🚀")
st.markdown("Menampilkan hasil perhitungan **Success Score** dari Step 2")


# ===================== FUNCTION SECTION =====================

def generate_ai_profile(role_name, job_level, role_purpose):
    """
    Generate AI-based Job Profile using OpenRouter
    """
    if not OPENROUTER_KEY:
        return "❌ OPENROUTER_API_KEY belum diset. Tambahkan dulu di environment variable."

    prompt = f"""
    Kamu adalah AI Talent Analyst profesional.
    Buatkan profil pekerjaan untuk peran berikut:

    Role Name: {role_name}
    Job Level: {job_level}
    Role Purpose: {role_purpose}

    Sertakan bagian:
    1. **Job Requirements** — skill teknis & non-teknis yang dibutuhkan
    2. **Job Description** — ringkasan peran dan tanggung jawab
    3. **Key Competencies** — kompetensi utama untuk sukses di peran ini
    4. **Soft Skills dan Behavioral Traits** — pola perilaku yang diharapkan
    Gunakan bahasa profesional dan jelas.
    """

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Gagal generate AI profile: {e}"


def generate_ai_summary(role_name, avg_scores, df):
    """
    Generate AI-based summary comparing benchmark vs total population
    """
    if not OPENROUTER_KEY:
        return "❌ OPENROUTER_API_KEY belum diset."

    # Hitung rata-rata keseluruhan populasi
    population_avg = df[["QDD", "LIE", "SEA", "STO", "FTC", "GTQ", "BehavioralFit", "SuccessScore"]].mean().round(2)
    comparison_text = f"""
    Benchmark Average: {avg_scores.to_dict()}
    Population Average: {population_avg.to_dict()}
    """

    prompt = f"""
    Kamu adalah AI Talent Analyst.
    Berdasarkan data kompetensi berikut, buatkan ringkasan analitik singkat (maks 2 paragraf):

    Role: {role_name}
    {comparison_text}

    Analisis:
    1. Kompetensi yang menonjol dibanding rata-rata perusahaan
    2. Area yang masih perlu dikembangkan
    3. Interpretasi singkat mengenai kekuatan benchmark talent pool ini
    """

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Gagal generate AI summary: {e}"


# ===================== QUERY BIGQUERY =====================

query = """
SELECT *
FROM `rakamin-study-case-da.Study_Case_DA.success_score`
WHERE SuccessScore IS NOT NULL
ORDER BY SuccessScore DESC
LIMIT 50
"""

try:
    df = client.query(query).to_dataframe()
    st.success("✅ Data berhasil diambil dari BigQuery!")
except Exception as e:
    st.error(f"❌ Gagal ambil data: {e}")
    st.stop()


# ===================== DISPLAY DATAFRAME =====================

st.subheader("Top 50 Employee by Success Score")
st.dataframe(df, use_container_width=True)

# Bar chart for top scores
chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("employee_id:N", sort="-y"),
        y="SuccessScore:Q",
        tooltip=["employee_id", "SuccessScore"]
    )
    .properties(height=400)
)
st.altair_chart(chart, use_container_width=True)

st.markdown("---")
st.subheader("🎯 Create AI Talent Profile & Benchmark Comparison")

# ===================== INPUT FORM =====================

with st.form("input_form"):
    role_name = st.text_input("Role Name (e.g. Data Analyst)")
    job_level = st.selectbox("Job Level", ["Junior", "Middle", "Senior"])
    role_purpose = st.text_area("Role Purpose", "Describe this role purpose here...")
    benchmark_ids = st.text_input("Benchmark Employee IDs (pisahkan dengan koma, contoh: EMP100221, EMP101186, EMP101683)")
    submitted = st.form_submit_button("🔍 Generate Profile & Insights")

# ===================== IF SUBMITTED =====================

if submitted:
    st.info(f"Benchmarking untuk: **{role_name} ({job_level})**")

    benchmark_list = [x.strip() for x in benchmark_ids.split(",") if x.strip()]
    if not benchmark_list:
        st.warning("⚠️ Mohon masukkan minimal 1 Employee ID untuk benchmark.")
    else:
        query = """
        SELECT *
        FROM `rakamin-study-case-da.Study_Case_DA.success_score`
        WHERE employee_id IN UNNEST(@benchmark_ids)
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ArrayQueryParameter("benchmark_ids", "STRING", benchmark_list)]
        )
        results = client.query(query, job_config=job_config).to_dataframe()

        if results.empty:
            st.error("❌ Tidak ditemukan data untuk Employee ID tersebut.")
        else:
            st.success(f"✅ Data benchmark ditemukan untuk {len(results)} karyawan.")
            st.dataframe(results)

            # ======= Hitung baseline =======
            avg_scores = results[["QDD", "LIE", "SEA", "STO", "FTC", "GTQ", "BehavioralFit", "SuccessScore"]].mean().round(2)
            st.write("### 📊 Baseline (Rata-rata Kompetensi Benchmark)")
            st.dataframe(avg_scores.to_frame("Average Score"))
            
            # ======= Ringkasan Benchmark =======
            st.markdown("### 📈 Ringkasan Benchmark Overview")
            col1, col2, col3 = st.columns(3)
            col1.metric("Average Success Score", f"{avg_scores['SuccessScore']:.2f}")
            col2.metric("Behavioral Fit", f"{avg_scores['BehavioralFit']:.2f}")
            col3.metric("Top Competency", avg_scores[['QDD','LIE','SEA','STO','FTC','GTQ','BehavioralFit']].idxmax())

            # ======= Radar Chart =======
            traits = ["QDD", "LIE", "SEA", "STO", "FTC", "GTQ", "BehavioralFit"]
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=avg_scores[traits],
                theta=traits,
                fill='toself',
                name='Benchmark Average'
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=False,
                title="🕸 Benchmark Competency Profile"
            )
            st.plotly_chart(fig)

            # ======= AI-Generated Job Profile =======
            st.markdown("## 🤖 AI-Generated Job Profile")
            with st.spinner("Generating job profile..."):
                ai_profile = generate_ai_profile(role_name, job_level, role_purpose)
            st.markdown(ai_profile)

            # ======= AI Summary (Benchmark vs Population) =======
            st.markdown("## 📈 AI Summary Insights")
            with st.spinner("Analyzing benchmark vs population..."):
                ai_summary = generate_ai_summary(role_name, avg_scores, df)
            st.markdown(ai_summary)
