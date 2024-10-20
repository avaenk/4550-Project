import requests
import random
import json
import os
from datetime import date

# API endpoint and key
API_URL = "https://newsapi.org/v2/everything"
API_KEY = "dd10187aee144736babe2ee903c573ba"

# Parameters for the API request
params = {
    "q": "tesla",
    "apiKey": API_KEY,
    #can also add in data specifications
}

responseDict = 0
if os.path.exists('sample.json'):
    with open('sample.json', 'r') as file:
        responseDict = json.load(file)
else: #if an API call has already been made, for testing purposes, don't make another
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        responseDict = response.json()
        with open("sample.json", "w") as outfile:
            json.dump(responseDict, outfile)
    else:
        print(f"Error: {response.status_code}")

numArticles = len(responseDict["articles"])
cache = []

for i in range(3):
    j = random.randrange(0, numArticles)
    while j not in cache:
        print(responseDict["articles"][j]["title"])
        cache.append(j)
