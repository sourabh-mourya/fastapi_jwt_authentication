from fastapi import APIRouter, Depends  # Depends import karna mat bhoolna
from src.dependencies.checkToken import get_current_user
from src.dependencies.roleChecker import RoleChecker
protectRoute = APIRouter(prefix="/api/v1")


# Jiske pass token rahega wahi isko access kar sakta hai
@protectRoute.get("/token_route_login")
async def tokenLogin(data: dict = Depends(get_current_user)):
    # data: dict (kyunki jwt.decode dictionary return karta hai)
    # Depends(get_current_user) -> parentheses () zaroori hain

    return {
        "id": data.get("userId"),
        "role": data.get("role"),
        "email": data.get("email"),
    }


# ab iss route ko only admin access kr skega



# Admin only route
@protectRoute.get("/admin")
async def admin_only(user: dict = Depends(RoleChecker(["admin"]))):
    return {"message": "Hello Admin!", "data": user}

# Admin aur Manager dono ke liye
@protectRoute.get("/management")
async def management_route(user: dict = Depends(RoleChecker(["admin", "manager"]))):
    return {"message": "Hello Staff!", "data": user}