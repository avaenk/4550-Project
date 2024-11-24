import requests
import random
import json
import os
import string

class Question:
    def __init__ (self, topic, pointValue):
        self.question = ""
        self.answer = ""

        self.topic = topic
        self.pointValue = pointValue

        self.generateQuestionAnswer()
    def getQuestion(self):
        return self.question
    def getAnswer(self):
        return self.answer
    
    def generateQuestionAnswer(self):
        API_URL = "https://newsapi.org/v2/everything"
        API_KEY = "dd10187aee144736babe2ee903c573ba"

        # Parameters for the API request
        params = {
            "apiKey": API_KEY,
            "q": self.topic,
            "language": "en"
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
                return -1

        numArticles = len(responseDict["articles"])
        if numArticles < 3 :
            return -1 #if not enough could be collected on the topic (or the call failed) signal with -1 to try again
        
        j = random.randrange(0, numArticles)
        rawQuestion = responseDict["articles"][j]["description"]
        questionArr = list()
        lastI = 0
        for i in range(len(rawQuestion)):
            if not rawQuestion[i].isalnum():
                questionArr.append(rawQuestion[lastI:i])
                questionArr.append(rawQuestion[i])
                lastI = i + 1

        answerIndex = -1
        for i in range(1, len(questionArr)): #find first proper noun
            if len(questionArr[i]) > 1 and questionArr[i][0].isupper():
                if questionArr[i-2] not in {".", "?", "!"} and questionArr[i].lower() not in {"the", "when","then","this", "in", "a", "an", "for", "that", "she", "he", "her", "it", "its", "his", "him", "hers", "them", "they","yet","from","with","here","there","about","above","across","against","along","among","around","at","before","behind","beneath","below","beside","between","beyond","by"}:
                    answerIndex = i
                    break

        if answerIndex == -1: # if no proper nouns found
            maxLength = 0
            for i in range(len(questionArr)):
                if len(questionArr[i]) > maxLength:
                    maxLength = len(questionArr[i])
                    answerIndex = i
        self.answer = questionArr[answerIndex]

        rawTitle = responseDict["articles"][j]["title"] + ": "
        titleArr = list()
        lastI = 0
        for i in range(len(rawTitle)):
            if not rawTitle[i].isalnum():
                titleArr.append(rawTitle[lastI:i])
                titleArr.append(rawTitle[i])
                lastI = i + 1

        for i in range(len(titleArr)):
            if titleArr[i] != self.answer:
                self.question += titleArr[i]
            else:
                for j in range(len(titleArr[i])):
                    self.question += "_"

        for i in range(len(questionArr)):
            if questionArr[i] != self.answer:
                self.question += questionArr[i]
            else:
                for j in range(len(questionArr[i])):
                    self.question += "_"
  

    def checkAnswer(self, userAnswer):
        if self.answer.lower() == userAnswer.lower():
            return self.pointValue
        else:
            return 0
