#  CoinStream – End-to-End Cryptocurrency Data Engineering Pipeline

CoinStream is a production-style cloud data engineering project that automatically collects live cryptocurrency market data from the CoinGecko API, stores raw data in an AWS S3 data lake, transforms it into a multi-layer data warehouse (Bronze, Silver, and Gold), and refreshes analytical datasets in PostgreSQL for reporting and business intelligence.

The pipeline is fully automated using **AWS EventBridge Scheduler**, **AWS Lambda**, and **AWS Systems Manager (SSM)**, allowing the entire workflow to run without manual intervention.

---

# 📌 Project Overview

This project demonstrates an end-to-end modern data engineering workflow using AWS cloud services and Python.

The pipeline:

- Extracts live cryptocurrency market data
- Validates incoming records
- Archives raw JSON data in Amazon S3
- Loads historical snapshots into PostgreSQL
- Builds Bronze, Silver, and Gold warehouse layers
- Produces analytical datasets for reporting
- Runs automatically on a schedule

---

# 🏗️ Architecture

```text
                    EventBridge Scheduler
                             │
                             ▼
                      AWS Lambda Function
                             │
                             ▼
                AWS Systems Manager (SSM)
                             │
                             ▼
                    Amazon EC2 Instance
                             │
                             ▼
                  CoinStream ETL Pipeline
                             │
        ┌────────────────────┴────────────────────┐
        ▼                                         ▼
 CoinGecko REST API                         Amazon S3
        │                               (Raw JSON Archive)
        └────────────────────┬────────────────────┘
                             ▼
                       PostgreSQL Warehouse
                  Bronze → Silver → Gold
                             │
                             ▼
                        Power BI Dashboard
```

---

# ⚙️ Tech Stack

## Programming

- Python 3.12
- SQL

## Cloud

- Amazon EC2
- Amazon S3
- AWS Lambda
- AWS Systems Manager (SSM)
- Amazon EventBridge Scheduler
- IAM Roles

## Database

- PostgreSQL 16

## Libraries

- pandas
- boto3
- SQLAlchemy
- requests
- psycopg2
- python-dotenv

## Version Control

- Git
- GitHub

---

# 📂 Project Structure

```
CoinStream/
│
├── data/
│   └── raw/
│
├── sql/
│   └── create_tables.sql
│
├── src/
│   ├── api/
│   ├── config/
│   ├── database/
│   ├── etl/
│   ├── pipeline/
│   ├── storage/
│   └── utils/
│
├── main.py
├── requirements.txt
├── .env
└── README.md
```

---

# 🔄 ETL Workflow

## 1️⃣ Extract

- Connects to CoinGecko REST API
- Retrieves live cryptocurrency market data
- Supports automatic retry handling

---

## 2️⃣ Validate

Checks for:

- Missing values
- Duplicate records
- Invalid data types
- Schema consistency

---

## 3️⃣ Raw Data Archive

Each successful API response is archived in Amazon S3.

Example:

```
s3://coinstream-data-lake/raw/2026/08/01/crypto_market_20260801_170041.json
```

---

## 4️⃣ Bronze Layer

Stores historical snapshots exactly as received.

Purpose:

- Immutable historical storage
- Audit trail
- Replay capability

---

## 5️⃣ Silver Layer

Transforms Bronze data by:

- Standardizing fields
- Cleaning records
- Removing inconsistencies
- Preparing analytical tables

---

## 6️⃣ Gold Layer

Produces business-ready datasets including:

### Market Summary

Overall market metrics.

### Top 10 Coins

Top cryptocurrencies ranked by market capitalization.

### Market Trends

Historical market performance for reporting and dashboards.

---

# ☁️ AWS Services Used

## Amazon EC2

Hosts the complete Python pipeline.

---

## Amazon S3

Stores raw JSON files as the project's data lake.

---

## AWS Lambda

Triggers pipeline execution remotely.

---

## AWS Systems Manager (SSM)

Executes the pipeline securely on the EC2 instance without SSH.

---

## Amazon EventBridge Scheduler

Automates execution on a daily schedule.

---

# 🔐 Security

The project uses IAM Roles instead of hard-coded AWS credentials.

Benefits include:

- No AWS Access Keys stored in code
- Automatic credential rotation
- Secure S3 access
- Production best practice

---

# 📊 Warehouse Design

```
Raw API Data
      │
      ▼
  Bronze Layer
      │
      ▼
  Silver Layer
      │
      ▼
   Gold Layer
```

---

# 📈 Example Output



<img width="834" height="642" alt="Screenshot 2026-08-01 215521" src="https://github.com/user-attachments/assets/c2ae65f5-97c9-431b-816d-e9da12a007f7" />
<img width="790" height="637" alt="Screenshot 2026-08-01 215439" src="https://github.com/user-attachments/assets/97dd2d89-d7d5-44a0-9f3b-2456551ffe4f" />


---

# 🚀 Automation

Pipeline execution flow:

```
EventBridge
      │
      ▼
Lambda
      │
      ▼
SSM Run Command
      │
      ▼
EC2
      │
      ▼
CoinStream Pipeline
```

No manual execution is required once deployed.

---

# 💡 Features

- Live cryptocurrency data ingestion
- Automated ETL pipeline
- Data validation
- Historical snapshot storage
- Bronze/Silver/Gold architecture
- Cloud automation
- S3 data lake
- PostgreSQL warehouse
- Production logging
- Duplicate detection
- Scheduled execution
- Modular project structure

---

# 📌 Future Improvements

- Docker containerization
- Apache Airflow orchestration
- dbt transformations
- Great Expectations data quality testing
- CloudWatch monitoring
- SNS email alerts
- Terraform infrastructure provisioning
- CI/CD with GitHub Actions
- Data catalog integration
- Grafana monitoring dashboard

---

# 👨‍💻 Author

**Michael Okposo**

Doctor of Pharmacy | Data Analyst | Data Engineer

Email:
okposom@gmail.com

LinkedIn:
https://www.linkedin.com/in/michael-okposo

---

# ⭐ If you found this project useful

Please consider giving the repository a ⭐.
