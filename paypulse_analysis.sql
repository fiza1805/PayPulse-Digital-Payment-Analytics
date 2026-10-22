USE paypulse;

SELECT
    m.merchant_name,
    COUNT(*) AS total_transactions,

    SUM(
        CASE
            WHEN t.payment_status = 'FAILED'
            THEN 1 ELSE 0
        END
    ) AS failed_transactions,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN t.payment_status = 'FAILED'
                THEN 1 ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS failure_rate

FROM transactions t

JOIN merchants m
    ON t.merchant_id = m.merchant_id

GROUP BY
    m.merchant_id,
    m.merchant_name

ORDER BY failure_rate DESC;


-- STEP 5: HOURLY TRANSACTION ANALYSIS

SELECT
    HOUR(transaction_date) AS transaction_hour,

    COUNT(*) AS total_transactions,

    SUM(
        CASE
            WHEN payment_status = 'FAILED'
            THEN 1 ELSE 0
        END
    ) AS failed_transactions,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN payment_status = 'FAILED'
                THEN 1 ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS failure_rate

FROM transactions

GROUP BY HOUR(transaction_date)

ORDER BY total_transactions DESC;

-- ==========================================
-- STEP 6: DAILY TRANSACTION TREND ANALYSIS
-- ==========================================

USE paypulse;

SELECT
    DATE(transaction_date) AS transaction_day,

    COUNT(*) AS total_transactions,

    SUM(
        CASE
            WHEN payment_status = 'SUCCESS'
            THEN 1 ELSE 0
        END
    ) AS successful_transactions,

    SUM(
        CASE
            WHEN payment_status = 'FAILED'
            THEN 1 ELSE 0
        END
    ) AS failed_transactions,

    ROUND(
        SUM(
            CASE
                WHEN payment_status = 'SUCCESS'
                THEN amount ELSE 0
            END
        ), 2
    ) AS successful_payment_value

FROM transactions

GROUP BY DATE(transaction_date)

ORDER BY transaction_day ASC;

-- ==========================================
-- STEP 6: DAILY TRANSACTION TREND ANALYSIS
-- ==========================================

USE paypulse;

SELECT
    DATE(transaction_date) AS transaction_day,

    COUNT(*) AS total_transactions,

    SUM(
        CASE
            WHEN payment_status = 'SUCCESS'
            THEN 1 ELSE 0
        END
    ) AS successful_transactions,

    SUM(
        CASE
            WHEN payment_status = 'FAILED'
            THEN 1 ELSE 0
        END
    ) AS failed_transactions,

    ROUND(
        SUM(
            CASE
                WHEN payment_status = 'SUCCESS'
                THEN amount ELSE 0
            END
        ), 2
    ) AS successful_payment_value

FROM transactions

GROUP BY DATE(transaction_date)

ORDER BY transaction_day ASC;

-- ==========================================
-- STEP 7: MERCHANT PAYMENT VALUE ANALYSIS
-- ==========================================

USE paypulse;

SELECT
    m.merchant_name,
    m.merchant_category,

    COUNT(t.transaction_id) AS total_transactions,

    SUM(
        CASE
            WHEN t.payment_status = 'SUCCESS'
            THEN 1 ELSE 0
        END
    ) AS successful_transactions,

    ROUND(
        SUM(
            CASE
                WHEN t.payment_status = 'SUCCESS'
                THEN t.amount ELSE 0
            END
        ), 2
    ) AS successful_payment_value,

    ROUND(
        AVG(
            CASE
                WHEN t.payment_status = 'SUCCESS'
                THEN t.amount
                ELSE NULL
            END
        ), 2
    ) AS average_successful_payment

FROM merchants m

JOIN transactions t
    ON m.merchant_id = t.merchant_id

GROUP BY
    m.merchant_id,
    m.merchant_name,
    m.merchant_category

ORDER BY successful_payment_value DESC;

-- ==========================================
-- STEP 8: PAYMENT FAILURE REASON ANALYSIS
-- ==========================================

USE paypulse;

SELECT
    COALESCE(failure_reason, 'Not Specified')
        AS failure_reason,

    COUNT(*) AS failed_transactions,

    ROUND(
        COUNT(*) * 100.0 /
        (
            SELECT COUNT(*)
            FROM transactions
            WHERE payment_status = 'FAILED'
        ),
        2
    ) AS failure_percentage

FROM transactions

WHERE payment_status = 'FAILED'

GROUP BY failure_reason

ORDER BY failed_transactions DESC;
