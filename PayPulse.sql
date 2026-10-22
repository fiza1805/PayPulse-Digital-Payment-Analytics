
-- =====================================================
-- PAYPULSE
-- UPI Transaction Reliability & Risk Intelligence
-- Complete Database Setup
-- =====================================================

-- STEP 1: CREATE DATABASE

CREATE DATABASE IF NOT EXISTS paypulse;
USE paypulse;


-- STEP 2: RESET EXISTING TABLES
-- WARNING: Deletes existing PayPulse table data.
-- Use only for this initial development setup.

DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS merchants;


-- STEP 3: CREATE MERCHANTS TABLE

CREATE TABLE merchants (
    merchant_id INT PRIMARY KEY AUTO_INCREMENT,
    merchant_name VARCHAR(100) NOT NULL UNIQUE,
    merchant_category VARCHAR(50) NOT NULL,
    city VARCHAR(50),
    registration_date DATE
);


-- STEP 4: CREATE TRANSACTIONS TABLE

CREATE TABLE transactions (
    transaction_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    merchant_id INT NOT NULL,
    transaction_date DATETIME NOT NULL,
    amount DECIMAL(12,2) NOT NULL,

    payment_status ENUM(
        'SUCCESS',
        'FAILED',
        'PENDING'
    ) NOT NULL,

    payment_method VARCHAR(30) DEFAULT 'UPI',
    failure_reason VARCHAR(100),

    FOREIGN KEY (merchant_id)
        REFERENCES merchants(merchant_id),

    CHECK (amount > 0)
);


-- STEP 5: INSERT FIVE MERCHANTS

INSERT INTO merchants
(merchant_name, merchant_category, city, registration_date)
VALUES
('FreshMart', 'Grocery', 'Hyderabad', '2025-01-10'),
('QuickBite', 'Food', 'Bengaluru', '2025-02-15'),
('TechZone', 'Electronics', 'Mumbai', '2025-03-20'),
('StyleHub', 'Fashion', 'Delhi', '2025-04-05'),
('DailyNeeds', 'Grocery', 'Chennai', '2025-05-12');


-- STEP 6: GENERATE 10,000 SYNTHETIC TRANSACTIONS


USE paypulse;

INSERT INTO transactions (
    merchant_id,
    transaction_date,
    amount,
    payment_status,
    payment_method,
    failure_reason
)
SELECT
    merchant_id,
    transaction_date,
    amount,
    CASE
        WHEN status_random < 0.85 THEN 'SUCCESS'
        WHEN status_random < 0.97 THEN 'FAILED'
        ELSE 'PENDING'
    END,
    'UPI',
    CASE
        WHEN status_random >= 0.85
         AND status_random < 0.97
        THEN 'Payment Processing Failure'
        ELSE NULL
    END
FROM (
    SELECT
        1 + FLOOR(RAND() * 5) AS merchant_id,
        DATE_SUB(
            '2026-10-01 00:00:00',
            INTERVAL FLOOR(RAND() * 259200) MINUTE
        ) AS transaction_date,
        ROUND(50 + RAND() * 9950, 2) AS amount,
        RAND() AS status_random
    FROM
        information_schema.COLUMNS a
    CROSS JOIN
        information_schema.COLUMNS b
    LIMIT 10000
) AS generated_data;


WITH RECURSIVE numbers AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1
    FROM numbers
    WHERE n < 1000
),

digits AS (
    SELECT 0 AS digit UNION ALL
    SELECT 1 UNION ALL SELECT 2 UNION ALL
    SELECT 3 UNION ALL SELECT 4 UNION ALL
    SELECT 5 UNION ALL SELECT 6 UNION ALL
    SELECT 7 UNION ALL SELECT 8 UNION ALL
    SELECT 9
),

generated AS (
    SELECT
        ROW_NUMBER() OVER (ORDER BY n, digit) AS rn
    FROM numbers
    CROSS JOIN digits
),

sample_data AS (
    SELECT
        1 + FLOOR(RAND() * 5) AS merchant_id,

        DATE_SUB(
            '2026-10-01 00:00:00',
            INTERVAL FLOOR(RAND() * 180 * 1440) MINUTE
        ) AS transaction_date,

        ROUND(50 + RAND() * 9950, 2) AS amount,

        RAND() AS status_random

    FROM generated
),

classified AS (
    SELECT
        merchant_id,
        transaction_date,
        amount,

        CASE
            WHEN status_random < 0.85
                THEN 'SUCCESS'
            WHEN status_random < 0.97
                THEN 'FAILED'
            ELSE 'PENDING'
        END AS payment_status,

        CASE
            WHEN status_random >= 0.85
             AND status_random < 0.97
                THEN 'Payment Processing Failure'
            ELSE NULL
        END AS failure_reason

    FROM sample_data
)

SELECT
    merchant_id,
    transaction_date,
    amount,
    payment_status,
    'UPI',
    failure_reason
FROM classified;


-- STEP 7: VERIFY TOTAL RECORDS

SELECT COUNT(*) AS total_merchants
FROM merchants;

SELECT COUNT(*) AS total_transactions
FROM transactions;


-- STEP 8: VIEW SAMPLE TRANSACTIONS

SELECT *
FROM transactions
LIMIT 10;


-- STEP 9: PAYMENT STATUS DISTRIBUTION

SELECT
    payment_status,
    COUNT(*) AS total_transactions,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM transactions),
        2
    ) AS percentage
FROM transactions
GROUP BY payment_status;


-- STEP 10: MERCHANT PERFORMANCE

SELECT
    m.merchant_name,
    COUNT(t.transaction_id) AS total_transactions,

    SUM(
        CASE
            WHEN t.payment_status = 'SUCCESS'
            THEN 1 ELSE 0
        END
    ) AS successful_transactions,

    SUM(
        CASE
            WHEN t.payment_status = 'FAILED'
            THEN 1 ELSE 0
        END
    ) AS failed_transactions

FROM merchants m
LEFT JOIN transactions t
    ON m.merchant_id = t.merchant_id

GROUP BY
    m.merchant_id,
    m.merchant_name

ORDER BY total_transactions DESC;


-- STEP 11: DAILY TRANSACTION TREND

SELECT
    DATE(transaction_date) AS transaction_day,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount), 2) AS total_attempted_amount

FROM transactions

GROUP BY DATE(transaction_date)
ORDER BY transaction_day;


-- STEP 12: OVERALL PAYMENT SUCCESS RATE

SELECT
    ROUND(
        100.0 * SUM(
            CASE
                WHEN payment_status = 'SUCCESS'
                THEN 1 ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS success_rate_percentage

FROM transactions;


-- =====================================================
-- PAYPULSE DATABASE SETUP COMPLETE
-- =====================================================
SELECT COUNT(*) AS total_transactions
FROM paypulse.transactions;




