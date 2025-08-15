# 📡 Live Chat API (FastAPI + WebSockets + Celery)

A real-time chat backend built using **FastAPI**, **PostgreSQL (async)**, **WebSockets**, and **Celery + Redis** for background tasks.  

---

## 🚀 Features

- **Async FastAPI** backend
- **PostgreSQL** database using SQLAlchemy Async + asyncpg
- **Real-time messaging** over WebSockets
- **Multi-client broadcasting** using the `broadcaster` package
- **Chat history API**
- **Background notifications** via Celery + Redis
- **Typing indicators** in real-time
- **Message delivery & read status updates**
- **Pytest coverage** for REST & WebSocket endpoints
- Ready for deployment on **AWS EC2** or **Heroku**

---

## 🛠 Tech Stack

| Layer               | Technology                                  |
|---------------------|---------------------------------------------|
| **Backend**         | FastAPI                                     |
| **Database**        | PostgreSQL (SQLAlchemy Async + asyncpg)     |
| **Real-time**       | WebSockets + broadcaster                      |
| **Background Jobs** | Celery + Redis                              |
| **Testing**         | pytest, pytest-asyncio, httpx, websockets   |
| **Deployment**      | AWS EC2 / Heroku                            |

---

## 🏗 Architecture

1. **API Layer**  
   - REST APIs for chat history & user operations  
   - WebSocket endpoint for real-time events  

2. **Database Layer**  
   - Stores users and messages  
   - Tracks delivery/read status for each message  

3. **Real-time Layer**  
   - `broadcaster` package for pub/sub messaging  
   - Supports in-memory or Redis-based broadcasting  

4. **Background Layer**  
   - Celery worker triggered on new messages  
   - Sends push/email notifications asynchronously  

---

## 📋 Database Schema

```mermaid
    User ||--o{ Message : sends
    User {
        int id PK
        string username
    }
    Message {
        int id PK
        string content
        datetime timestamp
        bool delivered
        bool read
        int sender_id FK
    }
```

## 🔌 API Endpoints
### REST
| Method	| Endpoint          | Description           
| ------ | ----------------- | ------------------ |
| **GET**| /chat/history?limit=50	| Fetch recent chat messages

### WebSockets
 Endpoint          | Description           
 ----------------- | ------------------ |
|/ws/chat	| Send & receive real-time events

## 📤 WebSocket Event Format
#### Send a message
```json
{
  "type": "message",
  "sender_id": 1,
  "content": "Hello!"
}
```
#### Typing indicator
```json
{
  "type": "typing",
  "user_id": 1
}
```
#### Update message status
```json
{
  "type": "status_update",
  "message_id": 5,
  "delivered": true,
  "read": false
}
```

## ⚙️ Local Development
### 1️⃣ Clone & Install
```bash
git clone https://github.com/miteshtiwary123/live-chat-fastapi.git
cd live-chat-fastapi
pip install -r requirements.txt
```
### 2️⃣ Setup Environment
Create a .env file:
```bash
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/live_chat

```
### 3️⃣ Run FastAPI
```bash
uvicorn app.main:app --reload
```
### 4️⃣ Run Redis
```bash
redis-server
```
### 5️⃣ Start Celery Worker
```bash
celery -A app.celery_app.celery worker --loglevel=info
```

## 📜 License
MIT License — free to use & modify.

## 🤝 Contributing
Pull requests are welcome! If you find bugs or want new features, open an issue first.

## 👨‍💻 Author
Built by ***Mitesh Tiwary*** as part of an advanced FastAPI real-time project series.
