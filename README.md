# 🎬 Videoflix Backend

## 📌 Project Description

Videoflix is a video streaming backend built with Django REST Framework.  
Users can upload videos, which are automatically converted into HLS format and streamed in the frontend.

---

## ⚙️ Features

- 🔐 User Authentication (Register, Login, Logout, Activation)
- 🎬 Video Upload
- ⚡ Background Processing with Redis + RQ
- 🎥 Automatic HLS Conversion (480p, 720p, 1080p)
- 📡 Streaming via `.m3u8`
- 🍪 JWT Authentication via Cookies
- 🐳 Docker Setup

---

## 🛠️ Tech Stack

- Django
- Django REST Framework
- PostgreSQL
- Redis
- Django RQ
- FFmpeg
- Docker

---

## 🚀 Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd videoflix
````

### 2. Environment Variables

Create a `.env` file by copying the template:

```bash
cp .env.template .env
```

Then open the `.env` file and fill in your own values, for example:

* Django secret key
* database configuration
* email settings
* allowed hosts
* CSRF trusted origins

The project will not run correctly without a configured `.env` file.

---

### 3. Start Docker

```bash
docker compose up --build
```

---

## 🔗 API Endpoints

### 🔐 Authentication

| Endpoint                       | Method | Description      |
| ------------------------------ | ------ | ---------------- |
| `/api/register/`               | POST   | Register user    |
| `/api/login/`                  | POST   | Login + tokens   |
| `/api/logout/`                 | POST   | Logout           |
| `/api/token/refresh/`          | POST   | Refresh token    |
| `/api/activate/<uid>/<token>/` | GET    | Activate account |

---

### 🎬 Videos

| Endpoint      | Method | Description     |
| ------------- | ------ | --------------- |
| `/api/video/` | GET    | List all videos |
| `/api/video/` | POST   | Upload video    |

---

### 📺 Streaming (HLS)

| Endpoint                                    | Description |
| ------------------------------------------- | ----------- |
| `/api/video/<id>/<resolution>/index.m3u8`   | Playlist    |
| `/api/video/<id>/<resolution>/<segment>.ts` | Segments    |

---

## 🔄 Video Processing

After upload, the following steps happen automatically:

1. Video is saved
2. Background job is started (RQ worker)
3. FFmpeg converts video into:

   * 480p
   * 720p
   * 1080p
4. HLS files are generated (`.m3u8` + `.ts`)

---

## 🧪 Testing

### Start Frontend

Open the academy frontend locally (e.g. with Live Server):

```text
http://127.0.0.1:5500
```

### Test Flow

1. Register
2. Activate account (via email)
3. Login
4. Load videos
5. Play video

---

## 📁 Project Structure

```
videoflix/
├── authentication/
├── videos/
├── core/
├── media/
├── static/
├── docker-compose.yml
└── manage.py
```

---

## 📌 Notes

* HLS endpoints are public (no authentication required for streaming)
* API endpoints are protected (JWT cookie authentication)
* Redis + worker must be running for video processing

---

## ✅ Status

* Authentication ✅
* Video Upload ✅
* HLS Streaming ✅
* Frontend Integration ✅

---

## 👨‍💻 Author

Muhammed Yunus Amini

