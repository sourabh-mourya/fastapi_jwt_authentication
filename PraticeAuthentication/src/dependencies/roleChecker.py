from fastapi import HTTPException, status, Depends

from src.dependencies.checkToken import get_current_user

class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, user: dict = Depends(get_current_user)):
        # Check if user role exists and is allowed
        if user.get("role") not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, # Auth issues ke liye 403 best hai
                detail=f"Access denied. Required roles: {self.allowed_roles}"
            )
        return user