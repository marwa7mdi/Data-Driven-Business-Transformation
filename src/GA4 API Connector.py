import os
import pandas as pd
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    OrderBy
)

class GoogleAnalyticsConnector:
    """
    GA4 API Connector to fetch custom marketing reports.
    """
    def __init__(self, property_id, credentials_path):
        """
        Initialize the client using Service Account credentials.
        """
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        self.client = BetaAnalyticsDataClient()
        self.property_id = f"properties/{property_id}"

    def get_report(self, start_date, end_date, dimensions_list, metrics_list):
        """
        Queries GA4 for specific dimensions and metrics.
        Returns a cleaned Pandas DataFrame.
        """
        request = RunReportRequest(
            property=self.property_id,
            dimensions=[Dimension(name=d) for d in dimensions_list],
            metrics=[Metric(name=m) for m in metrics_list],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        )

        print(f"Fetching GA4 report for property: {self.property_id}")
        
        try:
            response = self.client.run_report(request)
            return self._parse_response(response)
        except Exception as e:
            print(f"GA4 API Error: {str(e)}")
            return pd.DataFrame()

    def _parse_response(self, response):
        """
        Private method to parse the GA4 JSON response into a tabular format.
        """
        data = []
        for row in response.rows:
            row_data = {}
            # Extract Dimensions
            for i, dimension_value in enumerate(row.dimension_values):
                dim_name = response.dimension_headers[i].name
                row_data[dim_name] = dimension_value.value
            
            # Extract Metrics
            for i, metric_value in enumerate(row.metric_values):
                met_name = response.metric_headers[i].name
                row_data[met_name] = float(metric_value.value)
            
            data.append(row_data)
        
        return pd.DataFrame(data)

# --- Configuration ---
GA4_PROPERTY_ID = os.getenv('GA4_PROPERTY_ID') # Get from environment variable
CREDENTIALS_FILE = "service_account.json" # Path to your Google Cloud JSON key

def main():
    if not GA4_PROPERTY_ID:
        print("Error: GA4_PROPERTY_ID not set.")
        return

    ga4 = GoogleAnalyticsConnector(GA4_PROPERTY_ID, CREDENTIALS_FILE)

    # Example: Analyze Conversion by Session Source/Medium
    # This addresses your goal of analyzing keyword intent and conversion lift
    dimensions = ["sessionSourceMedium", "landingPagePlusQueryString"]
    metrics = ["sessions", "conversions", "totalRevenue"]

    df = ga4.get_report(
        start_date="2025-01-01", 
        end_date="today", 
        dimensions_list=dimensions, 
        metrics_list=metrics
    )

    if not df.empty:
        # Calculate Conversion Rate within Python for quick insights
        df['conversion_rate'] = (df['conversions'] / df['sessions']) * 100
        df.to_csv("ga4_marketing_performance.csv", index=False)
        print("GA4 data exported successfully to ga4_marketing_performance.csv")

if __name__ == "__main__":
    main()
