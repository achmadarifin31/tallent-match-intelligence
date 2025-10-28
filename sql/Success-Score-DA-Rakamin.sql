CREATE OR REPLACE TABLE `rakamin-study-case-da.Study_Case_DA.success_score` AS
WITH comp AS (
  SELECT 
    employee_id,
    MAX(CASE WHEN pillar_code = 'QDD' THEN score END) AS QDD,
    MAX(CASE WHEN pillar_code = 'LIE' THEN score END) AS LIE,
    MAX(CASE WHEN pillar_code = 'SEA' THEN score END) AS SEA,
    MAX(CASE WHEN pillar_code = 'STO' THEN score END) AS STO,
    MAX(CASE WHEN pillar_code = 'FTC' THEN score END) AS FTC
  FROM `rakamin-study-case-da.Study_Case_DA.competencies_yearly`
  GROUP BY employee_id
),
psych AS (
  SELECT 
    employee_id,
    gtq,
    85 AS BehavioralFit
  FROM `rakamin-study-case-da.Study_Case_DA.profiles_psych`
)
SELECT 
  e.employee_id,
  c.QDD, c.LIE, c.SEA, c.STO, c.FTC,
  p.gtq AS GTQ,
  p.BehavioralFit,
  ROUND(
    (0.25 * COALESCE(c.QDD, 0)) + -- Decision Making (Competency)
    (0.20 * COALESCE(c.LIE, 0)) + -- Leadership Execution
    (0.20 * COALESCE(c.SEA, 0)) + -- Self Awareness
    (0.15 * COALESCE(c.STO, 0)) + -- Strategic Orientation
    (0.10 * COALESCE(c.FTC, 0)) + -- Fast Time to Close
    (0.05 * COALESCE(p.gtq, 0)) + -- Cognitive Ability
    (0.05 * COALESCE(p.BehavioralFit, 0)) -- Behavioral Fit
    ,2) AS SuccessScore
FROM `rakamin-study-case-da.Study_Case_DA.employees` e
LEFT JOIN comp c ON e.employee_id = c.employee_id
LEFT JOIN psych p ON e.employee_id = p.employee_id
WHERE p.gtq IS NOT NULL;