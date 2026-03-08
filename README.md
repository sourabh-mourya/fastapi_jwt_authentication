# 🔐 FastAPI JWT Authentication

> A complete JWT-based authentication system built with FastAPI — featuring Role-Based Access Control (RBAC) and protected routes.

---

## ⚠️ Important — Read Before Using

Before working with this project, **read through the authentication file at least once.**

---

## 📂 Project Structure — Kahan Kya Milega?

```
project/
├── backend/                     # 📖 Padhne & Seekhne ke liye
│   └── auth.py                  # JWT, Middleware, RBAC — sab ek jagah
│
└── practice_authentication/     # 🚀 Production Level ke liye
    ├── auth/
    │   ├── jwt_handler.py
    │   ├── dependencies.py
    │   └── role_checker.py
    └── routes/
        ├── auth_routes.py
        ├── user_routes.py
        └── admin_routes.py
```

> 💡 **Tip:** Pehle `backend/` folder padho — poora flow samjh aayega.
> Jab confident ho jao tab `practice_authentication/` use karo real projects ke liye.

---

## 📖 `backend/` — Seekhne ke Liye

Is folder mein **saari authentication logic ek hi file mein** likhi hai.

Jab bhi koi cheez samajhni ho — **JWT kaise banta hai, verify hota hai, role check hota hai** — sab `backend/` folder mein milega.

### Is file mein kya hai:

| Component | Description |
|---|---|
| 🔑 JWT Token Creation | Token kaise generate hota hai |
| ✅ JWT Verification | Token kaise verify hota hai |
| 🛡️ Auth Middleware / Dependency | FastAPI dependency se route protect karna |
| 👥 Role-Based Access Control | Role ke hisab se access restrict karna |
| 🔒 Protected Routes | Sirf valid token par accessible endpoints |
| 🗄️ MongoDB User Validation | User credentials DB se verify karna |

### Kyun sab ek file mein hai?

- ✔️ Poora authentication flow ek jagah dikhe
- ✔️ Debugging aur testing aasaan ho
- ✔️ Seekhne aur samjhane ke liye best structure
- ✔️ Request ka full lifecycle ek hi jagah trace ho sake

---

## 🚀 `practice_authentication/` — Production ke Liye

Jab **real project ya production-level code** chahiye, to `practice_authentication/` folder use karo.

Yahan har cheez **alag-alag files mein properly separated** hai:

```
PracticeAuthentication/
├── env/                         # Virtual environment
│
└── src/
    ├── config/
    │   └── db.py                # Database connection
    │ 
    ├── dependencies/            # 🛡️ Auth Logic
    │   ├── checkToken.py        # JWT verification & middleware
    │   └── roleChecker.py       # Role-based access control
    │
    ├── models/
    │   └── authModel.py         # User model / schema
    │
    ├── routes/
    │   ├── authRoute.py         # Login / Register endpoints
    │   └── protectRoute.py      # Protected routes
    │
    ├── main.py                  # App entry point
    └── .env                     # Environment variables
---

## ✅ Sahi Tarika — Kaise Shuru Karo?

**Step 1 →** `backend/` folder kholo aur auth file ek baar poori padho

**Step 2 →** Samjho ki:
- Token kaise **generate** hota hai
- Token kaise **verify** hota hai
- **User data** kaise extract hota hai
- **Role** kaise check hoti hai

**Step 3 →** Ab `practice_authentication/` mein jaake production-ready code use ya modify karo

---

## 🔐 Authentication Features

- 🔐 JWT-based authentication
- 👮 Role-based authorization
- 🔒 Protected routes
- ⚙️ FastAPI dependency-based middleware
- 🗄️ MongoDB user validation *(if applicable)*
