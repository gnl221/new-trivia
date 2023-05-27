import requests
import json

class QuestionFetcher:
    def __init__(self):
        self.api_url = "https://opentdb.com/api.php?amount=1&type=multiple"
        self.backup_questions = json.load(open("questions.json"))

    def fetch_question(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()
            question = data["results"][0]["question"]
            correct_answer = data["results"][0]["correct_answer"]
            incorrect_answers = data["results"][0]["incorrect_answers"]
            answers = [correct_answer] + incorrect_answers
            return question, answers
        except (requests.RequestException, KeyError):
            return self.get_backup_question()

    def get_backup_question(self):
        question_data = self.backup_questions.pop()
        question = question_data["question"]
        correct_answer = question_data["correct_answer"]
        incorrect_answers = question_data["incorrect_answers"]
        answers = [correct_answer] + incorrect_answers
        return question, answers
