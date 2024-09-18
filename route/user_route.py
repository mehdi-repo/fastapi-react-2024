from fastapi import Depends,APIRouter,HTTPException,status
from sqlalchemy.orm import Session
from database.connection import get_db
from fastapi.security import   OAuth2PasswordRequestForm
from model.user_model import User
from repository import user_crud
from schema import user_schema
from security.user_security import  authenticate_user, create_access_token, get_current_user, verify_token


user_Router = APIRouter(prefix="/user")


@user_Router.post("/create", response_model=user_schema.RegisterResponse,tags=["users"])
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user_crud.create_user(db=db, user=user)
    return {"message": "User created successfully"}
    

# Login route
@user_Router.post("/login",tags=["users"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(User=user)
    return {"access_token": access_token, "token_type": "bearer"}




@user_Router.put("/users/{user_id}/role", response_model=user_schema.User,tags=["role"])
def update_role(user_id: int, new_role: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    if current_user.roles != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You do not have permission to perform this action."
        )

    if new_role not in ["admin", "user", "guest"]:  #
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")

    user = user_crud.update_user_role(db, user_id=user_id, new_role=new_role)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user




