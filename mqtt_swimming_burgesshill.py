import pytz
import requests
from bs4 import BeautifulSoup
import json
import html
from datetime import datetime, timezone, timedelta
import paho.mqtt.client as mqtt
from secret import MQTT_USERNAME, MQTT_PASSWORD, MQTT_BROKER



MQTT_PORT = 1883  # Default port
MQTT_TOPIC_REQUEST = "swimming/availability/request"  # Topic for requests
MQTT_TOPIC_RESPONSE = "swimming/availability/response"  # Topic for responses
MQTT_CLIENT_ID = "swimming_availability_client"



REQUIRED_SWIMMING_TIME = 40
TRAVEL_TIME = 30
NUMBER_OF_SESSIONS = 2


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



def build_statement():

    UK_TIMEZONE = pytz.timezone('Europe/London')
    today = datetime.now(UK_TIMEZONE).date()  # Get the current date in UK timezone

    url = 'https://www.placesleisure.org/centres/the-triangle/centre-activities/swimming-lessons/#timetable'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    input_elem = soup.find('input', {'id': 'timetable-data'})



    if input_elem:
        raw_value = input_elem.get('value', '')
    
        # Step 3: Unescape HTML entities (if any)
        unescaped_value = html.unescape(raw_value)
    
        # Step 4: Try to load as JSON
        try:
            timetable_data = json.loads(unescaped_value)
            print("Successfully parsed timetable data!")
            # Now we can work with `timetable_data` like a normal Python object
            #print(json.dumps(timetable_data, indent=2))  # Pretty print

            swimming_sessions = timetable_data["timetables"][0]["sessions"]

	        # Filter for SWIMLANE activities in the Main Pool
            #lane_swims = [ session for session in swimming_sessions if session["ag"] == "SWIMLANE" and session["lc"] == "Main Pool"]
            #lane_swims_today = [session for session in swimming_sessions if session["ag"] == "SWIMLANE" and session["lc"] == "Main Pool" and datetime.fromisoformat(session["s"].replace("Z", "+00:00")).astimezone(UK_TIMEZONE).date() == today]

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
            next_sessions = valid_sessions[:NUMBER_OF_SESSIONS]  #next 2 sessions

            statement = []
            statement.append("Today at the Burgess Hill swimming lane pool, ")
            # Show the next two valid sessions
            for session_num, session in enumerate(next_sessions):
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
            return alexa_statement

        except json.JSONDecodeError as e:
            print("Failed to decode JSON:", e)
            print("Raw unescaped value (preview):", unescaped_value[:500])
    else:
        print("Could not find the timetable-data input.")

    return "There is an error with the web site. See a Code Doctor! Quick!"



def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    client.subscribe(MQTT_TOPIC_REQUEST)

def on_message(client, userdata, msg):
    print(f"Received request: {msg.topic} -> {msg.payload.decode()}")

    # Generate the statement when a request is received
    availability_statement = build_statement()

    # Publish the statement to the response topic
    client.publish(MQTT_TOPIC_RESPONSE, availability_statement)
    print(f"Sent response: {availability_statement}")


# Set up the MQTT client
client = mqtt.Client(MQTT_CLIENT_ID)
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

# Connect to the broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start the loop to listen for messages
client.loop_forever()

#msg = build_statement()
#print(msg)
