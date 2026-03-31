import os
import pandas as pd
from datetime import datetime
from hubspot_ingestion import HubSpotConnector
from ga4_extractor import GoogleAnalyticsConnector
# from mailster_connector import MailsterConnector # Assuming this is the third module

def run_etl_pipeline():
    """
    Main Orchestrator for the Data Pipeline.
    Coordinates extraction from multiple APIs and prepares data for BI consumption.
    """
    print(f"--- ETL Pipeline Started at {datetime.now()} ---")

    # 1. Initialize Connectors using Environment Variables
    hs_token = os.getenv('HUBSPOT_TOKEN')
    ga4_property_id = os.getenv('GA4_PROPERTY_ID')
    ga4_creds = "service_account.json"

    # 2. Extract Data from HubSpot (CRM)
    print("Step 1: Extracting CRM Data...")
    hs = HubSpotConnector(hs_token)
    deals_df = hs.get_all_records("deals", "amount,dealname,dealstage,closedate,pipeline")
    contacts_df = hs.get_all_records("contacts", "email,firstname,lastname,lifecyclestage")

    # 3. Extract Data from Google Analytics 4 (Marketing)
    print("Step 2: Extracting Marketing Analytics...")
    ga4 = GoogleAnalyticsConnector(ga4_property_id, ga4_creds)
    marketing_df = ga4.get_report(
        start_date="30daysAgo", 
        end_date="today", 
        dimensions_list=["sessionSourceMedium", "campaignName"],
        metrics_list=["sessions", "conversions"]
    )

    # 4. Data Transformation Logic (The 'T' in ETL)
    print("Step 3: Transforming and Cleaning Data...")
    # Example: Filtering out 'Test' deals and calculating conversion rates
    if not deals_df.empty:
        deals_df = deals_df[deals_df['dealname'].str.contains("test", case=False) == False]
    
    if not marketing_df.empty:
        marketing_df['conversion_rate'] = (marketing_df['conversions'] / marketing_df['sessions']) * 100

    # 5. Load Data (The 'L' in ETL)
    print("Step 4: Loading Data to Local Storage/Database...")
    # In a production environment, this would be an SQL Ingestion (e.g., to PostgreSQL)
    deals_df.to_csv("data/cleaned_deals.csv", index=False)
    marketing_df.to_csv("data/marketing_performance.csv", index=False)

    print(f"--- ETL Pipeline Completed Successfully at {datetime.now()} ---")

if __name__ == "__main__":
    run_etl_pipeline()
