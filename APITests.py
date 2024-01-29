import unittest
import requests

class TestGetMyOffersAPI(unittest.TestCase):

    def test_get_my_offers(self):
        session_id = "00000"
        user_id = "1"

        response = requests.get(
            f"http://173.212.216.164:5555/getOffers?sessionID={session_id}&userID={user_id}"
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("offers", data) 

    def test_login(self):
        login_or_email = "user"
        password = "password"

        data = {"login_or_email": login_or_email, "password": password}

        response = requests.post("http://173.212.216.164:5555/login", json=data)

        self.assertIn(response.status_code, [200, 401])
        data = response.json()

        if response.status_code == 200:
            self.assertIn("access_token", data)  
            self.assertEqual(data["token_type"], "bearer")
        elif response.status_code == 401:
            self.assertIn("detail", data) 
            self.assertEqual(data["detail"], "Invalid login or email")
            
if __name__ == '__main__':
    unittest.main()