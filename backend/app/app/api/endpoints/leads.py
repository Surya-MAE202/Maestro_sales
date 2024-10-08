from app.models import User
from app.api.deps import *
from app.core.config import settings
from datetime import datetime
from app.utils import *
from sqlalchemy import *
from app.core.security import *
from fastapi import APIRouter, Depends, Form,requests,UploadFile,File
from sqlalchemy.orm import Session
from app.models import *
from app.core.security import get_password_hash,verify_password
from typing import Optional,List,Union

router = APIRouter()



# @router.post("/create_lead")
# async def createLead(db:Session=Depends(get_db),
#                      token:str = Form(...),name:str=Form(...),
#                      remarks:str=Form(None),
#                      phone_country_code:str=Form(...),
#                      landline_number:str=Form(None),
#                      whatsapp_country_code:str=Form(None),
#                      alter_country_code:str=Form(None),
#                      alternative_no:str=Form(None),whatsapp_no:str=Form(None),
#                      company_name :str=Form(None),
#                      contact_person:str=Form(None),
#                      address:str=Form(...),
#                      area:str=Form(None),
#                      phone:str=Form(...),email:str=Form(None),
#                      customer_category_id:int = Form(None),
#                      enquiry_type_id:int = Form(None),
#                      requirements_id:str=Form(...),
#                      state:str = Form(None),country:str=Form(None),city:str=Form(None),
#                      dealer_id:int=Form(None),
#                      assignedTo:int=Form(None),
#                      receivedDate:datetime=Form(None),
#                      referedBy:str = Form(None),referedPhone:str=Form(None),
#                      refer_country_code:str=Form(None),notes:str=Form(None),
#                      description:str=Form(None),isNew:int=Form(None),
#                      latitude:str=Form(None),
#                      longitude:str=Form(None),
#                      customerId:int=Form(None),Pincode:str=Form(None),
#                      schedule_date:datetime=Form(None),
#                     upload_file:Optional[Union[UploadFile,List[UploadFile]]] = File(default=None),
#                      approximate_amount:str=Form(None),
#                     ):
    
#     user = get_user_token(db=db , token=token)
#     if user:
#         if contains_emoji(name):
#             return {"status":0,"msg":"Emojis are not allowed to use."}
#         if company_name:
#             if contains_emoji(company_name):
#                 return {"status":0,"msg":"Emojis are not allowed to use."}
#         if contact_person:
#             if contains_emoji(contact_person):
#                 return {"status":0,"msg":"Emojis are not allowed to use."}
#         if email:
#             if contains_emoji(email):
#                 return {"status":0,"msg":"Emojis are not allowed to use in email."}
#         leadStatusID = 1
#         dealer = None
#         assignedUser= None
#         getAllUsers = db.query(User).filter(User.status == 1)

#         if user.user_type in [1,2]:

#             if schedule_date:
#                 if schedule_date<datetime.now():
#                         return{"status":0,"msg":"Only future datetime are allowed."}
#             if dealer_id:
#                 checkDealerId = getAllUsers.filter(User.id == dealer_id,
#                                                    User.user_type == 3).first()
#                 if not checkDealerId:
#                     return {"status":0,"msg":"No dealer record found."}
#                 dealer = dealer_id
#             else:
#                 dealer = None

#         elif user.user_type ==3: # 3 -> dealer 
#             dealer = user.id
#         elif user.user_type == 4:
#             dealer = user.dealer_id    

#         elif user.user_type == 5: # 5 -> employee
#             dealer = user.dealer_id
#             assignedUser = user.id
#             leadStatusID = 2
        
#         if user.user_type != 5:
#             if not assignedTo :
#                 assignedUser = None
#             else:
#                 checkUser = getAllUsers.filter(User.id == assignedTo,
#                                                 User.user_type==5).first()
#                 if not checkUser:
#                     return {"status":0,"msg":"No employee record found."}
#                 else:
#                     assignedUser = assignedTo
#                     leadStatusID = 2
    
            
#         checkuser = db.query(User).filter(User.status == 1)
#         if isNew: 
#             checkMobile = checkuser.filter(or_(User.phone==phone,
#                                                     User.alternative_number ==phone,
#                                                     User.whatsapp_no == phone)).first()
#             if checkMobile :
#                 return {"status":0,"msg":"This mobile number already exists."}
#             if alternative_no:
#                 if phone != alternative_no:
#                     checkMobile = checkuser.filter(or_(User.phone==alternative_no,
#                                                     User.alternative_number ==alternative_no,
#                                                     User.whatsapp_no == alternative_no)).first()
#                     if checkMobile :
#                         return {"status":0,"msg":"This alternative mobile number already exists."}
#                 else:
#                     return {"status":0,"msg":"Mobile number and alternative mobile number not to be same."}
#             if  whatsapp_no:
#                 checkMobile = checkuser.filter(or_(User.phone==whatsapp_no,
#                                                     User.alternative_number ==whatsapp_no,
#                                                     User.whatsapp_no == whatsapp_no)).first()
#                 if checkMobile :
#                     return {"status":0,"msg":"This whatsapp number already exists."}
                
                
#         getAllReqId = [int(row) for row in requirements_id.split(",") ]
    
#         # filter_conditions = [Lead.requirements_id.like(f"%{req}%") for req in getAllReqId]
#         filter_conditions = [Lead.requirements_id.op('REGEXP')(rf'\b{req}\b') for req in getAllReqId]


#         combined_filter = or_(*filter_conditions)

#         today = datetime.now(settings.tz_IN).date()

#         sameReqLead = db.query(Lead).filter(
#             Lead.status==1,combined_filter,
#             cast(Lead.created_t,Date)==today)
        
        
#         existNumber = sameReqLead.filter(or_(Lead.phone==phone,
#                 Lead.alternative_no ==phone,
#                 Lead.whatsapp_no==phone,)).first()
        
#         if existNumber:
#             return {"status":0,"msg":"This Requirement already exists With Same Phone Number."}
        
#         if whatsapp_no:

#             existWtsNumber = sameReqLead.filter(or_(Lead.phone==whatsapp_no,
#                 Lead.alternative_no ==whatsapp_no,
#                 Lead.whatsapp_no==whatsapp_no,)).first()
            
#             if existWtsNumber:
#                 return {"status":0,"msg":"This Requirement already exists With Same Whatsapp Number."}
            
#         if alternative_no:

#             existAltNumber = sameReqLead.filter(or_(Lead.phone==alternative_no,
#                 Lead.alternative_no ==alternative_no,
#                 Lead.whatsapp_no==alternative_no,)).first()
            
#             if existAltNumber:
#                 return {"status":0,"msg":"This Requirement already exists With Same alternative Number."}

            
#         if customer_category_id: 
#             checkCategory = db.query(CustomerCategory).filter(CustomerCategory.id == customer_category_id,
#                                                               CustomerCategory.status ==1 ).first()

#             if not checkCategory:
#                 return {"status":0,"msg":"Invalid customer category"}
            
#         if enquiry_type_id:
#             checkEnquiry = db.query(EnquiryType).filter(EnquiryType.id == enquiry_type_id,
#                                                         EnquiryType.status.in_([1,2])).first()
#             if not checkEnquiry:
#                 return {"status":0,"msg":"Invalid Enquiry type "}
        
        
#         checkRequirementsId = db.query(Requirements).filter(Requirements.id.in_(getAllReqId),
#                                                    Requirements.status ==1).first()
#         isvalid = 1
#         if not checkRequirementsId:
#             return {"status":0,"msg":"Invalid Requirement"}
#         # print(getAllReqId)
#         if 20 in getAllReqId:
#             # print("PResent")
#             leadStatusID = 17      

#         if not isNew:
#             customer = customerId
#         else:
#             createNewUser = User(
#                user_type =5,
#                name = name,
#                phone_country_code = phone_country_code,
#                whatsapp_country_code = whatsapp_country_code,
#                alter_country_code = alter_country_code,
#                user_name = contact_person,
#                landline_number=landline_number,
#                phone = phone,
#                alternative_number = alternative_no,
#                whatsapp_no = whatsapp_no,
#                address = address,
#                area = area,
#                states = state,
#                city = city,
#                country = country,
#                pincode = Pincode,
#                created_at = datetime.now(settings.tz_IN),
#                status =1,
#                email = email,
#                company_name = company_name,
#                is_active = 1
#             )

#             db.add(createNewUser)
#             db.commit()

#             customer = createNewUser.id

#         today = datetime.now(settings.tz_IN)
        
#         createNewLead = Lead(
#             name = name,
#             remarks = remarks,
#             customer_id = customer ,
#             company_name = company_name,
#             contact_person = contact_person,
#             lead_code =0,
#             phone = phone,
#             alternative_no = alternative_no,
#             whatsapp_no = whatsapp_no,
#             address =address,
#             area = area,
#             customer_category_id =customer_category_id,
#             enquiry_type_id = enquiry_type_id,
#             requirements_id = requirements_id,
#             email = email,
#             states = state,
#             city = city,
#             country = country,
#             approximate_amount =approximate_amount,
#             landline_number=landline_number,

#             pincode = Pincode,
#             lead_status_id = leadStatusID,
#             dealer_id = dealer,
#             assigned_to = assignedUser,
#             received_at = receivedDate or today ,
#             refered_by = referedBy,
#             refer_country_code = refer_country_code,
#             refered_ph_no = referedPhone,
#             is_active = 0,
#             notes = notes,
#             comments_description = description,
#             created_t = today,
#             created_by = user.id,
#             update_at = today,
#             is_valid = isvalid,
#             status = 1,
#             schedule_date = schedule_date,
#             latitude= latitude,
#             longitude = longitude)
        
#         db.add(createNewLead)
#         db.commit()

#         # to update latitude and longitude
#         if checkEnquiry.status == 2:
#             createNewLead.latitude = latitude
#             createNewLead.longitude = longitude
#             db.commit()
    
#         newLeadName = "Lead"+str(createNewLead.id)
#         createNewLead.lead_code = newLeadName
#         db.commit()

#         historyId = None
#         followupId = None

#         comment = "Created" 
#         if schedule_date:
#             comment = f"Created (The follow-up date is scheduled for {schedule_date.strftime('%Y-%m-%d %H:%M')})"
#             newFollowUp = FollowUp(
#                 lead_id= createNewLead.id,
#                 followup_dt = schedule_date,
#                 createdBy = user.id,
#                 comment = comment,
#                 followup_status = 1,
#                 created_at = datetime.now(settings.tz_IN),
#                 status = 1,
#                 latitude = latitude,
#                 longitude = longitude,
#                 enquiry_type_id = enquiry_type_id  )
            
#             createNewLead.is_followup=1
#             db.add(newFollowUp)
#             db.commit()


#             followupId=newFollowUp.id


#             addHistory = LeadHistory(
#                 lead_id= createNewLead.id,
#                 followup_id = newFollowUp.id,
#                 leadStatus = "Follow up",
#                 lead_status_id =5,
#                 changedBy= user.id,
#                 comment = comment,
#                 created_at = datetime.now(settings.tz_IN),
#                 status = 1,
#                 latitude = latitude,
#                 longitude = longitude,
#                 enquiry_type_id = enquiry_type_id
#             )
           
#             db.add(addHistory)
#             db.commit()
#             historyId = addHistory.id

#             if checkEnquiry.status == 2:
#                 addHistory.latitude = latitude
#                 addHistory.longitude = longitude
#                 db.commit()
            

#         if not schedule_date:

#             createLeadHistory =  LeadHistory(
#                 lead_id = createNewLead.id,
#                 leadStatus = "Unassigned" if leadStatusID == 1 else "Assigned" if leadStatusID == 2 else "Not valid",
#                 lead_status_id = leadStatusID,
#                 changedBy = user.id,
#                 created_at = today,
#                 longitude = longitude,
#                 latitude = latitude,
#                 comment =comment,
#                 status=1  ,
#                 enquiry_type_id = enquiry_type_id, )
#             db.add(createLeadHistory)
#             db.commit()
#             historyId = createLeadHistory.id

            
#         if upload_file and upload_file != None:
#             if isinstance(upload_file, list):
                    
#                 for i in range(len(upload_file)):  
                    
#                     store_fname = upload_file[i].filename
                    
#                     f_name,*etn = store_fname.split(".")
                
#                     file_path,file_exe = file_storage(upload_file[i],f_name)
#                     add_file = LeadMedia(
#                         lead_id = createNewLead.id,
#                         url =file_exe,
#                         lead_history_id = historyId,
#                         followup_id =followupId,
#                         created_at = datetime.now(tz=settings.tz_IN),
#                         upload_by = user.id,
#                         status = 1,
#                     )  
#                     db.add(add_file)  
#                     db.commit()  
#             else:
#                 store_fname = upload_file.filename
                    
#                 f_name,*etn = store_fname.split(".")
#                 file_path,file_exe = file_storage(upload_file,f_name)
#                 add_file = LeadMedia(
#                         lead_id = createNewLead.id,
#                         url =file_exe,
#                         lead_history_id = historyId,
#                         followup_id =followupId,
#                         created_at = datetime.now(tz=settings.tz_IN),
#                         upload_by = user.id,
#                         status = 1,
#                     )  
#                 db.add(add_file)  
#                 db.commit()  


#         if dealer_id and user.user_type in [1,2]:
#             getEmp = db.query(User).filter(User.id==dealer_id).first()
#             if getEmp:
#                 sender_id = [getEmp.id]
#                 msg = {
#                     "msg_title": "Maestro Sales",
#                     "msg_body": "New Lead has been assigned to you.",
#                 }
#                 message_data = {"lead_id":createNewLead.id,"id":2}

#                 PushNotidy = send_push_notification(
#                     db, sender_id, msg, message_data
#                 )

#         if assignedTo:
#             getEmp = db.query(User).filter(User.id==assignedTo).first()
#             if getEmp:
#                 sender_id = [getEmp.id]
#                 msg = {
#                     "msg_title": "Maestro Sales",
#                     "msg_body": "New Lead has been assigned to you.",
#                 }
#                 message_data = {"lead_id":createNewLead.id,"id":2}

#                 PushNotidy = send_push_notification(
#                     db, sender_id, msg, message_data
#                 )

#         return({"status":1,"msg":"Lead record successfully created"})
#     else:
#         return {"status":-1,"msg":"Sorry your login session expires.Please login again. "}
