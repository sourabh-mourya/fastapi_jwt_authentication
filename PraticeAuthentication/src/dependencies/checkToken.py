from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
import jwt
import os


load_dotenv()
JWT_AUTH = os.getenv("JWT_AUTH")

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials


    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing"
        )

    try:
        # 2. Decode the token
        payload = jwt.decode(token, JWT_AUTH, algorithms=["HS256"])

        # 3. Check if payload is empty
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
            )

        return payload

    # --- Yahan naye error checks add karein ---

    except jwt.ExpiredSignatureError:
        # Agar token ki date nikal gayi ho
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please login again.",
        )
    except jwt.InvalidTokenError:
        # Agar token tamper kiya gaya ho ya galat ho
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    except Exception as e:
        # Kisi bhi aur technical error ke liye
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


'''
agar apne token cookies ke ander hi to apne iss trh check krenge

from fastapi import Request, HTTPException, status

async def get_current_user(request: Request): # Request object use karein
    # Cookie se token nikalna
    token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Not authenticated"
        )
    
    try:
        payload = jwt.decode(token, JWT_AUTH, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
'''