import re
from typing import List, Tuple
from typing import Dict

from BaH.user import User


class UserHandler:
    """
    Считывает пользователей из папки, хранит в себе пользователей, может добавлять, убирать.
    В том числе содержит функции для проверки Логина и имейла
    После любого изменения пользователей, сам вызывает SaveToFile
    """
    def __init__(self, key: bytes, filepath: str = "", users: list = list()) -> None:
        self.users = users
        self.key = key              # filemanager задаёт все поля при начале работы с ним, считывая из config'а
        self.filepath = filepath    # Путь к файлу со всеми пользователями
        self.lastUser = None

        self.__ReadFromFile()
        self.__seekLastUser()   # Если список юзеров пуст, то переменная self.lastUser равна None

    def SaveToFile(self, filepath: str = "Перезапись"):
        """без проверки на существование файла"""
        path = filepath
        if filepath == "Перезапись":
            path = self.filepath
        else:
            self.filepath = filepath

        if len(self.users) == 0:
            return

        with open(path, "wb") as file:
            prelast_index = len(self.users) - 1

            for user in self.users[:prelast_index]:
                file.write(user.serialize(self.key))
                file.write(b'next_one')

            file.write(self.users[prelast_index].serialize(self.key))

    def getUsersLogins(self) -> List[str]:
        names = list()
        for user in self.users:
            names.append(user)
        return names

    def __ReadFromFile(self):

        try:
            with open(self.filepath, "rb") as file:
                text = file.read()
                text = text.split(b'next_one')

                Users = list()

                for code in text:
                    Users.append(User.deserialize(code, self.key))

            self.users = Users
        except FileNotFoundError:
            print("Файл с аккаунтами ещё не создан")

    def __seekLastUser(self):
        lastUser = None

        for user in self.users:
            if user.isLastUser is True:
                lastUser = user
                break

        self.lastUser = lastUser

    def Authorize(self, login: str, password: str) -> bool:
        """Если пользователь авторизован, возвращает True и ставит его lastUser'ом"""
        if not self.__lexicLoginValidation(login):
            return False   # Нет смысла проходить по всем юзерам, если логин не может существовать в первую очередь

        for user in self.users:
            if login == user.login:
                if password == user.password:

                    self.lastUser = user
                    return True

        return False

    def markAsLastUser(self, login: str) -> bool:
        """Возвращает True, если пользователь найден и отмечен последним"""
        self.setNoLastUsers()

        for user in self.users:
            if login == user.login:
                user.isLastUser = True
                self.lastUser = user

                self.SaveToFile()
                return True

        return False

    def setNoLastUsers(self):
        """Сохраняет, только если что-то изменилось"""
        isChanged = False
        for user in self.users:
            if user.isLastUser is True:
                user.isLastUser = False
                isChanged = True

        self.lastUser = None
        if isChanged:
            self.SaveToFile()

    def getAdministratorsNames(self):
        names = list()
        for user in self.users:
            if user.isAdministrator:
                names.append(user.login)

        return names

    def __lexicLoginValidation(self, login: str) -> bool:
        """Проверяет символы в логине"""
        login_len = len(login)

        if login_len > 32 or login_len < 4:
            return False

        for i in login.lower():
            if i not in '1234567890qwertyuiopasdfghjklzxcvbnm':
                return False

        return True

    def __ValidateLogin(self, login: str) -> Tuple[bool, str]:
        """Проверяет можно ли создать аккаунт с таким логином"""
        if not self.__lexicLoginValidation(login):
            return False, "Логин должен состоять из цифр и/или букв латинского "\
                           + "алфавита и быть длиной не меньше 4 и не больше 32 символов"
        if len(self.users) == 0:
            return True, ""

        for user in self.users:
            if login == user.login:
                return False, "Логин уже существует"
        return True, ""

    def __ValidateEmail(self, email: str) -> Tuple[bool, str]:
        """Проверка синтаксическая, без проверки на существование такого адреса"""
        pattern = r'^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$'

        if re.match(pattern, email):
            return True, ""
        return False, "Невозможный email"

    def __ValidatePassword(self, password: str) -> Tuple[bool, str]:
        password_len = len(password)

        if password_len > 32:
            return False, "Длина пароля больше 32 символов"
        if password_len < 8:
            return False, "Длина пароля меньше 8 символов"

        for i in password.lower():
            if i not in '1234567890qwertyuiopasdfghjklzxcvbnm!@#%&*?%№':
                return False, "Пароль содержит недопустимые символы"

        return True, ""

    def addEmailInfo(self, user: User, email: str, emailpassword: str) -> List[Dict[int, str]]:
        """Интерфейс для добавления почты для существующего пользователя
           Возвращает список словрей {int: str}, где int - аргумент, в котором была найдена ошибка
           0 - ошибок нет, 1 - email, 2 - Пароль
           str - описание ошибки"""

        isEmailValidated, EmailErrorString = self.__ValidateEmail(email)
        isEmailPasswordValidated, EmailPasswordErrorString = self.__ValidatePassword(emailpassword)

        errors = list()
        didErrorOccur = False

        if not isEmailValidated:
            errors.append({1: EmailErrorString})
            didErrorOccur = True

        if not isEmailPasswordValidated:
            errors.append({2: EmailPasswordErrorString})
            didErrorOccur = True

        if not didErrorOccur:
            errors.append({0: "Ошибок не выявлено"})
            user.email = email
            user.emailpassword = emailpassword
            self.SaveToFile()

        return errors

    def NewUser(self, login: str, password: str, email: str = "",
                emailpassword: str = "", isLastUser=False,
                isAdministrator=False) -> List[Dict[int, str]]:
        """Интерфейс для регистрации нового пользователя
           Возвращает список словрей {int: str}, где int - аргумент, в котором была найдена ошибка
           0 - ошибок нет, 1 - Логин, 2 - Пароль, и т.д.
           str - описание ошибки"""
        isLoginValidated, LoginErrorString = self.__ValidateLogin(login)
        isPasswordValidated, PasswordErrorString = self.__ValidatePassword(password)

        if email == "":
            isEmailValidated, EmailErrorString = True, ""
        else:
            isEmailValidated, EmailErrorString = self.__ValidateEmail(email)

        if emailpassword == "":
            isEmailPasswordValidated, EmailPasswordErrorString = True, ""
        else:
            isEmailPasswordValidated, EmailPasswordErrorString = self.__ValidatePassword(emailpassword)

        errors = list()
        didErrorOccur = False

        if not isLoginValidated:
            errors.append({1: LoginErrorString})
            didErrorOccur = True

        if not isPasswordValidated:
            errors.append({2: PasswordErrorString})
            didErrorOccur = True

        if not isEmailValidated:
            errors.append({3: EmailErrorString})
            if emailpassword == "":
                errors.append({4: "Не заполнен пароль почты"})
            didErrorOccur = True

        if not isEmailPasswordValidated:
            errors.append({4: EmailPasswordErrorString})
            if email == "":
                errors.append({3: "Не заполнен логин почты"})
            didErrorOccur = True

        if not didErrorOccur:
            errors.append({0: "Ошибок не выявлено"})
            newUser = User(email=email, login=login, password=password,
                           emailpassword=emailpassword, isLastUser=isLastUser,
                           isAdministrator=isAdministrator)
            self.__addUser(newUser)

        return errors

    def __addUser(self, user: User):
        """Подразумевается, что прежде чем юзера добавлять, были проверены логин и пароль"""
        self.users.append(user)
        self.SaveToFile()

    def deleteUserByLogin(self, login: str) -> bool:
        del_index = -1
        for i in range(0, len(self.users)):
            if login == self.users[i].login:
                del_index = i
                break
        if del_index != -1:
            self.users.pop(del_index)
            self.SaveToFile()
            return True

        return False
