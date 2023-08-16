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





 
def get_account_by_email(db: Session, email: str, request: Request): #will return none if database has no matches
    # Authenticate token before querying DB
    access_token = request.headers.get('access-token')
    utils.authenticate_token(access_token)

    account = db.query(models.Account).filter(models.Account.email == email).first()
    return account