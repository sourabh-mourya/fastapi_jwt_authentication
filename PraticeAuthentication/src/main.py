from fastapi import FastAPI

from src.routes.protectRoute import protectRoute
from src.routes.authRoute import authRoute

app=FastAPI()




app.include_router(authRoute)
app.include_router(protectRoute)