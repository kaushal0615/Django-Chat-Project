from rest_framework.test import APITestCase, APIClient
from apps.chat.models import Room


class RoomApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.base_url = "/api/chat"
        self.room_list_url = f"{self.base_url}/rooms"
        self.room_data = {"name": "test-room"}

    def test_create_room_success(self):
        response = self.client.post(self.room_list_url, self.room_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], self.room_data["name"])
        self.assertTrue(Room.objects.filter(name="test-room").exists())

    def test_create_duplicate_room(self):
        Room.objects.create(name="test-room")
        response = self.client.post(self.room_list_url, self.room_data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Room already exists", response.json()["detail"])

    def test_list_rooms(self):
        Room.objects.create(name="room1")
        Room.objects.create(name="room2")
        response = self.client.get(self.room_list_url)
        self.assertEqual(response.status_code, 200)

        room_names = [r["name"] for r in response.json()]
        self.assertIn("room1", room_names)
        self.assertIn("room2", room_names)
