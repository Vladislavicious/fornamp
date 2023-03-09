import smtplib
from typing import Tuple


def bla():
    smtpObj = smtplib.SMTP('smtp.mail.ru', 587)

    print(smtpObj.starttls())
    
  
def authentificate(login: str, password: str) -> None:#Tuple[bool, str]:
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
        smtpObj.login('vladshiov03@mail.ru','NAV60PWGuRpWkux79fjY')
        return (True, "Успешно")
    except smtplib.SMTPResponseException as e:
        error_code = e.smtp_code
        error_message = e.smtp_error
        if(error_code==535):
            error_message = "Для входа необходим пароль приложения"
        elif(error_code==553):
            error_message = "Проверь все адреса в Кому, CC и BCC полях. Где-то должна быть ошибка или неправильное написание"
        
        return (False, f"{error_code}: " + error_message)
        


print(authentificate("aboba@inbox.ru", "asd"))
#authentificate("aboba@gmail.com", "asd")
#authentificate("aboba@mail.ru", "asd")
#authentificate("aboba@yandex.ru", "asd")
#smtpObj.sendmail("vladshilov03@mail.ru", "vladshilov03@mail.ru","looks alive")

