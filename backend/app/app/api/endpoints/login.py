from fastapi import APIRouter, Depends, Form,requests
from sqlalchemy.orm import Session
from api.deps import *
from utils import send_mail
from app.core.security import get_password_hash,verify_password
router = APIRouter()

#check Token is vaild or not
@router.post("/check_token")
async def checkToken(*,db: Session = Depends(get_db),
                      token: str = Form(...)):
    
    checkToken = db.query(ApiTokens).filter(ApiTokens.token == token,
                                           ApiTokens.status == 1).first()
    if checkToken:
        return {"status": 1,"msg": "Success."}
    else:
        return {"status": 0,"msg": "Failed."}
    
#login
@router.post("/login")
async def login(*,db : Session = Depends(get_db),
                authcode: str = Form(None),
                username: str = Form(...),
                password: str = Form(...),
                dealer_code : str = Form(None),
                device_id: str = Form(None),
                device_type: str = Form(...,description = "1-android,2-ios"),
                ip : str = Form(None),
                push_id: str = Form(None)):
    ip = ip
    if device_id:
        auth_text = device_id + str(username)
    else:
        auth_text = username
    deviceTypeData = [1,2,3]
    user = None
    if dealer_code:
        user = dealer_authenticate(db,username=username,
                                     password=password,
                                     authcode=authcode,
                                     auth_text=auth_text,
                                     dealer_code=dealer_code)
    if not dealer_code:
        user = authenticate(db,username = username,
                                password = password,
                                authcode = authcode,
                                auth_text = auth_text)
    if user==1:
        return {"status":0,"msg":"wrong userName or password"}
    userId = None
    userType = None
    if user and user!=1: 
        userId = user.id
        userType = user.user_type

    key = None
    if userId:
        # db.query(ApiTokens).filter(
        #     ApiTokens.device_type == device_type,
        #     ApiTokens.user_id == userId
        # ).update({ApiTokens.status: False})
        key = ''
        char1 = '0123456789abcdefghijklmnopqrstuvwxyz'
        char2 = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        characters = char1 + char2
        token_text = userId
        for i in range(0, 30):
            key += characters[random.randint(
                    0, len(characters) - 1)]
        
        addToken = ApiTokens(user_id = userId,
                            token = key,
                            created_at = datetime.now(settings.tz_IN),
                            renewed_at = datetime.now(settings.tz_IN),
                            validity = 1,
                            device_type = device_type,
                            device_id = device_id,
                            push_device_id = push_id,
                            device_ip = ip,
                            status = 1)

        db.add(addToken)
        db.commit()

        return {'status':1,
                'token': key,
                'msg': 'Successfully login.',        
                'userType': userType,
                'userId': userId,
                'userName': username               
                }
    else:
        return {"status":0,"msg":"Your account not found.Please check the details you entered."}

#2.Logout
@router.post("/logout")
async def logout(db: Session = Depends(get_db),
                 token: str = Form(...)):

    user = get_user_token(db = db,token = token)
    if user:
        check_token = db.query(ApiTokens).\
            filter(ApiTokens.token == token,ApiTokens.status == 1).update({"status":-1})

        db.commit()
        return ({"status": 1,"msg": "Success."}) 
    else:
        return ({"status":0,"msg":"Invalid user."})

#3.change Password
""" This Api is for that Exception Case thus the User
Wants to Change their Password after Login"""

@router.post("/changePassword")
async def changePassword(db: Session = Depends(get_db),
                          token: str = Form(...)
                          ,old_password: str = Form(None),
                          new_password: str = Form(...),
                          userId: int = Form(None)):

    user = get_user_token(db = db,token = token)
    if user:
        userTypeData =[1,2,3,4]
        if not userId:
            if  verify_password(old_password,user.password):
                user.password = get_password_hash(new_password)
                db.commit()
                return ({"status": 1,"msg": 
                            "Password successfully updated."})
            else:
                return ({"status": 0,"msg": "Current password is invalid."})
        else:
            if user.user_type in userTypeData:
                getUser = db.query(User).\
                    filter(User.id == userId,
                            User.status == 1).\
                    update({'password':get_password_hash(new_password)})
                
                db.commit()
                return {"status":1,"msg":"Password successfully updated."}
            else:
                return {"status":"You are not authenticated to change the password for other users."}
        
    else:  
        return ({"status": -1,"msg": "Sorry your login session expires.Please login again."})

#3.1 ResetPassword
""" This Api is for that Exception Case thus the User
Wants to Change their Password before Login"""

@router.post("/reset_password")
async def resetPassword(db:Session=Depends(get_db),
                         resetKey:str = Form(...),
                         newPassword:str = Form(...)):
    getUser = db.query(User).filter(User.reset_key == resetKey,
                                    User.status == 1).first()
    if getUser:
        if getUser.is_active == 0:
            return {"status":0,"msg":"Unable to change password. Your account is inactive."}
        
        else:
            getUser.password = get_password_hash(newPassword)
            getUser.reset_key = None
            db.commit()
            return {"status":1,"msg":"Password changed successfully."}
    else:
        return {"status":-1,"msg":"You cannot change the password at this moment.Please try later."}


@router.post('/forgotPassword')
async def forgotPassword(db: Session = Depends(get_db),    
                                    email: str = Form(None),
                                    dealer_code = Form(None)):
    userTypeData = [1,2,3,4,5]
    user = db.query(User).filter(User.user_type.in_(userTypeData),
                                 User.email == email,
                                  User.status == 1)
    if dealer_code:
        user = user.filter(User.dealer_code == dealer_code)
    checkUser = user.first()
    if checkUser:
        if checkUser.is_active ==0:
            return {"status":0,
                    "msg":
                    "Access denied. Your account is inactive. Contact admin for further assistance."}
        
        else:

            (otp, reset, created_at,
            expire_time, expire_at,
                otp_valid_upto) = get_otp()
        
            otp="123456"
            message = f'''Your OTP for Reset Password is : {otp}'''
            reset_key = f'{reset}{checkUser.id}DTEKRNSSHPT'
    
            user = user.update({'otp': otp,
                                'reset_key': reset_key,
                                'otp_expire_at': expire_at})
            db.commit()

            try:
                send = await send_mail(receiver_email = checkUser.email,
                                       message = message)
                return ({'status': 1,'reset_key': reset_key,
                        'msg': 
                        f'An OTP message has been sent to {email}.',
                        'remaining_seconds': otp_valid_upto})
            
            except Exception as e:
                print("EXCEPTION: ",e)
                return {'status': 0,'msg': 'Unable to send the Email.'}
    else:
        return({'status':0,'msg':'Sorry. The requested account not found'})

@router.post("/verify_otp")
async def verifyOtp(db:Session = Depends(get_db),
                    resetKey:str= Form(...),otp:str=Form(...)):
    
    getUser = db.query(User).filter(User.reset_key == resetKey,
                                    User.status == 1,User.is_active==1).first()
    
    if getUser:
        if getUser.otp == str(otp):
            if getUser.otp_expire_at >= datetime.now(settings.tz_IN).replace(tzinfo=None):
                getUser.otp = None
                getUser.otp_expire_at = None
        
                (otp, reset, created_at,
                    expire_time, expire_at,
                        otp_valid_upto) = get_otp()
                
                reset_key = f'{reset}{getUser.id}DTEKRNSSHPT'
                getUser.reset_key = reset_key
                
                db.commit()
                return {"status":1,"msg":"Verified.","reset_key":reset_key}
            
            else:
                return ({"status": 0,"msg": "time out."})
        else:
            return ({"status": 0,"msg": "otp not match."})
    else:
        return {"status":0,"msg":"No record found."}

@router.post("/resend_otp")
async def resendOtp(db:Session = Depends(get_db),
                    resetKey:str= Form(...)):
    getUser = db.query(User).filter(User.reset_key == resetKey,
                                    User.status == 1,User.is_active==1).first()
    if getUser:
        (otp, reset, created_at,
            expire_time, expire_at,
                otp_valid_upto) = get_otp()
        otp="123456"
        message = f'''Your OTP for Reset Password is : {otp}'''
        reset_key = f'{reset}{getUser.id}DTEKRNSSHPT'

        getUser.otp = otp
        getUser.reset_key = reset_key
        getUser.otp_expire_at = expire_at
                          
        db.commit()

        try:
            send = await send_mail(receiver_email = getUser.email,
                                    message = message)
            return ({'status': 1,'reset_key': reset_key,
                    'msg': 
                    f'An OTP message has been sent to {getUser.email}.',
                    'remaining_seconds': otp_valid_upto})
        
        except Exception as e:
            print("EXCEPTION: ",e)
            return {'status': 0,'msg': 'Unable to send the Email.'}
    else:
        return {'status':0,"msg":"No user found."}




#get auth code
import hashlib
@router.post("/getAuth")
async def getAuth(name:str=Form(...)):
    
    salt = settings.SALT_KEY
    name = salt+name
    
    result = hashlib.sha1(name.encode())
    
    print(result.hexdigest())
    return {"authcode" : result.hexdigest()}