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
                     email:str=Form(...),
                     landline_number:str=Form(None),
                     state:str=Form(None),city:str=Form(None),country:str=Form(None),password:str=Form(...),
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
        if userType == 3 :
            if user.user_type not in [1,2]:
                  return {"status":0,"msg":"You are not authorized to create dealer."}
            check_dealerCode = getUser.filter(User.dealer_code == dealer_code).first()
            if check_dealerCode:
                 return {"status":0,"msg":"DealerCode already exits"}
        if user.user_type == 3:
            if not userType:
                return {"status":0,"msg":"Need user type."}
        if userType in [4,5]:
                if not dealer_id and not user.user_type == 3:
                        return {"status":0,"msg":"Need dealer."}
                elif user.user_type == 3:
                    dealer_id = user.id
                    dealer_code = user.dealer_code
                checkDealerId = getUser.filter(User.id == dealer_id,User.user_type == 3,User.is_active == True).first()
                check_username = getUser.filter(User.username == userName,User.dealer_id == dealer_id,User.is_active == True).first()
                check_email = getUser.filter(User.email == email,User.dealer_id == dealer_id,User.is_active == True).first()
                check_phone = getUser.filter(User.phone == phoneNumber,User.dealer_id == dealer_id,User.is_active == True).first()
                if not checkDealerId:
                        return {"status":1,"msg":"Invalid dealer."}
                if dealer_id:
                     dealer = getUser.filter(User.id == dealer_id).first()
                     dealer_code = dealer.dealer_code
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
                            "dealer_code":userData.dealer_code,
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
                return {'status':0,'msg':'User not found'}
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


@router.post("/create_customer")
async def createCustomer(db:Session =Depends(get_db),
                        token:str=Form(...),name:str=Form(None),
                        contact_person:str=Form(None),
                        phone_country_code:str=Form(None),
                        whatsapp_country_code:str=Form(None),
                        alter_country_code:str=Form(None),
                        phone:str=Form(None),
                        alternative_no:str=Form(None),
                        landline_number:str=Form(None),
                        whatsapp_no:str=Form(None),
                        address:str=Form(None),
                        area :str=Form(None),
                        email:str=Form(None),
                        companyName:str=Form(None),
                        pincode:str=Form(None),state:str = Form(None),
                        city:str=Form(None)):
    
    user = get_user_token(db=db,token=token)
    if user:
        if user.user_type in [1,2,3,4]:
            getUser = db.query(User).filter(User.user_type == 6,User.status == 1)
            if whatsapp_no == None and phone == None and landline_number == None and email == None:
                return {"status":0,"msg":"Please fill Any one of the Contact Information"}
            if name == None and contact_person == None and companyName == None:
                return {"status":0,"msg":"Please fill Company Name or Contact Person"}
            if email:
                checkEmail = getUser.filter(User.email == email ).first()
                if checkEmail:
                    return {"status":0,"msg":"Email already exists."}
            if phone:
                if not phone.isdigit():
                    return {"status":0,"msg":"Invalid Phone Number"}
                checkMobileNumber = getUser.filter(or_(User.phone == phone,
                                                    User.alternative_number == phone,
                                                    User.whatsapp_no == phone)).first()
                if checkMobileNumber:
                    return {"status":0,"msg":"Mobile number already in use."}
            if alternative_no:
                if not alternative_no.isdigit():
                    return {"status":0,"msg":"Alternative number should be numeric."}
                checkAlternativeMobile = getUser.filter(or_(User.phone == alternative_no,
                                                   User.alternative_number == alternative_no,
                                                   User.whatsapp_no == alternative_no)).first()
                if checkAlternativeMobile:
                    return {"status":0,"msg":"Mobile number already in use."}
            if whatsapp_no:
                if not whatsapp_no.isdigit():
                    return {"status":0,"msg":"Invalid WhatsApp Number"}
                checkWhatsApp = getUser.filter(or_(User.phone == whatsapp_no,
                                                   User.alternative_number == whatsapp_no,
                                                   User.whatsapp_no == whatsapp_no)).first()
                if checkWhatsApp:
                    return {"status":0,"msg":"Mobile number already in use."}

            
            createNewCustomer = User(
                user_type = 6,
                name = name,
                username = contact_person,
                phone = phone,
                alternative_number = alternative_no,
                phone_country_code =phone_country_code,
                whatsapp_country_code =whatsapp_country_code,
                alter_country_code =alter_country_code,
                whatsapp_no = whatsapp_no,
                landline_number = landline_number,
                address = address,
                area = area,
                states = state,
                city = city,
                pincode = pincode,
                created_at = datetime.now(settings.tz_IN),
                status = 1,
                email = email,
                company_name=companyName,
                is_active = 1
            )

            db.add(createNewCustomer)
            db.commit()
            return {"status":1,"msg":"Customer successfully created."}
        else:
            return {"status":0,"msg":"You are not authenticate to add any customer."}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login again."}

@router.post("/update_customer")
async def updateCustomer(db: Session = Depends(get_db),
                         token:str=Form(None),name:str=Form(None),
                         contact_person:str=Form(None),
                         phone:str=Form(None),
                          phone_country_code:str=Form(None),
                        whatsapp_country_code:str=Form(None),
                        alter_country_code:str=Form(None),
                         alternative_no:str=Form(None),
                         whatsapp_no:str=Form(None),
                         address:str=Form(None),
                         landline_number:str=Form(None),
                          area :str=Form(None),
                          email:str=Form(None),
                          companyName:str=Form(None),
                          pincode:str=Form(None),state:str = Form(None),
                          country:str = Form(None),
                          city:str=Form(None),CustomerId:int=Form(...)
                         ):
    user = get_user_token(db=db,token=token)
    if user:
        if user.user_type in [1,2,3,4]:
            getUser = db.query(User).filter(User.user_type ==6,User.status == 1)
            checkUserId = getUser.filter(User.id == CustomerId).first()
            exceptionCustomer = getUser.filter(User.id != CustomerId)

            if not checkUserId:
                return {'status':0,"msg":"No customer record found."}
            if whatsapp_no == None and phone == None and landline_number == None and email == None:
                return {'status':0,"msg":"Please enter any contact number or email."}
            if name == None and contact_person == None or companyName == None:
                return {"status":0,"msg":"Please fill Company Name or Contact Person"}
            if email:
                checkEmail = exceptionCustomer.filter(User.email == email ).first()
                if checkEmail:
                    return {"status":0,"msg":"Email already exists."}
            if phone:
                if not phone.isdigit() or not phone.count() == 10:
                    return {"status":0,"msg":"Please enter valid phone number."}
                checkMobileNumber = exceptionCustomer.filter(or_(User.phone == phone,
                                                    User.alternative_number == phone,
                                                    User.whatsapp_no == phone)).first()
                if checkMobileNumber:
                    return {"status":0,"msg":"Mobile number already in use."}
            if alternative_no:
                if not alternative_no.isdigit():
                    return {"status":0,"msg":"Please enter valid alternative phone number."}
                checkAlternativeMobile = exceptionCustomer.filter(or_(User.phone == alternative_no,
                                                   User.alternative_number == alternative_no,
                                                   User.whatsapp_no == alternative_no)).first()
                if checkAlternativeMobile:
                    return {"status":0,"msg":"alternative Mobile number already in use."}
            if whatsapp_no:
                if not whatsapp_no.isdigit():
                    return {"status":0,"msg":"Please enter valid whatsapp number."}
                checkWhatsApp = exceptionCustomer.filter(or_(User.phone == whatsapp_no,
                                                   User.alternative_number == whatsapp_no,
                                                   User.whatsapp_no == whatsapp_no)).first()
                if checkWhatsApp:
                    return {"status":0,"msg":"Whatsapp number already in use."}
            
            
            checkUserId.name = name
            checkUserId.username = contact_person
            checkUserId.phone = phone
            checkUserId.alternative_number = alternative_no
            checkUserId.phone_country_code = phone_country_code
            checkUserId.whatsapp_country_code = whatsapp_country_code
            checkUserId.alter_country_code = alter_country_code
            checkUserId.whatsapp_no = whatsapp_no
            checkUserId.address = address
            checkUserId.area = area
            checkUserId.states = state
            checkUserId.city = city
            checkUserId.country = country
            checkUserId.pincode = pincode
            checkUserId.updated_at = datetime.now(settings.tz_IN)
            checkUserId.email = email
            checkUserId.company_name = companyName
            
            db.commit()
            return {"status":1,"msg":"Customer details updated successfully."}
        else:
            return {"status":0,"msg":"You are not authenticated to update/edit customer details."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}


@router.post("/list_customer")
async def listCustomers(db:Session =Depends(get_db),
                        token:str=Form(...),
                        page:int=1,size:int=10,
                        mobileNumber:str=Form(None),
                        name:str=Form(None),state:str = Form(None),
                          country:str = Form(None),
                          city:str=Form(None),):
    user = get_user_token(db=db,token=token)
    if user:
        if user.user_type in [1,2,3,4]:
            getAllCustomer = db.query(User).filter(User.user_type == 6,
                                                   User.status == 1)
            if mobileNumber:
                getAllCustomer = getAllCustomer.\
                    filter(or_(User.phone.like('%'+mobileNumber+'%'),
                               User.alternative_number.like('%'+mobileNumber+'%'),
                               User.whatsapp_no.like('%'+mobileNumber+'%')))
            if name:
                getAllCustomer = getAllCustomer.filter(or_(User.name.like('%'+name+'%'),
                                                           User.user_name.like("%"+name+"%")))
            if state:
                getAllCustomer = getAllCustomer.filter(User.states.like("%"+state+"%"))  
            if country:
                getAllCustomer = getAllCustomer.filter(User.country.like("%"+country+"%"))
            if city:
                getAllCustomer = getAllCustomer.filter(User.city.like("%"+city+"%"))
            
            getAllCustomer = getAllCustomer.order_by(User.name.asc())
            
            totalCount = getAllCustomer.count()
            totalPages,offset,limit = get_pagination(totalCount,page,size)
            getAllCustomer = getAllCustomer.limit(limit).offset(offset).all()
            dataList = []
            if getAllCustomer:
                for row in getAllCustomer:
                    dataList.append({"customerId":row.id,
                                     "name":row.name,
                                     "contactPerson":row.username,
                                     "phone":row.phone,
                                     "alternative_number":row.alternative_number,
                                     "phone_country_code" : row.phone_country_code,
                                    "whatsapp_country_code" :row.whatsapp_country_code,
                                    "alter_country_code" : row.alter_country_code,
                                     "address":row.address,
                                     "area":row.area,
                                    "whatsapp_no":row.whatsapp_no if row.whatsapp_no else None,

                                    "stateName":row.states,
                                    "cityName":row.city,
                                    "countryName":row.country,
                                    "pincode":row.pincode,
                                    "email":row.email,
                                    "companyName":row.company_name
                                     })
            data=({"page":page,"size":size,
                "total_page":totalPages,
                "total_count":totalCount,
                "items":dataList})
            
            return ({"status":1,"msg":"Success.","data":data})
        else:
            return {"status":0,"msg":"You are not authenticated to see the customer details."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}
    
@router.post("/delete_customer")
async def deleteCustomer(db:Session=Depends(get_db),
                         token:str=Form(...),
                         customerId:int=Form(...)):
    user = get_user_token(db=db,token=token)
    if user:
        if user.user_type in [1,2]:
            deleteCustomer = db.query(User).\
                filter(User.id == customerId,
                User.user_type == 6).update({"status":-1,"is_active":-1})
            db.commit()

            return {"status":1,"msg":"Customer details successfully removed."}
        else:
            return {"status":0,"msg":"You are not authenticated to delete the customer record."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}
