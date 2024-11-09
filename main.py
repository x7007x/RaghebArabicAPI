import requests
import random
from fake_useragent import UserAgent

def process_questions(data):
    temp = []

    if data["success"]:
        results = data["result"]
        exam_id = results["id"]
        questions = results["questions"]

        for question in questions:
            question_id = question["id"]
            answers = question["answers"]

            temp_answer = []
            for answer in answers:
                answer_id = answer["id"]
                temp_answer.append(answer_id)

            temp.append({"id": question_id, 'answer_id': random.choice(temp_answer)})
    return temp

def get_correct_answers(data):
    temp = []

    if data["success"]:
        result = data["result"]
        exam = result["exam"]["exam"]
        exam_id = exam["id"]
        exam_title = exam["title"]
        questions = exam["questions"]

        for question in questions:
            question_id = question["id"]
            answers = question["answers"]

            for answer in answers:
                if answer["is_correct"]:
                    answer_id = answer["id"]
                    temp.append({"id": question_id, 'answer_id': answer_id})
    return temp

class RaghebArabicAPI:
    def __init__(self, mobile=None, password=None, token=None):
        self.base_url = 'https://apis.ragheb-arabic.com'
        self.headers = {
            'authority': 'apis.ragheb-arabic.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'origin': 'https://student.ragheb-arabic.com',
            'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': UserAgent().random,
            'content-type': 'application/json'
        }
        self.token = token
        self.mobile = mobile
        self.password = password
        if token:
            self.headers['authorization'] = f'Bearer {self.token}'

    def login(self):
        json_data = {
            'mobile': self.mobile,
            'password': self.password,
        }
        response = requests.post(f'{self.base_url}/auth/login', headers=self.headers, json=json_data)
        data = response.json()
        if data.get('success'):
            self.token = data['result']['token']
            self.headers['authorization'] = f'Bearer {self.token}'
        return data

    def get_public_exams(self, page=1, is_public=True):
        params = {
            'page': str(page),
            'public': str(is_public).lower(),
        }
        response = requests.get(f'{self.base_url}/user/public-exams', params=params, headers=self.headers)
        return response.json()

    def start_exam(self, exam_id):
        response = requests.post(f'{self.base_url}/user/exams/start/{exam_id}', headers=self.headers)
        return response.json()

    def get_exam(self, exam_id):
        response = requests.get(f'{self.base_url}/user/exams/{exam_id}', headers=self.headers)
        return response.json()

    def submit_answers(self, exam_id, questions, result=0):
        json_data = {
            'questions': questions,
            'id': str(exam_id),
            'result': result,
        }
        response = requests.post(f'{self.base_url}/user/exams/correct', headers=self.headers, json=json_data)
        return response.json()

    def get_user_exam_result(self, result_id):
        response = requests.get(f'{self.base_url}/user/exams/my/{result_id}', headers=self.headers)
        return response.json()


api = RaghebArabicAPI(mobile="", password="")
login_response = api.login()
