
-- ==========================================
-- PAYPULSE REAL DATA ANALYSIS
-- STEP 10: TOP STATES BY TRANSACTION VOLUME
-- ==========================================

USE paypulse_real;

SELECT
    state,

    SUM(transaction_count) AS total_transactions,

    ROUND(
        SUM(transaction_amount) / 10000000,
        2
    ) AS transaction_value_crore

FROM state_transactions

WHERE year = 2025

GROUP BY state

ORDER BY total_transactions DESC

LIMIT 10;
-- STEP 11: Quarterly Transaction Analysis (2025)

USE paypulse_real;

SELECT
    year,
    quarter,
    SUM(transaction_count) AS total_transactions,
    ROUND(SUM(transaction_amount) / 10000000, 2)
        AS transaction_value_crore
FROM state_transactions
WHERE year = 2025
GROUP BY year, quarter
ORDER BY quarter;


-- STEP 12: Quarter-over-Quarter Growth

WITH quarterly_data AS (
    SELECT
        year,
        quarter,
        SUM(transaction_count) AS total_transactions
    FROM state_transactions
    GROUP BY year, quarter
),
growth_data AS (
    SELECT
        year,
        quarter,
        total_transactions,
        LAG(total_transactions) OVER (
            ORDER BY year, quarter
        ) AS previous_quarter
    FROM quarterly_data
)
SELECT
    year,
    quarter,
    total_transactions,
    ROUND(
        (total_transactions - previous_quarter)
        * 100.0 / NULLIF(previous_quarter, 0),
        2
    ) AS growth_percentage
FROM growth_data
WHERE year = 2025
ORDER BY quarter;
