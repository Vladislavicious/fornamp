import pickle
from cryptography.fernet import InvalidToken
from cryptography.fernet import Fernet


class User:
    def __init__(self, email: str, login: str, password: str,
                 emailpassword: str, isLastUser=False, isAdministrator=False):
        self.email = email
        self.login = login
        self.password = password
        self.emailpassword = emailpassword

        self.isAdministrator = isAdministrator
        self.isLastUser = isLastUser

    def __str__(self) -> str:
        return f"email: {self.email}\
                 \nlogin: {self.login}\
                 \npassword: {self.password}\
                 \nemail password: {self.emailpassword}\
                 \nit's last user: {self.isLastUser}\
                 \nit's Administrator: {self.isAdministrator}\n"

    def serialize(self, key):
        f = Fernet(key)
        serialized_data = pickle.dumps(self.__dict__)
        encrypted_data = f.encrypt(serialized_data)
        return encrypted_data

    @classmethod
    def deserialize(cls, data, key):
        f = Fernet(key)
        try:
            decrypted_data = f.decrypt(data)
            deserialized_data = pickle.loads(decrypted_data)
            return cls(**deserialized_data)
        except InvalidToken:
            return None
