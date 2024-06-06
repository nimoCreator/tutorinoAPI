import unittest
import requests
import json

class TestUsersController(unittest.TestCase):
    BASE_URL = "https://tutorino.ddns.net:888/Users"

    def setUp(self) -> None:
         return super().setUp()

    def tearDown(self) -> None:
         return super().tearDown()

    def test_get_all_users(self):
        response = requests.get(f"{self.BASE_URL}/getAllUsers", verify=False)
        self.assertEqual(response.status_code, 200,"wrong response code = {}".format(response.status_code))
        try:
            json_data = response.json()
            self.assertIsInstance(json_data, list, f"Response is not a list: {json_data}")
        except ValueError:
            self.fail(f"Response is not a valid JSON: {response.text}")
    
    def test_add_user_new(self):
            new_user = {
                "UserName": "test_new",
                "UserSurname": "test_new",
                "UserLogin": "test_new",
                "UserEmail": "test@test.test",
                "UserPassword": "test_new",
                "AccountType": "Tutor"
            }
            response = requests.post(f"{self.BASE_URL}/addUser", json=new_user, verify=False)
            self.assertEqual(response.status_code, 200, f"Unexpected status code: {response.status_code}")
            try:
                json_data = response.json()
                self.assertIsInstance(json_data, dict, f"Response is not a dictionary: {json_data}")
                self.assertEqual(json_data['StatusCode'], 0, f"Unexpected StatusCode in json response: {json_data['StatusCode']}")
                self.assertEqual(json_data['ErrorMessage'], 'Data added', f"Unexpected ErrorMessage: {json_data['ErrorMessage']}")
            except ValueError:
                self.fail(f"Response is not a valid JSON: {response.text}")

    def test_add_user_existing(self):
                existing_user = {
                    "UserName": "test1",
                    "UserSurname": "test1",
                    "UserLogin": "test1",
                    "UserEmail": "test1",
                    "UserPassword": "test1",
                    "AccountType": "Student"
                }
                response = requests.post(f"{self.BASE_URL}/addUser", json=existing_user, verify=False)
                self.assertEqual(response.status_code, 200, f"Unexpected status code: {response.status_code}")
                try:
                    json_data = response.json()
                    self.assertIsInstance(json_data, dict, f"Response is not a dictionary: {json_data}")
                    self.assertEqual(json_data['StatusCode'], 102, f"Unexpected StatusCode in json response: {json_data['StatusCode']}")
                    self.assertEqual(json_data['ErrorMessage'], 'User Exists', f"Unexpected ErrorMessage: {json_data['ErrorMessage']}")
                except ValueError:
                    self.fail(f"Response is not a valid JSON: {response.text}")

    def test_login_user_correct_password(self):
        user_data = {
            "Username": "test1",
            "Email": "test1",
            "Password": "test1"
        }
        response = requests.post(f"{self.BASE_URL}/loginUser", json=user_data, verify=False)
        self.assertEqual(response.status_code, 200, f"Unexpected status code: {response.status_code}")
        try:
            json_data = response.json()
            self.assertIsInstance(json_data, dict, f"Response is not a dictionary: {json_data}")
            self.assertEqual(json_data['StatusCode'], 0, f"Unexpected StatusCode in json response: {json_data['StatusCode']}")
            self.assertEqual(json_data['ErrorCode'], 'Access', f"Unexpected Message: {json_data['ErrorCode']}")
            self.assertIn('UserID', json_data, "UserID is not present in response")
        except ValueError:
            self.fail(f"Response is not a valid JSON: {response.text}")

    def test_login_user_wrong_password(self):
        user_data = {
            "Username": "test1",
            "Email": "test1",
            "Password": "incorrect_password"
        } 
        response = requests.post(f"{self.BASE_URL}/loginUser", json=user_data, verify=False)
        self.assertEqual(response.status_code, 200, f"Unexpected status code: {response.status_code}")
        try:
            json_data = response.json()
            self.assertIsInstance(json_data, dict, f"Response is not a dictionary: {json_data}")
            self.assertEqual(json_data['StatusCode'], 101, f"Unexpected StatusCode in json response: {json_data['StatusCode']}")
            self.assertEqual(json_data['ErrorCode'], 'Wrong Password', f"Unexpected Message: {json_data['ErrorCode']}")
            self.assertEqual(json_data['UserID'], 0, f"UserId should be 0 instead of: {json_data['UserID']}")
        except ValueError:
            self.fail(f"Response is not a valid JSON: {response.text}")

    def test_login_user_no_user(self):
        user_data = {
            "Username": "nonexistent_user",
            "Email": "nonexistent@example.com",
            "Password": "password"
        }
        response = requests.post(f"{self.BASE_URL}/loginUser", json=user_data, verify=False)
        self.assertEqual(response.status_code, 200, f"Unexpected status code: {response.status_code}")
        try:
            json_data = response.json()
            self.assertIsInstance(json_data, dict, f"Response is not a dictionary: {json_data}")
            self.assertEqual(json_data['StatusCode'], 100, f"Unexpected StatusCode in json response: {json_data['StatusCode']}")
            self.assertEqual(json_data['ErrorCode'], 'No User', f"Unexpected Message: {json_data['ErrorCode']}")
            self.assertEqual(json_data['UserID'], 0, f"UserId should be 0 instead of: {json_data['UserID']}")
        except ValueError:
            self.fail(f"Response is not a valid JSON: {response.text}")

    def test_change_func_student(self):
        user_data = {
            "userID": 9,
            "AccountType": "Student"
        }
        response = requests.post(f"{self.BASE_URL}/changeFunction", json=user_data, verify=False)
        self.assertEqual(response.status_code, 200, f"Unexpected status code: {response.status_code}")
        try:
            json_data = response.json()
            self.assertIsInstance(json_data, dict, f"Response is not a dictionary: {json_data}")
            self.assertEqual(json_data['StatusCode'], 0, f"Unexpected StatusCode in json response: {json_data['StatusCode']}")
            self.assertEqual(json_data['ErrorMessage'], 'Data added', f"Unexpected Message: {json_data['ErrorMessage']}")
        except ValueError:
            self.fail(f"Response is not a valid JSON: {response.text}")

    def test_edit_profile_successful(self):
        user_data = {
            "userID": 9,
            "birthdate": "1990-01-01",
            "pfp": ""
        }
        response = requests.post(f"{self.BASE_URL}/editProfile", json=user_data, verify=False)
        self.assertEqual(response.status_code, 200, f"Unexpected status code: {response.status_code}")
        try:
            json_data = response.json()
            self.assertIsInstance(json_data, dict, f"Response is not a dictionary: {json_data}")
            self.assertEqual(json_data['StatusCode'], 0, f"Unexpected StatusCode in json response: {json_data['StatusCode']}")
            self.assertEqual(json_data['ErrorMessage'], 'Data Edited', f"Unexpected Message: {json_data['ErrorMessage']}")
        except ValueError:
            self.fail(f"Response is not a valid JSON: {response.text}")

    def test_edit_profile_nonexisting_user(self):
        user_data = {
            "userID": 0,
            "birthdate": "1990-01-01",
            "pfp": "abc"
        }
        response = requests.post(f"{self.BASE_URL}/editProfile", json=user_data, verify=False)
        self.assertEqual(response.status_code, 200, f"Unexpected status code: {response.status_code}{response.content}")
        try:
            json_data = response.json()
            self.assertIsInstance(json_data, dict, f"Response is not a dictionary: {json_data}")
            self.assertEqual(json_data['StatusCode'], 100, f"Unexpected StatusCode in json response: {json_data['StatusCode']}")
            self.assertEqual(json_data['ErrorMessage'], 'No Data Found', f"Unexpected Message: {json_data['ErrorMessage']}")
        except ValueError:
            self.fail(f"Response is not a valid JSON: {response.text}")

if __name__ == '__main__':
    unittest.main()