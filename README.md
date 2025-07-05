# Django Real-Time Chat Application

A real-time chat application built with Django, Django Ninja (Fast API layer), and WebSockets using Django Channels. The app supports:

- User registration and login
- Public chat rooms
- Private 1-on-1 messaging
- Group chats with room membership management
- Real-time messaging with typing indicators
  

## Features

### User Features
- Register and login using username/password
- Create chat rooms
- Join or get added to group chat rooms
- Send real-time messages via WebSockets
- See typing indicators from others in the same room

### Chat Types
- Public Room Chat: anyone can send messages
- Private Chat: one-on-one communication
- Group Chat: restricted to room members only
  

## Tech Stack

| Layer         | Technology                 |
|---------------|-----------------------------|
| Backend       | Django, Django Ninja (API) |
| Real-time     | Django Channels (WebSocket) |
| Database      | SQLite |
| Auth          | Django's built-in auth system |
| API Schema    | Pydantic/Ninja `Schema` |
| Testing Tools | Postman (WebSocket Support) |


## API Endpoints (via NinjaAPI)

Base URL: `http://127.0.0.1:8000/api/`

### User
- `POST /register` — Register user  
- `POST /login` — Login user  
- `GET /users` — List all users  

### Messages
- `GET /messages` — List all messages  
- `POST /messages` — Send a message  
- `GET /rooms/{room_id}/messages` — Get messages in a room  

### Rooms
- `GET /rooms` — List all rooms  
- `POST /rooms` — Create a new room  
- `POST /rooms/with-members` — Create a room with specific users  

## WebSocket Endpoints

Uses a WebSocket client like Postman or browser.

| Type     | URL Pattern                                    |
|----------|------------------------------------------------|
| Public   | `ws://127.0.0.1:8000/ws/chat/<room_name>/`     |
| Private  | `ws://127.0.0.1:8000/ws/private/<username>/`   |
| Group    | `ws://127.0.0.1:8000/ws/chat/group/<room_name>/` |


## How to Use the Application

### Prerequisites:

Ensure the server is running:
python manage.py runserver

## Step 1: Register Users

Endpoint: POST /api/register

Request Body:
{
  "username": "ila",
  "password": "password123"
}

This registers users to the system.

## Step 2: Login Users

Endpoint: POST /api/login

Request Body:
{
  "username": "ila",
  "password": "password123"
}

A successful response means login is verified.

## Step 3: Create a Group Chat Room with Members

Endpoint: POST /api/rooms/with-members

Request Body:
{
  "name": "friends",
  "members": ["ila", "kaushal"]
}
Now both users are part of the "friends" chat room.


## Step 4: Connect to WebSocket for Group Chat

WebSocket URL (in Postman):
ws://127.0.0.1:8000/ws/chat/group/friends/

Connect using Postman’s "New WebSocket Request".

## Step 5: Send a Group Message

WebSocket message (JSON format):
{
  "username": "ila",
  "message": "Hey everyone!"
}

All members in the "friends" room will receive this message in real-time.

![image](https://github.com/user-attachments/assets/2d4c71f4-12dc-4820-ac78-c8032a886465)

