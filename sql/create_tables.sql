/*==========================================================
CREATE SCHEMAS
==========================================================*/

CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS monitoring;


/*==========================================================
BRONZE LAYER (RAW DATA)
==========================================================*/

CREATE TABLE IF NOT EXISTS bronze.crypto_market (

    coin_id TEXT,
    symbol TEXT,
    coin_name TEXT,

    current_price NUMERIC,
    market_cap NUMERIC,
    market_cap_rank INTEGER,
    total_volume NUMERIC,

    high_24h NUMERIC,
    low_24h NUMERIC,

    price_change_percentage_24h NUMERIC,
    circulating_supply NUMERIC,

    last_updated TIMESTAMP,

    snapshot_date DATE,
    pipeline_timestamp TIMESTAMP

);


/*==========================================================
SILVER LAYER (CLEANED DATA)
==========================================================*/

CREATE TABLE IF NOT EXISTS silver.crypto_market_clean (

    coin_id TEXT,
    symbol TEXT,
    coin_name TEXT,

    current_price NUMERIC,
    market_cap NUMERIC,
    market_cap_rank INTEGER,
    total_volume NUMERIC,

    price_change_percentage_24h NUMERIC,
    circulating_supply NUMERIC,

    snapshot_date DATE,
    pipeline_timestamp TIMESTAMP

);


/*==========================================================
PIPELINE MONITORING
==========================================================*/

CREATE TABLE IF NOT EXISTS monitoring.pipeline_runs (

    run_id SERIAL PRIMARY KEY,

    pipeline_name TEXT NOT NULL,

    start_time TIMESTAMP,
    end_time TIMESTAMP,

    duration_seconds NUMERIC,

    records_extracted INTEGER,
    records_loaded INTEGER,

    status TEXT

);