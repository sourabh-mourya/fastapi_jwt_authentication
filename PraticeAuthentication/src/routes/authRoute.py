from tabnanny import check
from tkinter import NO
import token

from fastapi import APIRouter, HTTPException, status
import jwt
from src.models.authModel import LoginUser, RegisterUser
from src.config.db import db
from dotenv import load_dotenv
import bcrypt
import os


load_dotenv()

JWT_AUTH=os.getenv('JWT_AUTH')
authRoute = APIRouter(prefix='/api/v1/auth')
authCollection = db['user']

@authRoute.post('/register')
async def registerUser(data: RegisterUser):
    # Pydantic model ko dict mein convert karein
    user_data = data.dict()
    
    # 1. Check if user exists
    existingUser = await authCollection.find_one({'email': user_data['email']})
    if existingUser:
        # 403 Forbidden ki jagah 400 Bad Request zyada sahi hai duplicate user ke liye
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User already exists with this email"
        )
    
    # 2. Password Hashing (FIXED SYNTAX)
    salt = bcrypt.gensalt(10) # gensalt use karein
    hashPassword = bcrypt.hashpw(
        user_data["password"].encode("utf-8"),
        salt
    )
    
    # Password decode karke string banayein
    user_data['password'] = hashPassword.decode('utf-8')
    
    # 3. Insert in MongoDB
    result = await authCollection.insert_one(user_data)
    
    # 4. Fetch the document for testing (FIXED ID HANDLING)
    document = await authCollection.find_one(
        {"_id": result.inserted_id},
        {"password": 0} # Password ko hide karne ka behtar tarika
    )
    
    # MongoDB ki _id (ObjectId) ko string mein badalna zaroori hai
    document["_id"] = str(document["_id"])
    
    return {
        "message": "Register successful",
        "user": document,
    }
    
   
@authRoute.post('/login')
async def loginUser(data: LoginUser):
    # Pydantic model to dict
    login_data = data.dict()
    
    # 1. Check email in database
    user_dict = await authCollection.find_one({'email': login_data['email']})
    
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist with this email"
        )
    
    # 2. Check the password (FIXED ORDER AND LOGIC)
    # login_data['password'] = User ne jo dala (Plain)
    # user_dict['password'] = DB mein jo hai (Hash)
    is_password_correct = bcrypt.checkpw(
        login_data['password'].encode("utf-8"), # Plain text first
        user_dict['password'].encode("utf-8")  # Hashed hash second
    )
    
    if not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # 3. ID conversion and Cleanup
    user_dict['_id'] = str(user_dict['_id'])
    del user_dict['password'] # Security: Password delete kar dein response se pehle
    
    # 4. Token creation (FIXED PARAMETER 'algorithm')
    token_payload = {
        'userId': user_dict['_id'],
        'role': user_dict.get('role', 'user'), # Safe access
        'email': user_dict['email'],
    }
    
    token = jwt.encode(
        token_payload, 
        JWT_AUTH, 
        algorithm="HS256" # 'algorithm' not 'algorithms'
    )
    
    # agar cookies ke ander set krna hi to 
    # response.set_cookie(
    #     key="access_token", 
    #     value=token, 
    #     httponly=True,   # JS isse read nahi kar payega (Extra Security)
    #     max_age=3600,    # Token kitni der tak rahega (seconds mein)
    #     samesite="lax",  # CSRF protection ke liye
    #     secure=False     # Agar local pe ho toh False, production (HTTPS) pe True
    # )
    return {
        'message': "Login successfully",
        'data': user_dict,
        'token': token
    }