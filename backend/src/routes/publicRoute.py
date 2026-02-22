from fastapi import APIRouter

route = APIRouter(prefix='/api/v1/health')

@route.get("/")
def indexView():
    return {
        "message": "Server is running on 8000 Port"
    }