# 🚀 Data-Driven Business Transformation: From Manual Sheets to 5x Operational Growth

## 📌 Executive Summary
This project demonstrates a complete end-to-end transformation of an organization's data ecosystem. By transitioning the company from fragmented Excel sheets and disconnected tools to a centralized, automated BI infrastructure, I enabled data-backed decision-making that resulted in **50% higher marketing conversions**, a **5x increase in operational productivity**, and the successful expansion into **5 new branches**.

---

## 🛠️ Tech Stack & Integrations
* **Languages:** Python (Pandas, NumPy, Requests, SQLAlchemy)
* **Data Sources:** HubSpot CRM (via REST API), PostgreSQL, Google Analytics 4 (GA4)
* **Infrastructure:** Google Tag Manager (GTM), Automated Data Pipelines
* **BI & Visualization:** Power BI / Looker Studio
* **Methodology:** Full Data Lifecycle Ownership (Extraction → Modeling → Insights)

---

## 💡 Key Solutions & Business Impact

### 1. Unified Data Architecture (The Single Source of Truth)
* **The Problem:** Data was siloed across HubSpot, PostgreSQL, and manual Excel sheets, making real-time reporting impossible.
* **The Solution:** Built a custom ETL pipeline using **Python** to extract data via **HubSpot API** and integrated it with operational databases.
* **Result:** Reduced manual reporting time by **90%**, providing leadership with real-time clarity.

### 2. Sales Integrity & Anomaly Detection
* **The Insight:** Through "Closing Pattern" analysis, I discovered that sales teams were artificially delaying deal closures to meet next month's targets.
* **The Action:** Engineered a performance tracking system that flagged these anomalies.
* **Result:** Stabilized monthly revenue forecasting and eliminated "deal pushing" behaviors.

### 3. Marketing ROI & Conversion Optimization
* **Conversion Lift:** Analyzed GA4 search intent and keywords, refining the targeting strategy to achieve a **50% increase in Conversion Rate**.
* **Budget Optimization:** Identified "False Conversions" coming from low-quality placements (e.g., kids' YouTube channels), reallocating budget to high-performing segments.
* **Full-Funnel Tracking:** Linked Social Media spend to CRM deals using **GTM**, closing the ROI loop for all campaigns.

### 4. Operational Excellence
* **Bottleneck Analysis:** Conducted internal surveys and process mining to identify friction points. 
* **Result:** Optimized workflows led to a **5x increase in productivity** and the successful operational launch of **5 new branches**.

---

## 📂 Repository Structure
```text
├── src/
│   ├── hubspot_api_connector.py   # Python logic for CRM data extraction
│   ├── marketing_attribution.sql  # SQL queries for ROI and GA4 analysis
│   └── data_pipeline_main.py      # Main ETL flow logic
├── docs/
│   ├── kpi_framework.pdf          # Definition of cross-departmental metrics
│   └── system_architecture.png    # Visual map of the data ecosystem
└── README.md
