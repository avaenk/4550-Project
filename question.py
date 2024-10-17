class question:
    def __init__ (self, pointValue):
        self.generateQuestion()
        self.pointValue = pointValue

    def getQuestion(self):
        return self.question
    def getAnswer(self):
        return self.answer
    
    def generateQuestionAnswer(self):
        self.question = "What color is the sky?"
        self.answer = "blue"
    
    def checkAnswer(self, userAnswer):
        if self.answer.lower() == userAnswer.lower():
            return self.pointValue
        else:
            return 0

class dateQuestion(question):
    def __init__(self, pointValue):
        self.generateQuestionAnswer()
        super.pointValue = pointValue
        
    def generateQuestionAnswer(self):
        self.question = "What date was the Declaration of Independence signed? MM/DD/YYYY"
        self.answerMonth = 8
        self.answerDay = 2
        self.answerYear = 1776

    def checkAnswer(self, userAnswer):
        score = 0
        userMonth = eval(userAnswer[0:2])
        userDay = eval(userAnswer[3:5])
        userYear = eval(userAnswer[6:])
        score = score + abs(self.answerMonth - userMonth)
        score = score + abs(self.answerDay - userDay)
        score = score + abs(self.answerYear - userYear)
        return score
    
class peopleQuestion(question):
    def __init__(self, pointValue):
        self.generateQuestionAnswer()
        super.pointValue = pointValue
    
    def generateQuestionAnswer(self):
        self.question = "Who was the first president? FirstName LastName"
        self.answer = ["George", "Washington"]
    
    def checkAnswer(self, userAnswer):
        score = 0
        userAnswerArr = userAnswer.split()
        for i in range(len(self.answer)):
            if self.answer[i].lower() == userAnswer[i].lower():
                score = score + self.pointValue
            else:
                for a in userAnswer:
                    if self.answer[i].lower() == a.lower():
                        score = score + self.pointValue/2 # half points for having the right name in there somewhere

class placeQuestion(question):
    def __init__(self, pointValue):
        self.generateQuestionAnswer()
        super.pointValue = pointValue
    
    def generateQuestionAnswer(self):
        self.question = "What is the capital of Arkansaa"
        self.answer = ["Little Rock"]
    
    def checkAnswer(self, userAnswer):
        score = 0
        userAnswerArr = userAnswer.split()
        for i in range(len(self.answer)):
            if self.answer[i].lower() == userAnswer[i].lower():
                score = score + self.pointValue
            else:
                for a in userAnswer:
                    if self.answer[i].lower() == a.lower():
                        score = score + self.pointValue/2 # half points for having the right name in there somewhere