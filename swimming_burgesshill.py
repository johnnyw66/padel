import pytz
import requests
from bs4 import BeautifulSoup
import json
import html
from datetime import datetime, timezone, timedelta

REQUIRED_SWIMMING_TIME = 40
TRAVEL_TIME = 30


site_id = '149'  # The Triangle

def check_availability(activity_id, location_id, start_datetime_iso):
    url = (
        "https://www.placesleisure.org/umbraco/api/timetables/getgladstoneavailability"
        f"?activityId={activity_id}"
        f"&siteId={site_id}"
        f"&locationId={location_id}"
        f"&startDate={start_datetime_iso}"
    )
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json'
    }

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        json_data = r.json()

        if json_data.get("success") and json_data["data"]:
            slot = json_data["data"][0]  # Usually one per call
            return {
                "availability": slot.get("availability"),
                "status": slot.get("status"),
                "bookableFrom": slot.get("bookableFrom")
            }
        else:
            return {"availability": None, "status": "Unavailable"}

    except Exception as e:
        print(f"Error checking availability for {activity_id}: {e}")
        return {"availability": None, "status": "Error"}

url = 'https://www.placesleisure.org/centres/the-triangle/centre-activities/swimming-lessons/#timetable'
headers = {
    'User-Agent': 'Mozilla/5.0'
}

# Step 1: Get the page
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

input_elem = soup.find('input', {'id': 'timetable-data'})

UK_TIMEZONE = pytz.timezone('Europe/London')

#today = datetime.now(timezone.utc).date()
today = datetime.now(UK_TIMEZONE).date()  # Get the current date in UK timezone
print("TODAY ", today)

if input_elem:
    raw_value = input_elem.get('value', '')
    
    # Step 3: Unescape HTML entities (if any)
    unescaped_value = html.unescape(raw_value)
    
    # Step 4: Try to load as JSON
    try:
        timetable_data = json.loads(unescaped_value)
        print("Successfully parsed timetable data!")
        # Now you can work with `timetable_data` like a normal Python object
        #print(json.dumps(timetable_data, indent=2))  # Pretty print

        swimming_sessions = timetable_data["timetables"][0]["sessions"]

	    # Filter for SWIMLANE activities in the Main Pool
        lane_swims = [ session for session in swimming_sessions if session["ag"] == "SWIMLANE" and session["lc"] == "Main Pool"]
        lane_swims_today = [session for session in swimming_sessions if session["ag"] == "SWIMLANE" and session["lc"] == "Main Pool" and datetime.fromisoformat(session["s"].replace("Z", "+00:00")).astimezone(UK_TIMEZONE).date() == today]

        statement = []
	    # Pretty print
        for session in lane_swims_today:
            #start = datetime.fromisoformat(session["s"].replace("Z", "+00:00"))
            #end = datetime.fromisoformat(session["e"].replace("Z", "+00:00"))
            start = datetime.fromisoformat(session["s"].replace("Z", "+00:00")).astimezone(UK_TIMEZONE)
            end = datetime.fromisoformat(session["e"].replace("Z", "+00:00")).astimezone(UK_TIMEZONE)

            info = check_availability(session["aId"], session["al"], session["s"])
            print(f"{start:%H:%M}–{end:%H:%M} @ {session['lc']} ({session['ag']}) – Places Remaining: {info['availability']}")
            alexa_statement = ' '.join(statement)      
            ##statement.append(f"At the {start:%H:%M} session, there are {info['availability']} places available.")

        #print(f"ALEXA {alexa_statement}")

        # You have 40 minutes to travel, and need 30 minutes to swim
        travel_time = timedelta(minutes=TRAVEL_TIME)
        minimum_swim_time = timedelta(minutes=REQUIRED_SWIMMING_TIME)

        # Get current time (UTC)
        now = datetime.now(timezone.utc)

        # Filter for valid sessions: starting at least 40 minutes from now and lasting 30 mins or more
        valid_sessions = []
        lane_swims = [ session for session in swimming_sessions if session["ag"] == "SWIMLANE" and session["lc"] == "Main Pool"]

        for session in lane_swims:
            # Convert session start and end times to datetime objects
            start = datetime.fromisoformat(session["s"].replace("Z", "+00:00")).astimezone(UK_TIMEZONE)
            end = datetime.fromisoformat(session["e"].replace("Z", "+00:00")).astimezone(UK_TIMEZONE)

            # Ensure session starts at least 40 minutes from now
            if start >= now + travel_time and end - start >= minimum_swim_time:
                valid_sessions.append(session)

        # Sort sessions by start time and pick the first two
        valid_sessions.sort(key=lambda x: datetime.fromisoformat(x["s"].replace("Z", "+00:00")))
        next_two_sessions = valid_sessions[:2]

        statement = []
        statement.append("Today at the Burgess Hill swimming lane pool, ")
        # Show the next two valid sessions
        for session_num, session in enumerate(next_two_sessions):

            start = datetime.fromisoformat(session["s"].replace("Z", "+00:00")).astimezone(UK_TIMEZONE)
            end = datetime.fromisoformat(session["e"].replace("Z", "+00:00")).astimezone(UK_TIMEZONE)

            info = check_availability(session["aId"], session["al"], session["s"])
            print(f"{start:%Y-%m-%d %H:%M}–{end:%H:%M} @ {session['lc']} ({session['ag']}) "
                  f"– {info['availability']} places remaining, Status: {info['status']}")

            if session_num == 0:
                statement.append(f"At the {start:%H:%M} session, there are {info['availability']} places available.")
            # Add the second session with "Following that"
            else:
                statement.append(f"Following that, at the {start:%H:%M} swim lane session, there are {info['availability']} places available.")

        alexa_statement = " ".join(statement)
        print(f"Alexa Statement: '{alexa_statement}'")

    except json.JSONDecodeError as e:
        print("Failed to decode JSON:", e)
        print("Raw unescaped value (preview):", unescaped_value[:500])
else:
    print("Could not find the timetable-data input.")



