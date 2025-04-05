import httpx
import secret

url = "https://api.notifymyecho.com/v1/NotifyMe"
vm_payload = {
            "accessCode": secret.NOTIFICATIONS_TOKEN,
            "notification": "WELL DONE! YOUR NOTIFICATION IS WORKING!!"
		}
response = httpx.post(url, params = vm_payload) #headers = headers)

print(response.status_code)

if response.status_code != 401:
  print("Response Code:",response.status_code, "Notification triggered successfully!")
else:
  print("Error:", response.text)




