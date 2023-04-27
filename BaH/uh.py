import re

from BaH.user import User


class UserHandler:
    """
    Считывает пользователей из папки, хранит в себе пользователей, может добавлять, убирать.
    В том числе содержит функции для проверки Логина и имейла
    После любого изменения пользователей, требуется вызвать SaveToFile
    """
    def __init__(self, key: bytes, filepath: str = "", users: list = list()) -> None:
        self.users = users
        self.key = key              # filemanager задаёт все поля при начале работы с ним, считывая из config'а
        self.filepath = filepath    # Путь к файлу со всеми пользователями

        self.__ReadFromFile()

    def SaveToFile(self, filepath: str = "Перезапись"):
        path = filepath
        if filepath == "Перезапись":
            path = self.filepath
        if len(self.users) == 0:
            return
        
        with open(path, "wb") as file:
            prelast_index = len(self.users) - 1

            for user in self.users[:prelast_index]:
                file.write(user.serialize(self.key))
                file.write(b'next_one')

            file.write(self.users[prelast_index].serialize(self.key))
    
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

    def ValidateLogin(self, login: str) -> bool:
        if len(self.users) == 0:
            return True

        login_len = len(login)

        if login_len > 32 or login_len < 8:
            return False
        
        for i in login.lower():
            if i not in '1234567890qwertyuiopasdfghjklzxcvbnm':
                return False

        for user in self.users:
            if login == user.login:
                return False
        return True
    
    def ValidateEmail(self, email: str) -> bool:
        """Проверка синтаксическая, без проверки на существование"""
        pattern = r'^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$'
        
        if re.match(pattern, email):
            return True
        return False
    
    def addUser(self, user: User):
        self.users.append(user)

    def deleteUserByLogin(self, login: str) -> bool:
        del_index = -1
        for i in range(0, len(self.users)):
            if login == self.users[i].login:
                del_index = i
                break
        if del_index != -1:
            self.users.pop(del_index)
            return True
        
        return False
        
