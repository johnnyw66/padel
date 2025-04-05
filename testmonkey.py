import httpx
import secret


url = "https://api-v2.voicemonkey.io/announcement"

vm_payload = {
                "token": secret.VOICEMONKEY_TOKEN,    # Given to you when you set up VoiceMonkey account.
                "device": secret.VOICEMONKEY_DEVICE,   # Make sure this is set up with one of your valid device aliases that in your voice monkey account.
                "text": "WELL DONE! YOUR VOICEMONKEY IS WORKING!!"
}

response = httpx.get(url, params = vm_payload)
if response.status_code == 200:
    print("Announcement triggered successfully!")
else:
    print("Error:", response.text)




