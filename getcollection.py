import requests
import json

def get_collection(api_key, uuid, profile_name):
    # Get the collection amount from the Hypixel API
    url = f"https://api.hypixel.net/skyblock/profiles?key={api_key}&uuid={uuid}"
    response = requests.get(url)
    data = json.loads(response.text)

    # Find the required profile
    profile = None
    for p in data["profiles"]:
        if p["cute_name"] == profile_name:
            profile = p
            break

    # Get the collection amount
    collection = profile["members"][uuid]["collection"]["REDSTONE"]

    return collection
