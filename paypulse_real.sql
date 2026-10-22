
-- ==========================================
-- PAYPULSE REAL DATA DATABASE
-- Source: PhonePe Pulse
-- ==========================================

CREATE DATABASE IF NOT EXISTS paypulse_real;

USE paypulse_real;

-- State-level quarterly transactions

CREATE TABLE IF NOT EXISTS state_transactions (

    id INT AUTO_INCREMENT PRIMARY KEY,

    year INT NOT NULL,

    quarter INT NOT NULL,

    state VARCHAR(100) NOT NULL,

    transaction_count BIGINT NOT NULL,

    transaction_amount DECIMAL(22,2) NOT NULL,

    UNIQUE KEY unique_state_quarter (
        year,
        quarter,
        state
    ),

    CHECK (quarter BETWEEN 1 AND 4),

    CHECK (transaction_count >= 0),

    CHECK (transaction_amount >= 0)

);

-- Verify table creation

SHOW TABLES;

DESCRIBE state_transactions;
