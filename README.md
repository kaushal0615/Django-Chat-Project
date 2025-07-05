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

