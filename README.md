# Listen out for Sporting Opportunties. Using Alexa VoiceMonkey, NotifyMe and Ntfy Service

Fed up of missing that vital notification when waiting for Padel/Tennis or Swimming opportunities?

Using a simple Python script - you can automate checking particular emails and/or checking websites from your sports provider and make announcements on your Echo Dot/Alexa Devices

**Voice Monkey** and **Notify Me** are third-party skills that allows you to create and trigger customised Alexa routines and announcements. 

Essentially these skills and their associated webservices acts as a bridge between your devices, services, or apps and Alexa's ecosystem. 

When enabled you can easily make your Alexa devices announce specific messages. For example, you can send a message to Alexa to say "There are Padel Opportunities today at 10:30 AM" on all Echo devices in your home.

**Please Note:**

Announcements using an Alexa skills is only one part of the automation process when checking facilities on your local sports centre's website. You will also need additional scripts (written in Python or Javascript).
to check out those sporting opportunities that match your requirement are available. 

I have given two example scripts here as demonstrations.  One for **Hove's Padel and Tennis** website and the other for **Burgess Hill Triangle Sports Complex**.



# Voicemonkey Alexa Skill - Dynamic Announcements Setup Guide


## 1. Create a Voice Monkey Account
1. **Go to the Voice Monkey website**:  
   Visit [voicemonkey.io](https://voicemonkey.io) and sign up for a free account.
   
2. **Log in to your account**:  
   After signing up, log in to access the Voice Monkey dashboard.

---

## 2. Enable the Voice Monkey Alexa Skill
1. **Open the Alexa App**:  
   On your smartphone or desktop, open the Amazon Alexa app or visit the [Alexa Skills page](https://alexa.amazon.com).

2. **Search for the Voice Monkey Skill**:  
   In the Alexa app, navigate to "Skills & Games" and search for "Voice Monkey."

3. **Enable the Skill**:  
   Click on the Voice Monkey skill and enable it. 

4. **Link your Voice Monkey Account**:  
   When prompted, sign in with your Voice Monkey credentials to link your account to the Alexa skill.

---

## 3. Generate Your First Monkey
Monkeys in Voice Monkey act like virtual buttons or triggers.

1. **Go to the Monkeys Tab**:  
   In the Voice Monkey dashboard, navigate to the "Monkeys" section.

2. **Create a New Monkey**:  
   - Click "Add New Monkey."
   - Give your monkey a name (e.g., "Announce Dinner").
   - This name will be used to trigger actions in routines or announcements.

3. **Save the Monkey**:  
   After naming it, click "Save." The new monkey will now appear in your list.

---

## 4. Use Monkeys in Alexa Routines
1. **Open the Alexa App**:  
   Go to the "Routines" section.

2. **Create a New Routine**:  
   - Click the "+" icon to create a new routine.
   - Add a trigger (e.g., voice command, schedule, or event).
   - In the actions section, select "Smart Home," then "Voice Monkey," and choose the monkey you created.

3. **Customize the Routine**:  
   Add additional actions, such as playing music, announcing messages, or controlling smart devices.

4. **Save the Routine**:  
   Test the routine to ensure it works as expected.

---

## 5. Send Announcements Programmatically
Voice Monkey allows you to send announcements or trigger routines via HTTP requests.

1. **Generate an API Key**:  
   - In the Voice Monkey dashboard, go to the API section.
   - Generate an API key and note down the details.

2. **Use the API**:  
   You can make HTTP requests to trigger monkeys or send announcements to Alexa devices. Here's an example using `httpx` in Python:

   ```python
   import httpx

   api_key = "your_api_key"
   access_token = "your_access_token"
   monkey_name = "Announce Dinner"

   response = httpx.get(
       "https://api.voicemonkey.io/trigger",
       params={
           "key": api_key,
           "token": access_token,
           "monkey": monkey_name
       }
   )

   if response.status_code == 200:
       print("Announcement triggered successfully!")
   else:
       print("Error:", response.text)


## NotifyMe Alexa Skill - Static Notifications Setup Guide


The NotifyMe Alexa skill allows you to send notifications directly to your Alexa devices. Here's how to set it up:

---

## 1. Enable the NotifyMe Skill
1. **Open the Alexa App**:  
   On your smartphone or desktop, open the Amazon Alexa app or visit the [Alexa Skills page](https://alexa.amazon.com).

2. **Search for the NotifyMe Skill**:  
   In the Alexa app, navigate to "Skills & Games" and search for "NotifyMe."

3. **Enable the Skill**:  
   - Click on the NotifyMe skill and enable it.
   - Log in or create an account when prompted.

---

## 2. Link Your NotifyMe Account
1. **Log in to the NotifyMe Dashboard**:  
   Go to [NotifyMe Dashboard](https://www.notifymyecho.com) and log in with your account credentials.

2. **Copy Your API Key**:  
   After logging in, you’ll see your unique API key. This key is required to send notifications to your Alexa devices.

---

## 3. Sending Notifications
NotifyMe provides a simple HTTP API for sending notifications. Here’s how to use it:

### Using Curl

Send a notification directly from the command line:
```bash
curl -X POST https://api.notifymyecho.com/v1/NotifyMe \
-H "Content-Type: application/json" \
-d '{
  "notification": "Your custom message here",
  "accessCode": "your_api_key"
}'
```

### Using Python

```python

import httpx

api_url = "https://api.notifymyecho.com/v1/NotifyMe"
api_key = "your_api_key"
message = "This is a test notification from NotifyMe."

response = httpx.post(
    api_url,
    json={
        "notification": message,
        "accessCode": api_key
    }
)

if response.status_code == 200:
    print("Notification sent successfully!")
else:
    print(f"Error: {response.status_code} - {response.text}")

```


Altenatively, read the document **Amazon-Alexa-Access-Code-Guide.pdf** found in the docs folder (courtesey of Protesus.com). This gives instructions on how to set up notifications on your alexa devices.

Make sure you copy your notificatoins token into your **configure.py** file.

Run the test script **testnotify.py** from the command console. 

**python3 testnotify.py**

If you've registered your skill correctly and copied your token into configure.py - you should get a notification on your Alexa device(s).

As per instructions in the protesus documents -

**Alexa device will not announce the message aloud upon receiving the notification. It will simply make a beep and light up the ring indicating that there are new notifications available. Amazon for safety and privacy reasons controls this. When the ring lights up, you need to ask Alexa using your normal wake word,**

**“Alexa, Do I have any notifications?”, "Alexa, What are my notifications?" or “Alexa, read my notifications”.**

**To delete notifications from your Alexa device, you can say**

**“Alexa, delete my notifications”.**


## Don't have any Alexa devices?

With minimal Python skills you can modify the routine **notify_opportunities** to use your host computer's speaker.

Below is one example of a method I found with a google search.

Install pygame and gtts python modules.

* pip3 install gtts
* pip3 install pygame


```python
from gtts import gTTS
import pygame
import io
import tempfile

def notifyme_announce(text):
    # Create a gTTS object and get the speech as an in-memory stream
    tts = gTTS(text)
    speech_stream = io.BytesIO()
    tts.write_to_fp(speech_stream)

    # Save the in-memory stream to a temporary file
    temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_audio_file.write(speech_stream.getvalue())
    temp_audio_file.close()

    # Load and play the audio from the temporary file
    pygame.mixer.music.load(temp_audio_file.name)
    pygame.mixer.music.play()

    # Wait for the audio to finish
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


pygame.init()
notify_opportunities("You have 1 Padel opportunity!")
pygame.quit()

```





# Padel 
Padel Bat Hove Website watcher. Example source  - **WATCH THIS SPACE FOR UPDATES**
```
python3 padel.py
```

# Triangle Burgess Hill.
Mqtt watcher - (need to populate secret.py with credentials)
```

# MQTT Credentials (replace with your credentials)
MQTT_BROKER = "109-120-108-53.ip.linodeusercontent.com"  # MQTT Broker address (change to your broker if necessary)
MQTT_USERNAME = "YOUR MQTT USERNAME HERE"
MQTT_PASSWORD = "YOUR MQTT PASSWORD HERE"

# Notify Me (token emailed to you when you sign up for notifications service)
NOTIFICATIONS_TOKEN='amzn1.ask.account.AFEAOJZMICR3TK6JS7BPM6YSQGNSD33RSVARHDRVFBESNUZTZEOF5TFVQMXT5PVEZDCYRPHMYX6VCDA4ZWU76YQFTR5ZM6EEDT3V3GSJPFWUVGRRG6S6TCS3EEN4IGDQ6DY'

# Voice Monkey
VOICEMONKEY_TOKEN="8c98ca46fd8438160672c08072b4755c_04729b5326ed9"
VOICEMONKEY_DEVICE="nicks-echo-device"

```

To run

```
python3 mqtt_swimming_burgesshill.py
```

or to test website with a one off call to the Triangle website use

```
python3 swimming_burgesshill.py
```



