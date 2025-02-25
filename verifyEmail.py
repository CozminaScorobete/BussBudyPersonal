from email.message import EmailMessage
import ssl
import smtplib

def sendEmail(receiver,nr):
    email_sender= 'cozminascorobete@gmail.com'
    email_password='qhjkkkxocigrsybh'
    email_receiver=receiver
    subject='Validare Email'
    body="""
    Buna ziua,

    Introduceti codul in casuta de pe site
    """+str(nr)
    em=EmailMessage()
    em['From']=email_sender
    em['Ro']=email_receiver
    em['Subject']=subject
    em.set_content(body)
    context=ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender,email_receiver,em.as_string())
        









