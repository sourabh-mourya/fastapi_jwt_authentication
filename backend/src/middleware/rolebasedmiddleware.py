from fastapi import Depends,HTTPException,status

def roleBaseMiddleware(user:dict,allowed_role:list):
    role=user.get('role')
    if role not in allowed_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    #agar wo allowed role me hi to return user
     # kr dege
     
    return user