from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.schema import UserCreate, UserLogin, UserOut, Token
from app.core.database import get_db
from app.services import auth_services
#PostCreate, PostOut, FollowOut

authRouter = APIRouter(prefix="/auth", tags=["auth"])

@authRouter.post("/signup", response_model = UserOut, status_code= 201)
def signUp(signUpDetails : UserCreate, db: Session = Depends(get_db)):
    return auth_services.signup(db, signUpDetails)


@authRouter.post("/login", response_model = Token)
def login(loginDetails : UserLogin, db: Session = Depends(get_db)):
    return auth_services.login(db, loginDetails)


#router -> service -> repo -> db

