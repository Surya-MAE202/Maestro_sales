from fastapi import APIRouter, Depends, Form,requests
from sqlalchemy.orm import Session
from app.models import ApiTokens,User
from app.api.deps import *
from app.core.config import settings
from datetime import datetime
from app.utils import *
from sqlalchemy import or_,func
from app.core.security import *

router = APIRouter()

@router.post("/create_user")
async def createUser(db:Session = Depends(get_db),
                     token:str = Form(...),
                     name:str = Form(...),
                     userName:str=Form(...),phoneNumber:str=Form(...),
                     email:str=Form(None),
                     landline_number:str=Form(None),
                     state:str=Form(None),city:str=Form(None),country:str=Form(None),password:str=Form(None),
                     userType:int=Form(None,description="2->Admin,3->Dealer,4->dealerAdmin,5->Employee"),pincode:str=Form(None),
                     dealer_id : int=Form(None),
                     dealer_code : str = Form(None)
                     ):
    
    user = get_user_token(db=db,token=token)
    if user:
        getUser = db.query(User).filter(User.user_type != 6)
        check_username = getUser.filter(User.username == userName).first()
        check_email = getUser.filter(User.email == email ).first()
        check_phone = getUser.filter(User.phone == phoneNumber).first()
        if contains_emoji(userName):
                return {"status":0,"msg":"Emojis are not allowed to use."}
        if email:
                if contains_emoji(email):
                    return {"status":0,"msg":"Emojis are not allowed to use in email."}
        if contains_emoji(name):
                return {"status":0,"msg":"Emojis are not allowed to use in name."}
        if userType in [2,3]:
            if check_username:
                 return {"status":0,"msg":"Username already exists."}
            if check_email:
                return {"status":0,"msg":"Email already exists."}
            if check_phone:
                return {"status":0,"msg":"PhoneNumber already exists."}
        if userType == 2:
           if user.user_type != 1:
                return {"status":0,"msg":"You are not authorized to create admin."}
        dealer_code = None
        if userType == 3 :
            if user.user_type not in [1,2]:
                  return {"status":0,"msg":"You are not authorized to create dealer."}
            check_dealerCode = getUser.filter(User.dealer == dealer_code).first()
            if check_dealerCode:
                 return {"status":0,"msg":"DealerCode already exits"}
        if user.user_type == 3:
            if not userType:
                return {"status":0,"msg":"Need user type."}
        if userType in [4,5]:
                if not dealer_id and not user.user_type == 3:
                        return {"status":0,"msg":"Need dealer."}
                if dealer_id:
                     dealer = getUser.filter(User.id == dealer_id).first()
                     dealer_code = dealer.dealer_code
                elif user.user_type == 3:
                    dealer_id = user.id
                    dealer_code = user.dealer_code
                checkDealerId = getUser.filter(User.id == dealer_id,User.user_type == 3,User.is_active == True).first()
                check_username = getUser.filter(User.username == userName,User.dealer_id == dealer_id,User.is_active == True).first()
                check_email = getUser.filter(User.email == email,User.dealer_id == dealer_id,User.is_active == True).first()
                check_phone = getUser.filter(User.phone == phoneNumber,User.dealer_id == dealer_id,User.is_active == True).first()
                if not checkDealerId:
                        return {"status":1,"msg":"Invalid dealer."}
                if userType == 4:
                     check_dealerAdmin = getUser.filter(User.dealer_id == dealer_id,User.user_type == 4,User.is_active == True).first()
                     if check_dealerAdmin:
                          return {"status":0,"msg":"Dealer Admin already exists."}
                if check_username:
                    return {"status":0,"msg":"Username already exists."}
                if check_email:
                    return {"status":0,"msg":"Email already exists."}
                if check_phone:
                    return {"status":0,"msg":"PhoneNumber already exists."}   
        else:
                    dealer_id =None


        createUsers = User(
                    user_type = userType,
                    name = name,
                    username = userName,
                    email = email,
                    phone = phoneNumber,
                    states = state,
                    city = city,
                    landline_number = landline_number,
                    country = country,
                    pincode = pincode,
                    password =  get_password_hash(password) if password !=None else None,
                    dealer_code = dealer_code,
                    dealer_id = dealer_id,
                    is_active = 1,
                    created_at = datetime.now(settings.tz_IN),
                    updated_at = datetime.now(settings.tz_IN),
                    status =1)
                
        db.add(createUsers)
        db.commit()

        return {"status":1,"msg":"User created successfully."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}
    
@router.post("/update_user")
async def updateUser(db : Session = Depends(get_db),
                     token:str=Form(...),name:str = Form(...),
                     userName:str=Form(None),phoneNumber:str=Form(...),
                     state:str=Form(None),city:str=Form(None),country:str=Form(None),
                     email:str=Form(None),
                     landline_number:str=Form(None),
                     userType:int=Form(None,description="2->Admin,3->dealer,4->dealerAdmin,5->Employee"),pincode:str=Form(None),
                     dealer_id : int=Form(None),
                     userId:int=Form(...)):
    
    user=get_user_token(db=db,token=token)
    if user:
        if user.user_type !=5:
            if contains_emoji(userName):
                return {"status":0,"msg":"Emojis are not allowed to use."}
            if email:
                if contains_emoji(email):
                    return {"status":0,"msg":"Emojis are not allowed to use in email."}
            if contains_emoji(name):
                return {"status":0,"msg":"Emojis are not allowed to use in email."}
            
            getUser = db.query(User).filter(User.user_type != 6)
            checkUserId = getUser.filter(User.id == userId,User.user_type!=1).first()
            if checkUserId:
                if userType in [2,3]:
                    check_username = getUser.filter(User.username == userName).first()
                    check_email = getUser.filter(User.email == email).first()
                    check_phone = getUser.filter(User.phone == phoneNumber).first()
                    if check_username:
                        return {"status":0,"msg":"Username already exists."}
                    if check_email:
                        return {"status":0,"msg":"Email already exists."}
                    if check_phone:
                        return {"status":0,"msg":"PhoneNumber already exists."}
                    if userType == 2:
                        if user.user_type != 1:
                            return {"status":0,"msg":"You are not authorized to Edit admin."}
                if userType in [4,5]:
                    if user.user_type == 3:
                        dealer_id == user.id
                    if not dealer_id:
                        return {"status":0,"msg":"dealer needed"}
                    check_dealer = getUser.filter(User.id==dealer_id,User.user_type == 3,User.is_active == True).first()
                    check_username = getUser.filter(User.username == userName,User.dealer_id == dealer_id,User.is_active == True).first()
                    check_email = getUser.filter(User.email == email,User.dealer_id == dealer_id,User.is_active == True).first()
                    check_phone = getUser.filter(User.phone == phoneNumber,User.dealer_id == dealer_id,User.is_active == True).first()
                    if not check_dealer:
                        return {"status":0,"msg":"Dealer not found"}
                    if not checkUserId.dealer_id != dealer_id:
                          return {"status":0,"msg":"Employee not found under this dealer"}
                    if check_username:
                        return {"status":0,"msg":"Username already exists."}
                    if check_email:
                        return {"status":0,"msg":"Email already exists."}
                    if check_phone:
                        return {"status":0,"msg":"PhoneNumber already exists."}
                else:
                        dealer_id =None

                checkUserId.user_type = userType
                checkUserId.name = name
                checkUserId.user_name = userName
                checkUserId.email = email
                checkUserId.phone = phoneNumber
                checkUserId.states = state
                checkUserId.landline_number = landline_number
                checkUserId.city = city
                checkUserId.country = country
                checkUserId.pincode = pincode
                checkUserId.dealer_id = dealer_id
                checkUserId.updated_at = datetime.now(settings.tz_IN)
                    
                db.commit()

                return {"status":1,"msg":"User successfully updated."}
            else:
                return {"status":0,"msg":"Invalid user."}
        else:
            return {"status":0,"msg":"You are not authenticated to modify any users."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}

@router.post("/list_users")
async def listUser(db:Session =Depends(get_db),
                   token:str=Form(...),page:int=1,
                   size:int=10,phoneNumber:str=Form(None),
                   type:int=Form(...,description="2->Admin,3->Dealer4->Dealer Admin5->Employee"),
                   email:str=Form(None),dealerId:int=Form(None),
                   username:str=Form(None)
                   ):
    user = get_user_token(db=db,token=token)

    if user:
        if user.user_type !=5:            
            
            getAllUser = db.query(User).filter(User.user_type == type,User.status==1)
            if user.user_type == 2:
                getAllUser = getAllUser.filter(User.user_type!=2)

            elif user.user_type == 3:
                getAllUser = getAllUser.filter(User.dealer_id == user.id,
                                               User.user_type not in [2,3])
            if phoneNumber:
                getAllUser = getAllUser.filter(User.phone.like("%"+phoneNumber+"%") )
            if email:
                getAllUser = getAllUser.filter(User.email == email)

            if dealerId:
                getAllUser = getAllUser.filter(User.dealer_id == dealerId)
            if username:
                getAllUser = getAllUser.filter(User.name.like("%"+username+"%"))
            
            getAllUser = getAllUser.order_by(User.name.asc())
            
            userCount = getAllUser.count()
            totalPages,offset,limit = get_pagination(userCount,page,size)
            getAllUser = getAllUser.limit(limit).offset(offset).all()
            
            userTypeData = ["-","-","Admin","Dealer","Dealer Admin","Employee","Customer"]
            dataList = []
            if getAllUser:
                for userData in getAllUser:
                    dataList.append(
                        {
                            "userId":userData.id,
                            "userName":userData.username,
                            "name":userData.name,
                            "landline_number":userData.landline_number,
                            "phoneNumber":userData.phone,
                            "whatsapp_no":userData.whatsapp_no if userData.whatsapp_no else None,
                            "email":userData.email,
                            "userStatus":userData.is_active,
                            "userType":userData.user_type,
                            "userTypeName": userTypeData[userData.user_type],
                            "dealer_id":userData.dealer_id ,
                            "dealerName":userData.dealer.username if userData.dealer_id else None,
                            "location":userData.city
                        }
                    )
            data=({"page":page,"size":size,
                    "total_page":totalPages,
                    "total_count":userCount,
                    "items":dataList})
            
            return ({"status":1,"msg":"Success.","data":data})
        else:
            return {"status":0,"msg":"You are not authenticated to see the user details."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}


@router.post("/view_user")
async def viewUser(db:Session=Depends(get_db),
                   token:str=Form(...),
                   userId:int=Form(...)):
    user = get_user_token(db=db,token=token)
    if user:
        if user.user_type !=5:
            getUser = db.query(User).filter(User.id == userId,
                                            User.status == 1)
            if user.user_type ==3:
                getUser = getUser.filter(User.dealer_id == user.id)
            if user.user_type == 4:
                 getUser = getUser.filter(User.dealer_id == user.dealer_id)
            getUser = getUser.first()
            userTypeData = ["-","Super Admin","Admin","Dealer","Dealer Admin","Employee"]
            if getUser:
                data ={
                    "userId":userId,
                    "name":getUser.name,
                    "userName":getUser.username,
                    "userType":getUser.user_type,
                    "userTypeName":userTypeData[getUser.user_type],
                    "active_status":getUser.is_active,
                    "email" : getUser.email,
                    "phoneNumber": getUser.phone,
                    "whatsapp_no":getUser.whatsapp_no if getUser.whatsapp_no else None,

                    "stateName":getUser.states,
                    "cityName":getUser.city,
                    "countryName":getUser.country,
                    "pincode":getUser.pincode,
                    "dealerId":getUser.dealer_id,
                    "dealerName":getUser.dealer.username if getUser.dealer_id else None


                }
            return {"status":1,"msg":"Success.","data":data}
        else:
            return {'status':0,"msg":"You are not authenticated to view any user."}
    return {"status":-1,"msg":"Your login session expires.Please login again."}

@router.post("/delete_user")
async def deleteUser(db:Session=Depends(get_db),
                     token:str = Form(...),
                     userId:int=Form(...)):
    user = get_user_token(db=db,token=token)
    if user:
        if user.user_type not in [4,5]:
            getUser = db.query(User).filter(User.id == userId,
                                            User.status == 1)
            if user.user_type ==3:
                getUser = getUser.filter(User.dealer_id == user.id)
            if user.user_type ==4:
                 getUser = getUser.filter(User.dealer_id == user.dealer_id)
            if getUser.first() == None:
                 return {"status":0,"msg":"There is no user"}
            getUser = getUser.update({"status":-1,"is_active":-1})
            db.commit()
            return {"status":1,"msg":"User successfully deleted."}
        else:
            return {'status':0,"msg":"You are not authenticated to delete any user"}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login again."}

@router.post("active_inactive_user")
async def activeInactiveUser(db:Session=Depends(get_db),
                             token:str=Form(...),userId:int=Form(...),
                             activeStatus:int=Form(...,description="1->active,2->inactive")):
    user = get_user_token(db=db,token=token)
    if user:
        if user.user_type !=5:
            getUser = db.query(User).filter(User.id == userId,
                                            User.status == 1)
            if user.user_type ==3:
                getUser = getUser.filter(User.dealer_id == user.id)
            if user.user_type ==4:
                 getUser = getUser.filter(User.dealer_id == user.dealer_id)
            if getUser.first() == None:
                 return {"status":0,"msg":"There is no user"}
            getUser = getUser.update({"is_active":activeStatus})
            db.commit()
            message ="Success."
            if activeStatus ==1:
                message ="User successfully activated."
            else:
                message ="User successfully deactivated."

            return {"status":1,"msg":message}
        else:
            return {'status':0,"msg":"You are not authenticated to change status of any user"}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login again."}
