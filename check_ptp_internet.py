#Python scrfip that checks the status of a remote link by pinging the IP address.
#Based on the status of the link, send appropriate discord notificaitons and change LIFX bulb color via API.

import requests
import os
import creds
from discordwebhook import Discord


def main():
    bulb_api_key = creds.lifx_api_key    
    status = get_remote_status(creds.remote_ip_address)
    
    if status == 0:
        color = 'white'        
    else:        
        color = 'red'
        send_discord_notification("@everyone - Remote Link down")
        
    change_lifx_bulb_color(bulb_api_key,color)    
    print ("done")
    
    
    
def send_discord_notification(message_text):
    print ("entering discord")
    url = creds.discord_webhook_url
    print (url)
    discord = Discord(url = creds.discord_webhook_url)
    discord.post(content=message_text)
    print ("exiting discord")


def get_remote_status(ip_address):
        remote_status = os.system("ping -c 1 " + ip_address)
        return remote_status

def change_lifx_bulb_color(api_key,color):
    headers = {"Authorization": "Bearer " + api_key}
    payload = {"color": color}
    l = requests.put(url="https://api.lifx.com/v1/lights/all/state/", data=payload, headers=headers)
    
    
#Main Code Execution
main()

