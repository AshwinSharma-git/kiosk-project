import gspread
import os
import json # <--- ADDED THIS IMPORT
from oauth2client.service_account import ServiceAccountCredentials # Keep this if other parts of your code might use it, but not directly used for env var loading
import datetime

# Removed CREDS_PATH as we will now use environment variables

def get_google_sheets_client():
    """
    Get authenticated Google Sheets client using credentials from environment variables.
    This function is designed for secure deployment on platforms like Render.
    """
    try:
        # Get the JSON string of your credentials from the environment variable
        credentials_json_string = os.environ.get("GOOGLE_CREDENTIALS_JSON_STRING")

        if credentials_json_string:
            # If the environment variable exists, parse the JSON string into a Python dictionary
            credentials_data = json.loads(credentials_json_string)
            
            # Authenticate gspread using the dictionary data
            gc = gspread.service_account_from_dict(credentials_data)
            return gc
        else:
            # If the environment variable is not found, it's a critical error for deployment.
            # For local development, you might have a fallback (e.g., from a local file
            # that is in your .gitignore), but for Render, this variable MUST be set.
            print("ERROR: GOOGLE_CREDENTIALS_JSON_STRING environment variable not found.")
            raise RuntimeError("Google Sheets credentials are not configured. Deployment will fail.")

    except Exception as e:
        print(f"Error authenticating Google Sheets client: {str(e)}")
        # Re-raise the exception to ensure the calling function knows authentication failed
        raise

def append_to_sheet(data_row):
    """
    Append a row of data to the Google Sheet.
    It now gets the client securely via get_google_sheets_client().
    """
    try:
        client = get_google_sheets_client() # Get the authenticated client
        # Open the spreadsheet by its title
        # IMPORTANT: Replace 'ISRO_Kiosk_Feedback' with the EXACT name of your Google Spreadsheet
        sheet = client.open('ISRO_Kiosk_Feedback').sheet1 
        sheet.append_row(data_row)
        return True
    except Exception as e:
        print(f"Error appending to sheet: {str(e)}")
        return False

def get_filtered_data(filters=None):
    """
    Get data from sheet with optional filters.
    It now gets the client securely via get_google_sheets_client().
    filters can include:
    - date_from: datetime
    - date_to: datetime
    - college: str
    - role: str
    """
    try:
        client = get_google_sheets_client() # Get the authenticated client
        # Open the spreadsheet by its title
        # IMPORTANT: Replace 'ISRO_Kiosk_Feedback' with the EXACT name of your Google Spreadsheet
        sheet = client.open('ISRO_Kiosk_Feedback').sheet1
        
        # Get all data including headers
        all_data = sheet.get_all_records()
        
        if not filters:
            return all_data
            
        filtered_data = []
        for row in all_data:
            include_row = True
            
            # Apply date filter
            if 'date_from' in filters or 'date_to' in filters:
                # Ensure 'Timestamp' column exists in your sheet and format matches
                row_date = datetime.datetime.strptime(row['Timestamp'], '%Y-%m-%d %H:%M:%S')
                
                if 'date_from' in filters and row_date < filters['date_from']:
                    include_row = False
                if 'date_to' in filters and row_date > filters['date_to']:
                    include_row = False
            
            # Apply college filter
            if 'college' in filters and filters['college'].lower() not in row['College'].lower():
                include_row = False
                
            # Apply role filter
            if 'role' in filters and filters['role'].lower() != row['Role'].lower():
                include_row = False
            
            if include_row:
                filtered_data.append(row)
                
        return filtered_data
        
    except Exception as e:
        print(f"Error getting data from sheet: {str(e)}")
        return []
