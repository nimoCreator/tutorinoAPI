import unittest
import requests
import json

class TestAvailableController(unittest.TestCase):
    BASE_URL = "https://tutorino.ddns.net:888/api/Available"

    def setUp(self) -> None:
         return super().setUp()

    def tearDown(self) -> None:
         return super().tearDown()
    
    def test_add_available(self):
        aval_data = {
            "user_uuid": 9,
            "weekday": 0,
            "begin": 1,
            "end": 2,
            "valid_from": "2024-06-06T09:04:27.975Z",
            "valid_until": "2024-06-06T10:04:27.975Z"
        }
        response = requests.post(f"{self.BASE_URL}/AddAvailable", json=aval_data, verify=False)
        self.assertEqual(response.status_code, 200, f"Wrong response code: {response.status_code}")
        try:
            json_data = response.json()
            self.assertEqual(json_data['StatusCode'], 0, f"Unexpected StatusCode in json response: {json_data['StatusCode']}")
            self.assertEqual(json_data['ErrorMessage'], "Available added", f"Unexpected ErrorMessage: {json_data['ErrorMessage']}")
        except ValueError:
            self.fail(f"Response is not a valid JSON: {response.text}")
    
    # def test_edit_available(self):
    #     aval_change_data = {
    #         "aid": i,
    #         "user_uuid": 10
    #     }
    #     response = requests.post(f"{self.BASE_URL}/editAval", json=aval_change_data, verify=False)
    #     self.assertEqual(response.status_code, 200, f"Wrong response code: {response.status_code}")
    #     try:
    #         json_data = response.json()
    #         self.assertEqual(json_data['StatusCode'], 0, f"Unexpected StatusCode in json response: {json_data['StatusCode']}")
    #         self.assertEqual(json_data['ErrorMessage'], "Data Edited", f"Unexpected ErrorMessage: {json_data['ErrorMessage']}")
    #     except ValueError:
    #         self.fail(f"Response is not a valid JSON: {response.text}")
    
    def test_get_available(self):
        uuid = {
            "user_uuid" : 9
        }
        response = requests.post(f"{self.BASE_URL}/getAval", json=uuid, verify=False)
        self.assertEqual(response.status_code, 200, f"Wrong response code: {response.status_code}")
        try:
            json_data = response.json()
            self.assertIsInstance(json_data, list, f"Response is not a list: {json_data}")
            self.assertEqual(json_data['StatusCode'], 0, f"Unexpected StatusCode in json response: {json_data['StatusCode']}")
            self.assertEqual(json_data['ErrorMessage'], 'Data added', f"Unexpected ErrorMessage: {json_data['ErrorMessage']}")
        except ValueError:
            self.fail(f"Response is not a valid JSON: {response.text}")

if __name__ == '__main__':
    unittest.main()
