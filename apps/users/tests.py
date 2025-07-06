from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from apps.users.schemas import RegisterSchema, LoginSchema


class UserApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = "/api/users/register"
        self.login_url = "/api/users/login"
        self.users_url = "/api/users/users"
        self.user_data = {
            "username": "testuser",
            "password": "testpass123"
        }

    def test_register_user_success(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], self.user_data["username"])
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_register_user_duplicate(self):
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Username already taken", response.json()['detail'])

    def test_login_user_success(self):
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Login successful")

    def test_login_user_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            "username": "wrong",
            "password": "wrong"
        }, format="json")
        self.assertEqual(response.status_code, 401)
        # import pdb; pdb.set_trace();
        self.assertIn("Invalid credentials", response.json()['detail'])

    def test_list_users(self):
        User.objects.create_user(username="user1", password="pass1")
        User.objects.create_user(username="user2", password="pass2")
        response = self.client.get(self.users_url)
        
        self.assertEqual(response.status_code, 200)

        usernames = [u["username"] for u in response.json()]
        self.assertIn("user1", usernames)
        self.assertIn("user2", usernames)
