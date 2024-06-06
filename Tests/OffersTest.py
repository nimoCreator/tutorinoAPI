import unittest
import requests
import json

class TestOffers(unittest.TestCase):
    BASE_URL = "https://tutorino.ddns.net:888/api/Offers"

    def setUp(self) -> None:
         return super().setUp()

    def tearDown(self) -> None:
         return super().tearDown()
     
    def test_get_all_offers(self):
        subject = {"subjectName": "string"}
        response = requests.post(f"{self.BASE_URL}/getAllOffers", json=subject, verify=False)
        self.assertEqual(response.status_code, 200,"wrong response code = {}".format(response.status_code))
        try:
            json_data = response.json()
            self.assertIsInstance(json_data, list, f"Response is not a list: {json_data}")
        except ValueError:
            self.fail(f"Response is not a valid JSON: {response.text}")
     
    def test_get_add_offer(self):
        new_offer ={
            "userID": 9,
            "subjectID": 2,
            "price": 0.52,
            "description": "test_offer"
            }
        response = requests.post(f"{self.BASE_URL}/addOffer", json=new_offer, verify=False)
        self.assertEqual(response.status_code, 200,"wrong response code = {}".format(response.status_code))
        try:
            json_data = response.json()
            self.assertIsInstance(json_data, dict, f"Response is not a dict: {json_data}")
            self.assertEqual(json_data['StatusCode'], 0, f"Unexpected StatusCode in json response: {json_data['StatusCode']}")
            self.assertEqual(json_data['ErrorMessage'], 'Data added', f"Unexpected ErrorMessage: {json_data['ErrorMessage']}")
        except ValueError:
            self.fail(f"Response is not a valid JSON: {response.text}")
        
    def test_get_offer(self):
        offer_id ={"id": 21}
        response = requests.post(f"{self.BASE_URL}/getOffer", json=offer_id, verify=False)
        self.assertEqual(response.status_code, 200,"wrong response code = {}".format(response.status_code))
        try:
            json_data = response.json()
            self.assertIsInstance(json_data, list, f"Response is not a list: {json_data}")
        except ValueError:
            self.fail(f"Response is not a valid JSON: {response.text}")
        

if __name__ == '__main__':
    unittest.main()