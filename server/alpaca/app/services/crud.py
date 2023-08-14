import os
from dotenv import load_dotenv
load_dotenv()

import boto3
from fastapi import HTTPException
from ..schemas import schemas 
from ..utils import utils


username = "danieltest123@gmail.com"
password = "password123"

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
        UserPoolId=os.environ.get('USER_POOL_ID'),
        Username=username,
    )

    # Now authenticate the user and return the tokens
    auth_response = client.initiate_auth(
        ClientId=os.environ.get('COGNITO_USER_CLIENT_ID'),
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