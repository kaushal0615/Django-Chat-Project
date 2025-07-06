from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from apps.chat.models import Room, Message


class MessageApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.base_url = "/api/chat"
        self.messages_url = f"{self.base_url}/messages"

        # Create test user and room
        self.user = User.objects.create_user(username="alice", password="testpass")
        self.room = Room.objects.create(name="general")

    def test_create_message_success(self):
        payload = {
            "username": self.user.username,
            "room": self.room.name,
            "content": "Hello from test!"
        }
        response = self.client.post(self.messages_url, payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Hello from test!")
        self.assertTrue(Message.objects.filter(content="Hello from test!").exists())

    def test_create_message_invalid_user(self):
        payload = {
            "username": "nonexistent_user",
            "room": self.room.name,
            "content": "Should fail"
        }
        response = self.client.post(self.messages_url, payload, format="json")
        self.assertEqual(response.status_code, 404)
        self.assertIn("User not found", response.json()["detail"])

    def test_create_message_invalid_room(self):
        payload = {
            "username": self.user.username,
            "room": "no-room",
            "content": "Should fail"
        }
        response = self.client.post(self.messages_url, payload, format="json")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Room not found", response.json()["detail"])

    def test_get_all_messages(self):
        Message.objects.create(user=self.user, room=self.room, content="Msg 1")
        Message.objects.create(user=self.user, room=self.room, content="Msg 2")
        response = self.client.get(self.messages_url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()), 2)

    def test_get_messages_for_room(self):
        Message.objects.create(user=self.user, room=self.room, content="Room msg")
        room_messages_url = f"{self.base_url}/rooms/{self.room.id}/messages"
        response = self.client.get(room_messages_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["room"], self.room.name)
        self.assertEqual(response.json()[0]["username"], self.user.username)
