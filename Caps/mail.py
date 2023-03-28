"""функции для отправления писем на почту"""
import smtplib
from typing import List
from email import encoders
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase
from typing import Tuple

  
def authentificate(login: str, password: str) -> Tuple[bool, str, smtplib.SMTP]:
    """
    Возвращает False и строку ошибки, если не удалось подключиться к почте
    При успешном подключении возвращает True и объект SMTP
    """
    if login.endswith("mail.ru"):
        smtpObj = smtplib.SMTP('smtp.mail.ru', 587)
    elif login.endswith("gmail.com"):
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    elif login.endswith("inbox.ru"):
        smtpObj = smtplib.SMTP('smtp.inbox.ru', 587)
    elif login.endswith("yandex.ru"):
        smtpObj = smtplib.SMTP('smtp.yandex.ru', 587)
    
    smtpObj.starttls()

    try:
        smtpObj.login(login, password)
        return (True, "Успешно", smtpObj)
    except smtplib.SMTPResponseException as e:
        error_code = e.smtp_code
        error_message = e.smtp_error
        if(error_code==535):
            error_message = "Для входа необходим пароль приложения"
        elif(error_code==553):
            error_message = "Проверь все адреса в Кому, CC и BCC полях. Где-то должна быть ошибка или неправильное написание"
        
        return (False, f"{error_code}: " + error_message, smtpObj)
        
def createMessage(FROM: str, TO: str, message: str, Subject: str = "Отчёт", filepaths: List[str] = list()) -> MIMEMultipart:
    """filepath - путь для прикрепления файла, допускаются только англоязычные названия"""
    msg = MIMEMultipart()
    msg["Subject"] = Subject
    msg["From"] = FROM
    msg["To"] = TO

    msg.attach(MIMEText(message, 'plain', 'utf-8'))

    if len(filepaths) != 0:
        for filepath in filepaths:
            part = MIMEBase("application", "octet-stream")
            with open(filepath, "rb") as attachment:
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= {filepath}")

            msg.attach(part)

    return msg

def sendMessage(SMTP: smtplib.SMTP, message: MIMEMultipart):
    """SMTP - здесь это экземпляр, возвращаемый из authentificate"""
    SMTP.sendmail(message["From"], message["To"], message.as_string())

