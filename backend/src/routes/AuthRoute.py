from fastapi import APIRouter,HTTPException,status,Depends
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from src.models.User import User as UserModal
from src.models.User import LoginModel as LoginModel
from src.config.db import db as MonogoDB
from src.middleware.rolebasedmiddleware  import roleBaseMiddleware 
import bcrypt
import jwt
import os
from dotenv import load_dotenv




load_dotenv()
JWT_AUTH=os.getenv('JWT_AUTH')


router = APIRouter(prefix="/api/v1/auth")

# -------------------- Mongo Collection --------------------
# MonogoDB = database object
# 'user' = collection name in MongoDB
# authCollection ek reference hai MongoDB ke user collection ka
# Jo bhi operation authCollection par karenge, wo MongoDB ke user collection me hoga
authCollection = MonogoDB["user"]


# -------------------- Register API --------------------
@router.post("/register")
async def registerUser(data: UserModal):



    # FastAPI request body Pydantic model hota hai
    # MongoDB me insert karne ke liye hume dictionary chahiye
    user_dict = data.dict()


    ##Check existing user in database 
    existingUser=await authCollection.find_one({"email":user_dict['email'].lower() })
    #agar user mil gya to apne error raise krenge 
    if existingUser:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,"User already exits with these email")
    
    
    # -------------------- Password Hashing --------------------
    # Password ko plain text me store nahi karte (security risk)
    # bcrypt se password hash karte hain

    # gensalt(12) -> 12 is cost factor (security level)
    salt = bcrypt.gensalt(12)

    # password string ko bytes me convert karke hash karte hain
    hashed_password = bcrypt.hashpw(
        user_dict["password"].encode("utf-8"),
        salt
    )

    # MongoDB me string store karne ke liye decode kar dete hain
    user_dict["password"] = hashed_password.decode("utf-8")

    # -------------------- Insert User --------------------
    # insert_one ek document insert karta hai aur inserted_id return karta hai
    result = await authCollection.insert_one(user_dict)

    # -------------------- Fetch Inserted User (Testing / Response purpose) --------------------
    # Projection me sirf selected fields return kar rahe hain
    document = await authCollection.find_one(
        {"_id": result.inserted_id},
        {
            "_id": 1,
            "name": 1,
            "email": 1,
            "address": 1
        }
    )

    # MongoDB ObjectId JSON me directly send nahi hota
    # Isliye string me convert kar dete hain
    document["_id"] = str(document["_id"])

    #ab data database me store ho jane ke baad hm token ko generate krenge 
   # token=jwt.encode({"userId":document['_id']},JWT_AUTH, algorithm="HS256") token hmsea login ke time generate hota but apne ne pratice ke liye yaha pr token ko generate kiya hi 
   
    

    # -------------------- Response --------------------
    return {
        "message": "Register successful",
        "user": document,
        # 'token':token
    }
    
    
@router.post("/login")
async def loginUser(data:LoginModel ):
    # Convert incoming data to dict
    user_dict = data.dict() # If using Pydantic model: user_dict = data.dict()
    print("Incoming login data:", user_dict)

    # Step 1: Find user by email (normalize lowercase)
    checkUser = await authCollection.find_one({"email": user_dict['email'].lower()})

    if not checkUser:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist with this email"
        )

    # Step 2: Compare password
    password_match = bcrypt.checkpw(
        user_dict['password'].encode(),
        checkUser['password'].encode()
    )

    if not password_match:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Step 3: Remove password before sending response
    checkUser['_id'] = str(checkUser['_id'])
    token=jwt.encode({"userId":checkUser['_id'],"role":checkUser['role']},JWT_AUTH, algorithm="HS256")

    del checkUser['password']

    return {
        "message": "Login successful",
        "user": checkUser,
        'token':token

    }
    

#token access code means token ko fucntion me kaise kya used krnege


# -------------------- Security Scheme --------------------
# This creates an HTTP Bearer security scheme to automatically check
# the Authorization header in requests
security = HTTPBearer()#security ke ander token jo ki header se aagyega 

# -------------------- Dependency Function --------------------
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    This function is a dependency that extracts the token from the Authorization header.

    Parameters:
    - credentials: Automatically provided by Depends(security)
      -> This is an HTTPAuthorizationCredentials object which has:
         - credentials.scheme (should be 'Bearer')
         - credentials.credentials (the actual token string)

    Returns:
    - The token string itself (credentials.credentials)
    
    Why use Depends here?
    - To run this logic automatically before any route that needs authentication
    - Avoids repeating header parsing in every route
    """
    # Extract the token string from the Authorization header
    userData=jwt.decode(credentials.credentials,JWT_AUTH, algorithms=["HS256"])
    print("user data :-",userData)
    print("User role :- ",userData['role'])
    print("User id :- ",userData['userId'])
    return userData


# -------------------- Protected Route -------------------- its means wo login rhega and token ko header me dega whi access kr skta hi iss route ko 
@router.get("/profile")
def userProfile(
    data: str = Depends(get_current_user)  # Depends calls get_current_user and passes token to 'data'
):
    """
    Example route to get the profile info.
    
    Parameters:
    - data: This is the token string returned by get_current_user
    
    Returns:
    - The token string in this example (for testing)
    
    Note:
    - If Depends(get_current_user) was not used, you'd have to manually parse the header
      in every route which is repetitive and error-prone.
    """
    # Return the token received from get_current_user
    return {
        "id":data['userId'],
        'role':data['role']
    }
    
    
#ab apne role based authetication lga mtlb jiss role ko allow kra whi log iss route ko access kr ske ge uska pura code niche hi 
from fastapi import Depends, HTTPException, status

# Function to check whether user's role is allowed or not
def require_role(user: dict, allowed_role: list):
    
    # user is a dictionary coming from JWT payload
    # Example:
    # user = {
    #     "user_id": "123",
    #     "email": "test@gmail.com",
    #     "role": "admin"
    # }

    # user.get("role") safely fetches the role value from the dictionary
    # If "role" key is not present, it returns None instead of error
    # Example:
    # role = user.get("role")  → "admin"
    role = user.get("role")

    # Check if user's role is NOT present in allowed_role list
    # Example:
    # allowed_role = ["admin", "manager"]
    # If role = "user" → condition True → Access denied
    #apne examole se role ke ander kya aaa jyeg admin ur wo allowed role me bhi to user return kr dega
    #agar role abc hi to wo allowed role ke ander nhi it means not in allowed role return error dega
    
    if role not in allowed_role:
        raise HTTPException(
            Astatus_code=status.HTTP_403_FORBIDDEN,
            detail="ccess denied"
        )

    # If role is allowed, return user data
    return user


@router.get('/admin')
def adminRoute(
    # FastAPI dependency:
    # get_current_user() will:
    # 1. Read JWT from Authorization header
    # 2. Decode it
    # 3. Return payload as dictionary
    user: dict = Depends(get_current_user)
):
    
    # Here we check if user's role is allowed for this route
    # Only users whose role is 'admin' can access this route
    require_role(user, ['admin'])

    # If role check passes, this response will be returned
    return {"message": "Admin access granted"}



#same code bus calling different tarike se ho rhi apnd require role ko middleware se call kr requrie role equal roleBaseMiddleke 

@router.get('/admin2')
def adminRoute(
    # FastAPI dependency:
    # get_current_user() will:
    # 1. Read JWT from Authorization header
    # 2. Decode it
    # 3. Return payload as dictionary
    user: dict = Depends(get_current_user)
):
    
    # Here we check if user's role is allowed for this route
    # Only users whose role is 'admin' can access this route
    roleBaseMiddleware(user,['admin'])
    # If role check passes, this response will be returned
    return {"message": "Admin access granted"}
