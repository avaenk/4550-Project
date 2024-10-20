import requests
import random
import json
import os

class question:
    def __init__ (self, topic, pointValue):
        self.question = self.generateQuestion()
        self.answer = ""
        self.topic = topic
        self.pointValue = pointValue

    def getQuestion(self):
        return self.question
    def getAnswer(self):
        return self.answer
    
    def generateQuestionAnswer(self):
        API_URL = "https://newsapi.org/v2/everything"
        API_KEY = "dd10187aee144736babe2ee903c573ba"

        # Parameters for the API request
        params = {
            "country": "us",
            "apiKey": API_KEY,
            "q": self.topic
        }

        responseDict = 0

        if os.path.exists(f"{self.topic}.json"): #if an API call on this topic has already been made,don't make another
            with open(f"{self.topic}.json", "r") as file:
                responseDict = json.load(file)
        else: 
            response = requests.get(API_URL, params=params)
            if response.status_code == 200:
                responseDict = response.json()
                with open(f"{self.topic}.json", "w") as outfile:
                    json.dump(responseDict, outfile)
            else:
                print(f"Error: {response.status_code}")

        numArticles = len(responseDict["articles"])
        if numArticles < 3 :
            return -1 #if not enough could be collected on the topic (or the call failed) signal with -1 to try again
        
        j = random.randrange(0, numArticles)
        self.question = responseDict["articles"][j]["title"]
        #still need to parse headline and form the actual question/answer
    
    def checkAnswer(self, userAnswer):
        if self.answer.lower() == userAnswer.lower():
            return self.pointValue
        else:
            return 0