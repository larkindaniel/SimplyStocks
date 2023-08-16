import os
from dotenv import load_dotenv
load_dotenv()

import boto3
from datetime import datetime
from faker import Faker
from sqlalchemy.orm import Session
from fastapi import HTTPException, Request
from uuid import UUID

from alpaca.broker.client import BrokerClient
from alpaca.broker.models import (
                        Contact,
                        Identity,
                        Disclosures,
                        Agreement
                    )
from alpaca.broker.requests import CreateAccountRequest
from alpaca.broker.enums import TaxIdType, FundingSource, AgreementType

from ..schemas import schemas
from ..models import models
from ..utils import utils


def cognito_signup(username: str, password: str):
    client = boto3.client('cognito-idp', region_name=os.environ.get('COGNITO_REGION_NAME'))
    try:
        response = client.sign_up(
            ClientId=os.environ.get('COGNITO_USER_CLIENT_ID'),
            Username=username,
            Password=password
        )
        print(response)
    except Exception as e: # Generally, will trigger upon non-unique email
        raise HTTPException(status_code=400, detail=f"{e}")

    user_sub = response['UserSub']
    
    # This will confirm user registration as an admin without a confirmation code
    client.admin_confirm_sign_up(
        UserPoolId= os.environ.get("USER_POOL_ID"),
        Username=username,
    )

    # Now authenticate the user and return the tokens
    auth_response = client.initiate_auth(
        ClientId= os.environ.get("COGNITO_USER_CLIENT_ID"),
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': password
        }
    )
    access_token = auth_response['AuthenticationResult']['AccessToken']
    refresh_token = auth_response['AuthenticationResult']['RefreshToken']

    signup_result = utils.CognitoResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        cognito_user_id=user_sub
    )
    return signup_result

def cognito_login(username: str, password: str):
    client = boto3.client('cognito-idp', region_name=os.environ.get('COGNITO_REGION_NAME'))
    # Authenticate the user and return the tokens
    try:
        auth_response = client.initiate_auth(
            ClientId=os.environ.get('COGNITO_USER_CLIENT_ID'),
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )
    except Exception as e: # Generally, will trigger upon wrong email/password
        raise HTTPException(status_code=400, detail=f"{e}")
    
    access_token = auth_response['AuthenticationResult']['AccessToken']
    refresh_token = auth_response['AuthenticationResult']['RefreshToken']
    login_result = utils.CognitoResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )

    return login_result


 
def get_account_by_email(db: Session, email: str, request: Request): #will return none if database has no matches
    # Authenticate token before querying DB
    access_token = request.headers.get('access-token')
    utils.authenticate_token(access_token)

    account = db.query(models.Account).filter(models.Account.email == email).first()
    return account