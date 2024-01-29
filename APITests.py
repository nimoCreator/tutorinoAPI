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

    def test_register(self):
        login = "user"
        email = "newuser@gmail.com"
        password = "password"

        data = {"login": login, "email": email, "password": password}

        response = requests.post("http://173.212.216.164:5555/register", json=data)

        self.assertIn(response.status_code, [200, 409])

        data = response.json()
        if response.status_code == 200:
            self.assertIn("access_token", data)
            self.assertEqual(data["token_type"], "bearer")
        elif response.status_code == 409:
            self.assertIn("error", data)
            self.assertEqual(data["error"], "Login or email already exists in the database")

    def test_validate_session(self):
        session_id = "00000"

        response = requests.get(f"http://173.212.216.164:5555/validateSession?sessionID={session_id}")

        self.assertIn(response.status_code, [200, 409])

        data = response.json()
        if response.status_code == 200:
            self.assertIn("message", data)
            self.assertEqual(data["message"], "session valid")
        elif response.status_code == 409:
            self.assertIn("error", data)
            self.assertEqual(data["error"], "Session ID wrong or expired")

    def test_session_add_success(self):
        data = {"userID": "123"}

        response = self.app.post("http://173.212.216.164:5555/addSession", json=data)

        json_data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("sessionId", json_data)

    def test_session_add_failure(self):
        data = {"userID": "invaliduser"}

        response = self.app.post("http://173.212.216.164:5555/addSession", json=data)

        json_data = response.get_json()
        self.assertEqual(response.status_code, 409)
        self.assertIn("error", json_data)
        self.assertEqual(json_data["error"], "Failed to add new session")

    def test_hello(self):
        response = self.app.get("http://173.212.216.164:5555/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "Hello")

    def test_get_ogloszenie(self):
        response = self.app.get("http://173.212.216.164:5555/ogloszenie")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    def test_get_operator(self):
        response = self.app.get("http://173.212.216.164:5555/operator")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    def test_get_przedmioty(self):
        response = self.app.get("http://173.212.216.164:5555/przedmioty")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    def test_get_rating(self):
        response = self.app.get("http://173.212.216.164:5555/rating")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    def test_get_reports(self):
        response = self.app.get("http://173.212.216.164:5555/reports")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    def test_get_uczen(self):
        response = self.app.get("http://173.212.216.164:5555/uczen")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    def test_get_users(self):
        response = self.app.get("http://173.212.216.164:5555/users")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    def test_get_wiadomosci(self):
        response = self.app.get("http://173.212.216.164:5555/wiadomosci")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    def test_get_korepetytor(self):
        response = self.app.get("http://173.212.216.164:5555/korepetytor")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    def test_get_korepetycje(self):
        response = self.app.get("http://173.212.216.164:5555/korepetycje")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    def test_get_seen_by(self):
        response = self.app.get("http://173.212.216.164:5555/seen_by")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    def test_get_konwersacje(self):
        response = self.app.get("http://173.212.216.164:5555/konwersacje")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    def test_get_czlonkowie_konwersacji(self):
        response = self.app.get("http://173.212.216.164:5555/czlonkowie_konwersacji")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    def test_get_korepetytor_profile(self):
        response = self.app.get("http://173.212.216.164:5555/korepetytor_profile/1")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIsInstance(json_data, dict)

    def test_get_konwersacje_uzytkownika(self):
        response = self.app.get("http://173.212.216.164:5555/konwersacje/1")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    def test_get_wiadomosci_konwersacji(self):
        response = self.app.get("http://173.212.216.164:5555/wiadomosci/1")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    def test_get_korepetytor_korepetycje(self):
        response = self.app.get("http://173.212.216.164:5555/korepetycje_k/1")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    def test_get_uczen_korepetycje(self):
        response = self.app.get("http://173.212.216.164:5555/korepetycje_u/1")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

if __name__ == '__main__':
    unittest.main()