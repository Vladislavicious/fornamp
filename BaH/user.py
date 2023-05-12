import pickle
from cryptography.fernet import Fernet


class User:
    def __init__(self, email, login, password, emailpassword, isLastUser=False):
        self.email = email
        self.login = login
        self.password = password
        self.emailpassword = emailpassword

        self.isLastUser = isLastUser
    
    def __str__(self) -> str:
        return f"email: {self.email}\
                 \nlogin: {self.login}\
                 \npassword: {self.password}\
                 \nemail password: {self.emailpassword}\
                 \nit's last user: {self.isLastUser}\n"

    def serialize(self, key):
        f = Fernet(key)
        serialized_data = pickle.dumps(self.__dict__)
        encrypted_data = f.encrypt(serialized_data)
        return encrypted_data

    @classmethod
    def deserialize(cls, data, key):
        f = Fernet(key)
        decrypted_data = f.decrypt(data)
        deserialized_data = pickle.loads(decrypted_data)
        return cls(**deserialized_data)
