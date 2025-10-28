CREATE TABLE IF NOT EXISTS `rakamin-study-case-da.Study_Case_DA.talent_benchmarks` (
  job_vacancy_id STRING,                  -- ID unik vacancy
  role_name STRING,                       -- Nama role (mis. Data Analyst)
  job_level STRING,                       -- Level (Junior, Middle, Senior)
  role_purpose STRING,                    -- Deskripsi singkat peran
  benchmark_employee_ids ARRAY<STRING>,   -- daftar employee_id rating 5 yang dipilih user
  created_at TIMESTAMP                    -- waktu input
);