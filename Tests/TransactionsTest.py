import unittest
import requests
import json

class TestAvailableController(unittest.TestCase):
    BASE_URL = "https://tutorino.ddns.net:888/api/Transactions"
    transaction_id = None
    
    def setUp(self) -> None:
         return super().setUp()

    def tearDown(self) -> None:
         return super().tearDown()\
    
    def test_1_new_transaction(self):
        trans_data = {
            "status": "test",
            "ouid": 9,
            "trans_date": "2024-06-07T12:39:31.220Z",
            "value": 0.42,
            "currency": "test",
            "details": "t"
        }
        response = requests.post(f"{self.BASE_URL}/newTransaction", json=trans_data, verify=False)
        self.assertEqual(response.status_code, 200, f"Wrong response code: {response.status_code}")
        try:
            json_data = response.json()
            self.assertEqual(json_data['StatusCode'], 0, f"Unexpected StatusCode in json response: {json_data['StatusCode']}")
            self.assertEqual(json_data['ErrorMessage'], 'Transaction added', f"Unexpected ErrorMessage: {json_data['ErrorMessage']}")
        except ValueError:
            self.fail(f"Response is not a valid JSON: {response.text}")
    
    def test_2_get_last_transaction(self):
        trans_data = {
            "ouid": 9
        }
        response = requests.post(f"{self.BASE_URL}/getLastTrans", json=trans_data, verify=False)
        self.assertEqual(response.status_code, 200, f"Wrong response code: {response.status_code}")
        try:
            json_data = response.json()
            self.assertIsInstance(json_data, dict, f"Unexpected response type: {type(json_data)}")
            self.assertIn('tid', json_data, "Transaction missing 'tid'")
            self.assertIn('status', json_data, "Transaction missing 'status'")
            self.assertIn('trans_date', json_data, "Transaction missing 'trans_date'")
            self.assertIn('value', json_data, "Transaction missing 'value'")
            self.assertIn('currency', json_data, "Transaction missing 'currency'")
            self.assertIn('details', json_data, "Transaction missing 'details'")
            TestAvailableController.transaction_id = json_data['tid']
        except ValueError:
            self.fail(f"Response is not a valid JSON: {response.text}")
    
    def test_3_update_transaction(self):
        trans_data = {
            "tid": TestAvailableController.transaction_id,
            "status": "updated",
            "conf_date": "2024-06-07T12:39:31.220Z"
        }
        response = requests.post(f"{self.BASE_URL}/updateTrans", json=trans_data, verify=False)
        self.assertEqual(response.status_code, 200, f"Wrong response code: {response.status_code}")
        try:
            json_data = response.json()
            self.assertEqual(json_data['StatusCode'], 0, f"Unexpected StatusCode in json response: {json_data['StatusCode']}")
            self.assertEqual(json_data['ErrorMessage'], 'Data Edited', f"Unexpected ErrorMessage: {json_data['ErrorMessage']}")
        except ValueError:
            self.fail(f"Response is not a valid JSON: {response.text}")
    
    def test_4_delete_transaction(self):
        trans_data = {
            "tid": TestAvailableController.transaction_id
        }
        response = requests.post(f"{self.BASE_URL}/DeleteTransaction", json=trans_data, verify=False)
        self.assertEqual(response.status_code, 200, f"Wrong response code: {response.status_code}")
        try:
            json_data = response.json()
            self.assertEqual(json_data['StatusCode'], 0, f"Unexpected StatusCode in json response: {json_data['StatusCode']}")
            self.assertEqual(json_data['ErrorMessage'], 'Transaction Deleted', f"Unexpected ErrorMessage: {json_data['ErrorMessage']}")
        except ValueError:
            self.fail(f"Response is not a valid JSON: {response.text}")
            
    def test_get_transaction(self):
        trans_data = {
            "ouid": 10
        }
        response = requests.post(f"{self.BASE_URL}/getTrans", json=trans_data, verify=False)
        self.assertEqual(response.status_code, 200, f"Wrong response code: {response.status_code}")
        try:
            json_data = response.json()
            self.assertIsInstance(json_data, list, f"Unexpected response type: {type(json_data)}")
            for transaction in json_data:
                self.assertIn('tid', transaction, "Transaction missing 'tid'")
                self.assertIn('status', transaction, "Transaction missing 'status'")
                self.assertIn('trans_date', transaction, "Transaction missing 'trans_date'")
                self.assertIn('value', transaction, "Transaction missing 'value'")
                self.assertIn('currency', transaction, "Transaction missing 'currency'")
                self.assertIn('details', transaction, "Transaction missing 'details'")
        except ValueError:
            self.fail(f"Response is not a valid JSON: {response.text}")

if __name__ == '__main__':
    unittest.main()
    
