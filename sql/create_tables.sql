/*==========================================================
CREATE SCHEMAS
==========================================================*/

CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
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
    pipeline_timestamp TIMESTAMP,

    PRIMARY KEY (coin_id, snapshot_date)

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
    pipeline_timestamp TIMESTAMP,

    PRIMARY KEY (coin_id, snapshot_date)

);


/*==========================================================
GOLD LAYER
==========================================================*/

------------------------------------------------------------
-- Executive KPIs
------------------------------------------------------------

CREATE TABLE IF NOT EXISTS gold.market_summary (

    snapshot_date DATE PRIMARY KEY,

    total_market_cap NUMERIC,

    average_price NUMERIC,

    average_24h_change NUMERIC,

    total_volume NUMERIC,

    total_coins INTEGER,

    pipeline_timestamp TIMESTAMP

);


------------------------------------------------------------
-- Top 10 Coins
------------------------------------------------------------

CREATE TABLE IF NOT EXISTS gold.top10_coins (

    coin_id TEXT,

    symbol TEXT,

    coin_name TEXT,

    current_price NUMERIC,

    market_cap NUMERIC,

    market_cap_rank INTEGER,

    total_volume NUMERIC,

    price_change_percentage_24h NUMERIC,

    snapshot_date DATE,

    pipeline_timestamp TIMESTAMP,

    PRIMARY KEY (coin_id, snapshot_date)

);


------------------------------------------------------------
-- Historical Market Trends
------------------------------------------------------------

CREATE TABLE IF NOT EXISTS gold.market_trends (

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

    pipeline_timestamp TIMESTAMP,

    PRIMARY KEY (coin_id, snapshot_date)

);


/*==========================================================
PIPELINE MONITORING
==========================================================*/

CREATE TABLE IF NOT EXISTS monitoring.pipeline_runs (

    run_id SERIAL PRIMARY KEY,

    pipeline_name TEXT NOT NULL,

    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    end_time TIMESTAMP,

    duration_seconds NUMERIC,

    records_extracted INTEGER,

    records_loaded INTEGER,

    status TEXT

);