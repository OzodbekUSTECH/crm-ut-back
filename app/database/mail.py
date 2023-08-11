# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
# from services.users import UsersService
# from services.maillist import MailListService
# from fastapi import Depends
# from schemas.maillist import SendMailMessageSchema
# from utils.dependency import get_users_services, get_maillist_services

# conf = ConnectionConfig(
#     MAIL_USERNAME = "naimovozod81@gmail.com",
#     MAIL_PASSWORD = "nqddzknaqybrdojn",
#     MAIL_FROM = "naimovozod81@gmail.com",
#     MAIL_PORT = 587,
#     MAIL_SERVER = "smtp.gmail.com",
#     MAIL_FROM_NAME = "Desired Name",
#     MAIL_STARTTLS = True,
#     MAIL_SSL_TLS = False,
#     USE_CREDENTIALS = True,
#     VALIDATE_CERTS = True
# )


# class EmailSender:
#     def __init__(
#             self, 
#             users_service: UsersService = Depends(get_users_services),
#             maillist_service: MailListService = Depends(get_maillist_services)
#     ):
#         self.fm = FastMail(conf)
#         self.users_service = users_service
#         self.maillist_service = maillist_service
    
#     async def send_password(self, email: str, password: str):
#         message = MessageSchema(
#             subject="Your Password",
#             recipients=[email],
#             body=f"Your password: {password}",
#             subtype=MessageType.html
#         )
#         await self.fm.send_message(message)

#     async def send_reset_password_link(self, email: str):
#         user = await self.users_service.get_user_by_email(email)
#         if user:
#             reset_token = await self.users_service.generate_reset_token(user.email)
#             reset_link = f"http://localhost:8000/reset/password?token={reset_token}"

#             html = f"<p>Click the link below to reset your password:</p><p><a href='{reset_link}'>{reset_link}</a></p>"

#             message = MessageSchema(
#                 subject="Reset Password",
#                 recipients=[user.email],
#                 body=html,
#                 subtype=MessageType.html
#             )

#             await self.fm.send_message(message)

#             return {"message": "Reset Password sent successfully"}
#         return {"message": "Incorrect email address"}
    
#     async def send_message_to_all_emails(self, mail_data: SendMailMessageSchema):
#         emails = await self.maillist_service.get_emails_without_pagination()
#         all_emails = []
#         for email in emails:
#             all_emails.append(email.email)
            
#         message = MessageSchema(
#             subject = mail_data.subject,
#             recipients=all_emails,
#             body = mail_data.body,
#             subtype=MessageType.html
#         )
#         await self.fm.send_message(message)
