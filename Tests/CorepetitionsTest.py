import unittest
import requests
import json

class TestAvailableController(unittest.TestCase):
    BASE_URL = "https://tutorino.ddns.net:888/api/Corepetitions"
    
    def setUp(self) -> None:
         return super().setUp()

    def tearDown(self) -> None:
         return super().tearDown()

    def test_get_all_corepetitions(self):
        response = requests.get(f"{self.BASE_URL}/getAllComps", verify=False)
        self.assertEqual(response.status_code, 200,"wrong response code = {}".format(response.status_code))
        try:
            json_data = response.json()
            self.assertIsInstance(json_data, list, f"Response is not a list: {json_data}")
        except ValueError:
            self.fail(f"Response is not a valid JSON: {response.text}")

    def test_get_corepetition(self):
        request_body = {
        "zuid": 7
        }
        response = requests.post(f"{self.BASE_URL}/getCorepetition", json=request_body, verify=False)
        self.assertEqual(response.status_code, 200,"wrong response code = {}".format(response.status_code))
        try:
            json_data = response.json()
            self.assertIsInstance(json_data, dict, f"Response is not a dicitonary: {json_data}")
        except ValueError:
            self.fail(f"Response is not a valid JSON: {response.text}")
        
    def test_new_corepetition(self):
        new_corepetition = {
            "teacher": 10,
            "pupil": 9,
            "subject": "math",
            "level": 0,
            "status": "string",
            "start": "2024-06-08T05:56:17.983Z",
            "end": "2024-06-08T05:56:17.983Z",
            "time": 0,
            "price": 0,
            "currency": "string",
            "form": "T",
            "meet_link": "string",
            "table_link": "string",
            "localization": "string",
            "accepted_o": True,
            "accepted_k": True,
            "paid_in_cash": True,
            "trainsaction_id": 39
        }
        response = requests.post(f"{self.BASE_URL}/newCorepetition", json=new_corepetition, verify=False)
        self.assertEqual(response.status_code, 200, f"Unexpected status code: {response.status_code}")
        try:
            json_data = response.json()
            self.assertIsInstance(json_data, dict, f"Response is not a dictionary: {json_data}")
            self.assertEqual(json_data['StatusCode'], 0, f"Unexpected StatusCode in json response: {json_data['StatusCode']}")
            self.assertEqual(json_data['ErrorMessage'], 'Corepetition added', f"Unexpected ErrorMessage: {json_data['ErrorMessage']}")
        except ValueError:
            self.fail(f"Response is not a valid JSON: {response.text}")
    
    def test_edit_corepetition(self):
        edit_corepetition = {
            "zuid": 24,
            "teacher": 9,
            "pupil": 9,
            "subject" : "math",
            "level": 0,
            "status": "test_changed",
            "start": "2024-06-08T06:01:54.965Z",
            "end": "2024-06-08T06:01:54.965Z",
            "time": 0,
            "price": 100,
            "currency": "test",
            "form": "T",
            "meet_link": "test",
            "table_link": "test",
            "localization": "test",
            "accepted_o": True,
            "accepted_k": True,
            "paid_in_cash": True,
            "trainsaction_id": 39
        }
        response = requests.post(f"{self.BASE_URL}/editCorepetition", json=edit_corepetition, verify=False)
        self.assertEqual(response.status_code, 200, f"Unexpected status code: {response.status_code}")
        try:
            json_data = response.json()
            self.assertIsInstance(json_data, dict, f"Response is not a dictionary: {json_data}")
            self.assertEqual(json_data['StatusCode'], 0, f"Unexpected StatusCode in json response: {json_data['StatusCode']}")
            self.assertEqual(json_data['ErrorMessage'], 'Corepetition edited', f"Unexpected ErrorMessage: {json_data['ErrorMessage']}")
        except ValueError:
            self.fail(f"Response is not a valid JSON: {response.text}")
    
    def test_delete_corepetition(self):
        request_body = {
        "zuid": 26
        }
        response = requests.post(f"{self.BASE_URL}/DeleteCorepetition", json=request_body, verify=False)
        self.assertEqual(response.status_code, 200,"wrong response code = {}".format(response.status_code))
        try:
            json_data = response.json()
            self.assertIsInstance(json_data, dict, f"Response is not a dicitonary: {json_data}")
            self.assertEqual(json_data['StatusCode'], 0, f"Unexpected StatusCode in json response: {json_data['StatusCode']}")
            self.assertEqual(json_data['ErrorMessage'], 'Corepetition Deleted', f"Unexpected ErrorMessage: {json_data['ErrorMessage']}")
        except ValueError:
            self.fail(f"Response is not a valid JSON: {response.text}")

if __name__ == '__main__':
    unittest.main()