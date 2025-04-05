
# https://api.matchi.com/facilities/resources/17521/availabilities?startDateTime=2025-04-05T08%3A00%3A00.000%2B01%3A00&endDateTime=2025-04-05T22%3A00%3A00.000%2B01%3A00

import requests
import re
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

def get_api_key_from_page(facility_url: str) -> str:
    """
    Scrapes the facility page and tries to extract the x-api-key from the content.
    Args:
        facility_url (str): The full URL to the facility's page on Matchi.com

    Returns:
        str: Extracted API key, or None if not found.
    """
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(facility_url, headers=headers)
    response.raise_for_status()

    # Try to find x-api-key using regex (based on observed patterns)
    match = re.search(r'api-key\s*=\s*([^>]+)', response.text)
    print(f"KEY IS <{match.group(1)}>")    
    if match:
        return match.group(1).strip()
    else:
        print("API key not found in the main page HTML.")
        return None

def get_matchi_availability(resource_id: int, start: datetime, end: datetime, api_key: str):
    """
    Fetch availability for a given Matchit facility resource ID and time range.
    Args:
        resource_id (int): The Matchit resource ID (e.g., 17521 'TENNIS COURT 1').
        start (datetime): Start datetime (timezone-aware).
        end (datetime): End datetime (timezone-aware).
        api_key (str): The x-api-key to authenticate with the Matchi API.

    Returns:
        dict: JSON response with availability data.
    """
    start_str = quote(start.isoformat(timespec="milliseconds"))
    end_str = quote(end.isoformat(timespec="milliseconds"))

    url = (
        f"https://api.matchi.com/facilities/resources/{resource_id}/availabilities"
        f"?startDateTime={start_str}&endDateTime={end_str}"
    )

    headers = {
        "x-api-key": api_key,
        "User-Agent": "Mozilla/5.0"
    }

    print(f"Requesting: {url}")
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_resources(api_key:str):
    resource_url = 'https://api.matchi.com/facilities/2668/resources'
    headers = {
        "x-api-key": api_key,
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(resource_url, headers=headers)
    response.raise_for_status()
    return response.json()

    

# --- Example usage ---
if __name__ == "__main__":
    # Parameters
    # Step 1: Get API key
    facility_url = "https://www-game4padel-com.filesusr.com/html/3adcad_81a68fcda74844458f8203a1bb2e9a30.html"
    api_key = get_api_key_from_page(facility_url)
    if not api_key:
        print("Failed to retrieve API key.")
        exit(1)

    court_type = "TENNIS"
    #court_type = "PADEL"
    # Get Resources for our centre    
    resources = get_resources(api_key)
    filtered_resource_ids = [resource["id"] for resource in resources if court_type in resource["type"]]

    #print("+++++++++++++++++++++++++++++++++++++")
    #for resource in filtered_resources:
    #    print(resource)


    # Time range: April 16, 2025, from 08:00 to 22:00 (UTC+1)
    tz = timezone(timedelta(hours=1))
    month = 4
    day = 7
    start_dt = datetime(2025, month, day, 8, 0, 0, tzinfo=tz)
    end_dt = datetime(2025, month, day, 22, 0, 0, tzinfo=tz)

    
    for resource_id in filtered_resource_ids:
        # Step 2: Get availability data
        availability = get_matchi_availability(resource_id, start_dt, end_dt, api_key)
        name = [resource["name"] for resource in resources if  resource_id == resource["id"]]
        print(f"RESOURCE {resource_id} Desc: {name[0]}")
        print(availability)
        # Step 3: Print availability slots
        #for slot in availability
        for slot in availability:
            print(f"{slot['startDateTime']} to {slot['endDateTime']} — Available: {slot['price']} ")
        print("")
        print("------------------------------------------------")