# 🎬 Videoflix Backend

## 📌 Projektbeschreibung

Videoflix ist ein Video-Streaming Backend mit Django REST Framework.  
Videos werden hochgeladen, automatisch in HLS konvertiert und im Frontend abgespielt.

---

## ⚙️ Features

- 🔐 User Authentication (Register, Login, Logout, Activation)
- 🎬 Video Upload
- ⚡ Background Processing mit Redis + RQ
- 🎥 Automatische HLS Konvertierung (480p, 720p, 1080p)
- 📡 Streaming über `.m3u8`
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

### 1. Projekt klonen

```bash
git clone <repo-url>
cd videoflix
````

### 2. Docker starten

```bash
docker compose up --build
```

---

## 🔗 API Endpoints

### 🔐 Authentication

| Endpoint                       | Method | Beschreibung       |
| ------------------------------ | ------ | ------------------ |
| `/api/register/`               | POST   | User registrieren  |
| `/api/login/`                  | POST   | Login + Tokens     |
| `/api/logout/`                 | POST   | Logout             |
| `/api/token/refresh/`          | POST   | Token erneuern     |
| `/api/activate/<uid>/<token>/` | GET    | Account aktivieren |

---

### 🎬 Videos

| Endpoint      | Method | Beschreibung       |
| ------------- | ------ | ------------------ |
| `/api/video/` | GET    | Liste aller Videos |
| `/api/video/` | POST   | Video hochladen    |

---

### 📺 Streaming (HLS)

| Endpoint                                    | Beschreibung |
| ------------------------------------------- | ------------ |
| `/api/video/<id>/<resolution>/index.m3u8`   | Playlist     |
| `/api/video/<id>/<resolution>/<segment>.ts` | Segmente     |

---

## 🔄 Video Processing

Nach Upload wird automatisch:

1. Video gespeichert
2. Hintergrund-Job gestartet (RQ Worker)
3. FFmpeg konvertiert in:

   * 480p
   * 720p
   * 1080p
4. HLS Dateien erzeugt (`.m3u8` + `.ts`)

---

## 🧪 Testen

### Frontend starten

Frontend der Akademie lokal öffnen (z. B. mit Live Server):

```text
http://127.0.0.1:5500
```

### Test Flow

1. Register
2. Activate Account
3. Login
4. Videos laden
5. Video abspielen

---

## 📁 Projektstruktur

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

## 📌 Hinweise

* HLS Endpoints sind öffentlich (kein Auth), damit Streaming funktioniert
* API Endpoints sind geschützt (JWT Cookie Auth)
* Redis + Worker müssen laufen für Video Processing

---

## ✅ Status

* Authentication ✅
* Video Upload ✅
* HLS Streaming ✅
* Frontend Verbindung ✅

---

## 👨‍💻 Autor

Muhammed Yunus Amini

