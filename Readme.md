# 🔐 FastAPI Authentication System

A **authentication system backend** built with FastAPI, featuring JWT authentication, refresh tokens, role-based access control, and Google OAuth login.

---

## 🚀 Features

* ✅ User Signup & Login
* 🔐 JWT Authentication (Access + Refresh Tokens)
* 🔄 Token Refresh System
* 🚪 Logout (Token Blacklisting)
* 👑 Role-Based Access (Admin/User)
* 🌐 Google OAuth Login
* 🔒 Password Hashing with Bcrypt
* 📄 Swagger UI Documentation

---

## 🛠️ Tech Stack

* **Backend:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Auth:** JWT (python-jose)
* **OAuth:** Authlib (Google Login)
* **Security:** Passlib (bcrypt)
* **Server:** Uvicorn

---

## 📂 Project Structure

```
Auth-System/
│── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth/
│   │   ├── routes.py
│   │   ├── utils.py
│   │   ├── dependencies.py
│   │   ├── google.py
│   │   ├── blacklist.py
│── .env
│──.gitignore
│── requirements.txt
│── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/auth-system.git
cd auth-system
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://username:password@localhost/auth_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256

GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

---

## ▶️ Run the Server

```bash
uvicorn app.main:app --reload
```

---

## 📌 API Documentation

Open in browser:

👉 http://127.0.0.1:8000/docs

---

## 🔐 Authentication Flow

1. User Signup → `/auth/signup`
2. Login → `/auth/login`
3. Receive:

   * Access Token
   * Refresh Token
4. Use token in protected routes:

   ```
   Authorization: Bearer <your_token>
   ```

---

## 🌐 Google OAuth Setup

1. Go to Google Cloud Console
2. Create OAuth Client ID
3. Add redirect URI:

```
http://127.0.0.1:8000/auth/google/callback
```

4. Add credentials in `.env`

---

## 📡 API Endpoints

| Method | Endpoint           | Description      |
| ------ | ------------------ | ---------------- |
| POST   | /auth/signup       | Register user    |
| POST   | /auth/login        | Login user       |
| POST   | /auth/refresh      | Refresh token    |
| POST   | /auth/logout       | Logout           |
| GET    | /auth/me           | Get current user |
| GET    | /auth/admin        | Admin access     |
| GET    | /auth/google/login | Google login     |

---

## 🔒 Security Features

* Password hashing (bcrypt)
* JWT token validation
* Token expiration handling
* Blacklist-based logout
* OAuth secure login

---

## 🚀 Future Improvements

* Email verification system
* Password reset via email
* Rate limiting
* Docker deployment
* CI/CD pipeline

---

## 👨‍💻 Author

**Prince Kushwaha**
