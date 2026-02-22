from fastapi import FastAPI
from src.routes.publicRoute import route as publicRoute
from src.routes.AuthRoute import router as AuthRoute

# cors error solutin
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# middleware
origins = ["http://localhost", "*"]  # anyone can access
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ✅ correct
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# add route
app.include_router(publicRoute)
app.include_router(AuthRoute)