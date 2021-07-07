import json
import random
import requests

quiz_file = open('quiz.json', 'r')
quiz = json.load(quiz_file)


# print(quiz['results'][random.randint(0, 9)]['question'])/

# questions_file = open('questions.text', "w")
# for each in range(0, 9):
#     questions_file.write(f"{quiz['results'][each]['question']}\n")
# questions_file.close()


