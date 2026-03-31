import requests
import time
import os
import pandas as pd

class HubSpotConnector:
    """
    Custom Python Wrapper for HubSpot CRM API.
    Designed to handle large-scale data extraction with automated pagination.
    """
    def __init__(self, access_token):
        """
        Initialize the connector using a Private App Access Token.
        """
        self.base_url = "https://api.hubapi.com/crm/v3/objects/"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

    def get_all_records(self, object_type, properties_list):
        """
        Extracts all records for a specified object type.
        Implements cursor-based pagination logic.
        """
        all_results = []
        after = None
        endpoint_url = f"{self.base_url}{object_type}"
        
        params = {
            "limit": 100,
            "archived": "false",
            "properties": properties_list.split(',')
        }

        print(f"Extraction Started: {object_type}")

        while True:
            if after:
                params['after'] = after
            
            try:
                response = requests.get(endpoint_url, headers=self.headers, params=params)
                
                if response.status_code != 200:
                    print(f"Error {response.status_code}: {response.text}")
                    break
                    
                data = response.json()
                batch = data.get('results', [])
                
                # Flatten the 'properties' dictionary for each record
                for record in batch:
                    flattened_record = record.get('properties', {})
                    flattened_record['hubspot_id'] = record.get('id')
                    all_results.append(flattened_record)
                
                paging = data.get('paging')
                if paging and 'next' in paging:
                    after = paging['next'].get('after')
                else:
                    break
                
                time.sleep(0.1) # Rate limiting protection
                
            except Exception as e:
                print(f"Connection Error: {str(e)}")
                break

        print(f"Extraction Completed: {len(all_results)} records retrieved.")
        return pd.DataFrame(all_results)

# --- Modular Configuration ---
# It is recommended to set these variables in your system environment or a .env file
HUBSPOT_TOKEN = os.getenv('HUBSPOT_TOKEN')

# Define target properties for extraction
CONFIG = {
    "deals": {
        "properties": "hs_forecast_amount, amount,closedate,dealname,dealstage, pipeline,hubspot_owner_id",
        "output_file": "deals_data.csv"
    },
    "contacts": {
        "properties": "email,firstname,lastname, city, country,jobtitle,lifecyclestage,createdate",
        "output_file": "contacts_data.csv"
    }
}

def main():
    if not HUBSPOT_TOKEN:
        print("Error: HUBSPOT_TOKEN environment variable is not set.")
        return

    connector = HubSpotConnector(HUBSPOT_TOKEN)

    for obj_type, settings in CONFIG.items():
        # Execute extraction and return a Pandas DataFrame
        df = connector.get_all_records(obj_type, settings["properties"])
        
        # Save to CSV for audit trail or local analysis
        if not df.empty:
            df.to_csv(settings["output_file"], index=False)
            print(f"Data for {obj_type} saved to {settings['output_file']}")

if __name__ == "__main__":
    main()
