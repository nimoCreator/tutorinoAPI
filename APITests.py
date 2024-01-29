import unittest
import requests

class TestGetMyOffersAPI(unittest.TestCase):

    # Test case for retrieving offers
    def test_get_my_offers(self):
        # Set session and user IDs for the test
        session_id = "00000"
        user_id = "1"

        # Make a GET request to the getOffers API endpoint
        response = requests.get(
            f"http://173.212.216.164:5555/getOffers?sessionID={session_id}&userID={user_id}"
        )

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Parse the response JSON and assert that it contains the 'offers' key
        data = response.json()
        self.assertIn("offers", data) 

    # Test case for user login
    def test_login(self):
        # Set login credentials for the test
        login_or_email = "user"
        password = "password"

        # Prepare data for the login request
        data = {"login_or_email": login_or_email, "password": password}

        # Make a POST request to the login API endpoint
        response = requests.post("http://173.212.216.164:5555/login", json=data)

        # Assert that the response status code is either 200 or 401
        self.assertIn(response.status_code, [200, 401])
        data = response.json()

        # If the login is successful (status code 200)
        if response.status_code == 200:
            self.assertIn("access_token", data)  
            self.assertEqual(data["token_type"], "bearer")
        # If the login fails (status code 401)
        elif response.status_code == 401:
            self.assertIn("detail", data) 
            self.assertEqual(data["detail"], "Invalid login or email")

    # Test case for user registration
    def test_register(self):
        # Set registration credentials for the test
        login = "user"
        email = "newuser@gmail.com"
        password = "password"

        # Prepare data for the registration request
        data = {"login": login, "email": email, "password": password}

        # Make a POST request to the register API endpoint
        response = requests.post("http://173.212.216.164:5555/register", json=data)

        # Assert that the response status code is either 200 or 409
        self.assertIn(response.status_code, [200, 409])

        data = response.json()

        # If registration is successful (status code 200)
        if response.status_code == 200:
            self.assertIn("access_token", data)
            self.assertEqual(data["token_type"], "bearer")
        # If registration fails (status code 409)
        elif response.status_code == 409:
            self.assertIn("error", data)
            self.assertEqual(data["error"], "Login or email already exists in the database")

    # Test case for validating a session
    def test_validate_session(self):
        # Set a session ID for the test
        session_id = "00000"

        # Make a GET request to the validateSession API endpoint
        response = requests.get(f"http://173.212.216.164:5555/validateSession?sessionID={session_id}")

        # Assert that the response status code is either 200 or 409
        self.assertIn(response.status_code, [200, 409])

        data = response.json()

        # If session validation is successful (status code 200)
        if response.status_code == 200:
            self.assertIn("message", data)
            self.assertEqual(data["message"], "session valid")
        # If session validation fails (status code 409)
        elif response.status_code == 409:
            self.assertIn("error", data)
            self.assertEqual(data["error"], "Session ID wrong or expired")

    # Test case for adding a session (success)
    def test_session_add_success(self):
        # Set user ID for the test
        data = {"userID": "123"}

        # Make a POST request to the addSession API endpoint
        response = self.app.post("http://173.212.216.164:5555/addSession", json=data)

        # Parse the JSON response and assert that it contains 'sessionId'
        json_data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("sessionId", json_data)

       # Test case for adding a session (failure)
    def test_session_add_failure(self):
        # Set invalid user ID for the test
        data = {"userID": "invaliduser"}

        # Make a POST request to the addSession API endpoint
        response = self.app.post("http://173.212.216.164:5555/addSession", json=data)

        # Parse the JSON response and assert that it returns a status code 409
        json_data = response.get_json()
        self.assertEqual(response.status_code, 409)

        # Assert that the JSON response contains an 'error' key
        self.assertIn("error", json_data)

        # Assert that the 'error' key in the response contains the expected message
        self.assertEqual(json_data["error"], "Failed to add new session")

    # Test case for accessing the root endpoint ("/")
    def test_hello(self):
        # Make a GET request to the root endpoint
        response = self.app.get("http://173.212.216.164:5555/")

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the response data (decoded UTF-8) is equal to the expected string "Hello"
        self.assertEqual(response.data.decode("utf-8"), "Hello")

    # Test case for retrieving data from the "/ogloszenie" endpoint
    def test_get_ogloszenie(self):
        # Make a GET request to the "/ogloszenie" endpoint
        response = self.app.get("http://173.212.216.164:5555/ogloszenie")

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response and assert that it is an instance of a list
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    # Test case for retrieving data from the "/operator" endpoint
    def test_get_operator(self):
        # Make a GET request to the "/operator" endpoint
        response = self.app.get("http://173.212.216.164:5555/operator")

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response and assert that it is an instance of a list
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    # Test case for retrieving data from the "/przedmioty" endpoint
    def test_get_przedmioty(self):
        # Make a GET request to the "/przedmioty" endpoint
        response = self.app.get("http://173.212.216.164:5555/przedmioty")

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response and assert that it is an instance of a list
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    # Test case for retrieving data from the "/rating" endpoint
    def test_get_rating(self):
        # Make a GET request to the "/rating" endpoint
        response = self.app.get("http://173.212.216.164:5555/rating")

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response and assert that it is an instance of a list
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    # Test case for retrieving data from the "/reports" endpoint
    def test_get_reports(self):
        # Make a GET request to the "/reports" endpoint
        response = self.app.get("http://173.212.216.164:5555/reports")

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response and assert that it is an instance of a list
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    # Test case for retrieving data from the "/uczen" endpoint
    def test_get_uczen(self):
        # Make a GET request to the "/uczen" endpoint
        response = self.app.get("http://173.212.216.164:5555/uczen")

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response and assert that it is an instance of a list
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    # Test case for retrieving data from the "/users" endpoint
    def test_get_users(self):
        # Make a GET request to the "/users" endpoint
        response = self.app.get("http://173.212.216.164:5555/users")

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response and assert that it is an instance of a list
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    # Test case for retrieving data from the "/wiadomosci" endpoint
    def test_get_wiadomosci(self):
        # Make a GET request to the "/wiadomosci" endpoint
        response = self.app.get("http://173.212.216.164:5555/wiadomosci")

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response and assert that it is an instance of a list
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    # Test case for retrieving data from the "/korepetytor" endpoint
    def test_get_korepetytor(self):
        # Make a GET request to the "/korepetytor" endpoint
        response = self.app.get("http://173.212.216.164:5555/korepetytor")

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response and assert that it is an instance of a list
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    # Test case for retrieving data from the "/korepetycje" endpoint
    def test_get_korepetycje(self):
        # Make a GET request to the "/korepetycje" endpoint
        response = self.app.get("http://173.212.216.164:5555/korepetycje")

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response and assert that it is an instance of a list
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    # Test case for retrieving data from the "/seen_by" endpoint
    def test_get_seen_by(self):
        # Make a GET request to the "/seen_by" endpoint
        response = self.app.get("http://173.212.216.164:5555/seen_by")

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response and assert that it is an instance of a list
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    # Test case for retrieving data from the "/konwersacje" endpoint
    def test_get_konwersacje(self):
        # Make a GET request to the "/konwersacje" endpoint
        response = self.app.get("http://173.212.216.164:5555/konwersacje")

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response and assert that it is an instance of a list
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

      # Test case for retrieving data from the "/czlonkowie_konwersacji" endpoint
    def test_get_czlonkowie_konwersacji(self):
        # Make a GET request to the "/czlonkowie_konwersacji" endpoint
        response = self.app.get("http://173.212.216.164:5555/czlonkowie_konwersacji")

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response and assert that it is an instance of a list
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    # Test case for retrieving data from the "/korepetytor_profile" endpoint for a specific user ID (1 in this case)
    def test_get_korepetytor_profile(self):
        # Make a GET request to the "/korepetytor_profile/1" endpoint
        response = self.app.get("http://173.212.216.164:5555/korepetytor_profile/1")

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response and assert that it is an instance of a dictionary
        json_data = response.get_json()
        self.assertIsInstance(json_data, dict)

    # Test case for retrieving user-specific conversations from the "/konwersacje" endpoint for a specific user ID (1 in this case)
    def test_get_konwersacje_uzytkownika(self):
        # Make a GET request to the "/konwersacje/1" endpoint
        response = self.app.get("http://173.212.216.164:5555/konwersacje/1")

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response and assert that it is an instance of a list
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    # Test case for retrieving messages from a specific conversation ID (1 in this case) using the "/wiadomosci" endpoint
    def test_get_wiadomosci_konwersacji(self):
        # Make a GET request to the "/wiadomosci/1" endpoint
        response = self.app.get("http://173.212.216.164:5555/wiadomosci/1")

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response and assert that it is an instance of a list
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    # Test case for retrieving korepetycje (tutoring sessions) for a specific korepetytor (user ID 1 in this case)
    def test_get_korepetytor_korepetycje(self):
        # Make a GET request to the "/korepetycje_k/1" endpoint
        response = self.app.get("http://173.212.216.164:5555/korepetycje_k/1")

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response and assert that it is an instance of a list
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

    # Test case for retrieving korepetycje (tutoring sessions) for a specific uczenn (user ID 1 in this case)
    def test_get_uczen_korepetycje(self):
        # Make a GET request to the "/korepetycje_u/1" endpoint
        response = self.app.get("http://173.212.216.164:5555/korepetycje_u/1")

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response and assert that it is an instance of a list
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)

if __name__ == '__main__':
    unittest.main()