import smtplib
import email.message
from typing import Tuple

import listFuncs
  
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
        
def createMessage(FROM: str, TO: str, content: str, Subject: str = "Отчёт") -> email.message.Message:
    message = email.message.Message()
    message["Subject"] = Subject
    message["From"] = FROM
    message["To"] = TO

    if content.startswith("<!DOCTYPE html>"):
        message.add_header('Content-Type', 'text/html')
    else:
        message.add_header('content-disposition', 'attachment')
    
    message.set_payload(content, charset="utf-8")

    return message

def sendMessage(SMTP: smtplib.SMTP, message: email.message.Message):

    SMTP.sendmail(message['From'], [message['To']], message.as_string())


login = "vladshilov03@mail.ru"
password = "g1FHGGDk3CAs82TjUh8q"

(_, _, SMTP) = authentificate(login, password)
content = listFuncs.listToHTML(listFuncs.listFromJSONfile("orderList.json"), "Отчётик")
msg = createMessage(login, login, content)

sendMessage(SMTP, msg)

#authentificate("aboba@gmail.com", "asd")
#authentificate("aboba@mail.ru", "asd")
#authentificate("aboba@yandex.ru", "asd")
#smtpObj.sendmail("vladshilov03@mail.ru", "vladshilov03@mail.ru","looks alive")

