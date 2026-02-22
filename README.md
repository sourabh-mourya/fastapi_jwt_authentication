# 🔐 FastAPI JWT Authentication

> A complete JWT-based authentication system built with FastAPI — featuring Role-Based Access Control (RBAC) and protected routes, all in one file for fast learning and development.

---

## ⚠️ Important — Read Before Using

Before working with this project, **read through the authentication file at least once.**

All authentication logic lives in a **single file** so you can trace the full request lifecycle without jumping between modules.

---

## 📦 What's Inside (Single File)

| Component | Description |
|---|---|
| 🔑 JWT Token Creation | Generates signed tokens on login |
| ✅ JWT Verification | Validates and decodes incoming tokens |
| 🛡️ Auth Middleware / Dependency | FastAPI dependency injection for route protection |
| 👥 Role-Based Access Control | Restricts endpoints by user role |
| 🔒 Protected Routes | Endpoints that require a valid token |
| 🗄️ MongoDB User Validation | Verifies user credentials against DB *(if applicable)* |

---

## 🤔 Why Everything Is in One File?

This structure was **intentionally chosen** for:

- ✔️ Easier understanding of the complete authentication flow
- ✔️ Quick debugging and testing
- ✔️ Learning and demonstration purposes
- ✔️ Seeing the full request lifecycle in one place

---

## 📖 Recommendation for Users

If you plan to **use or extend** this project, follow these steps:

1. **Read** the authentication file once
2. **Understand** how each part works:
   - How the token is **generated**
   - How the token is **verified**
   - How **user data** is extracted
   - How the **role** is checked
3. **Then** start using or modifying the routes

> This will help you understand the project structure quickly and confidently.

---

## 🚀 Authentication Features

- 🔐 JWT-based authentication
- 👮 Role-based authorization
- 🔒 Protected routes
- ⚙️ FastAPI dependency-based middleware
- 🗄️ MongoDB user validation *(if applicable)*

---

## 🏗️ Recommended Structure for Production

The current structure is optimized for **learning and demonstration.**
For a production environment, the following separation is recommended:

```
auth/
├── jwt_handler.py       # Token creation & verification
├── dependencies.py      # FastAPI auth dependencies
└── role_checker.py      # Role-based access logic

routes/
├── auth_routes.py       # Login / register endpoints
├── user_routes.py       # User-level protected routes
└── admin_routes.py      # Admin-level protected routes
```

> ⚠️ The current single-file structure is **not** intended for strict production use.

---

## 📝 License

This project is intended for **educational and demonstration purposes.**
Feel free to extend it for your own use case.
