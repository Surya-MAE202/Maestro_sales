
from typing import Generator, Any, Optional
from fastapi.security import OAuth2PasswordBearer
import datetime
from sqlalchemy.orm import Session
from app import models,schemas
import random
# import jwt
from sqlalchemy import or_
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal
from datetime import datetime,timedelta
import hashlib
from app.models import ApiTokens,User
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_user_token(db: Session, *, token: str) :
    get_token=db.query(ApiTokens).filter(ApiTokens.token== token ,
                                            ApiTokens.status==1).first()

    if get_token: 
        return db.query(User).filter(User.id == get_token.user_id,
                                         User.status == 1,User.is_active == 1).first()            
    else:
        return None

def authenticate(db: Session, *, username: str, password: str ,
                  authcode:str ,
                    auth_text:str) -> Optional[models.User]:
    
        user = get_by_user(db, username=username) 
        if not user or user.password == None:
            return None

        if not security.check_authcode(authcode, auth_text):   
            return None

        if not security.verify_password(password, user.password):
            return 1
        return user

def dealer_authenticate(db: Session, *, username: str, password: str ,
                  authcode:str ,
                    auth_text:str,
                    dealer_code : str):
    
        user = get_by_user_employee(db, username=username,dealer_code=dealer_code) 
        print(user)
        if not user or user.password == None:
            return None

        if not security.check_authcode(authcode, auth_text):   
            return None

        if not security.verify_password(password, user.password):
            return 1
        return user

def get_by_user_employee(db: Session, *, username: str,dealer_code :str):
        
        userTypeData = [3,4,5]
        getUser=db.query(User).\
            filter( or_(User.username == username,
                        User.phone == username,
                        User.email == username,
                        User.alternative_number == username),
                    User.dealer_code == dealer_code, User.user_type.in_(userTypeData),User.status == 1).first()
        return getUser

def get_by_user(db: Session, *, username: str):
        
        userTypeData = [1,2]
        getUser=db.query(User).\
            filter( or_(User.username == username,
                       
                        User.phone == username,
                        User.email == username,
                        User.alternative_number == username) 
                   , User.user_type.in_(userTypeData),User.status == 1).first()
        return getUser

def get_otp():
    otp = ''
    reset = ""
    characters = '0123456789'
    char1 = 'qwertyuioplkjhgfdsazxcvbnm0123456789'
    char2 = 'QWERTYUIOPLKJHGFDSAZXCVBNM'
    reset_character = char1 + char2
    
    otp = random.randint(111111, 999999)
   
    for j in range(0, 20):
        reset += reset_character[random.randint(
            0, len(reset_character) - 1)]

    created_at = datetime.now(settings.tz_IN)
    expire_time = created_at +timedelta(minutes=2)
    expire_at = expire_time.strftime("%Y-%m-%d %H:%M:%S")
    otp_valid_upto = expire_time.strftime("%d-%m-%Y %I:%M %p")

    return [otp, reset , created_at, expire_time, expire_at, otp_valid_upto]

import re

def contains_emoji(text):
    # Define a regular expression to match emojis
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F700-\U0001F77F"  # alchemical symbols
                           u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                           u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                           u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                           u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                           u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                           u"\U00002702-\U000027B0"  # Dingbats
                           "]+", flags=re.UNICODE)

    # Check if the text contains emojis
    return bool(emoji_pattern.search(text))