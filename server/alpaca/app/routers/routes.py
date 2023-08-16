from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from ..schemas import schemas
from ..services import crud
from ..config import SQLALCHEMY_DATABASE_URL


database.create_tables()

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Server is running"}

# User signs up for the platform
@router.post("/signup")
async def create_user(user: schemas.User):
    username = user.email
    password = user.password
    signup_result = crud.cognito_signup(username, password)
    return signup_result



# User logs into the platform
@router.post("/login")
async def login_user(user: schemas.User):
    username = user.email
    password = user.password
    login_result = crud.cognito_login(username, password)
    return login_result


# Sign up for brokerage account
@router.post("/accounts/signup")
async def create_brokerage_account(account: schemas.AccountCreate, request: Request, db: Session = Depends(database.get_db)):
    account = crud.create_account(db=db, account=account, request=request)
    return account