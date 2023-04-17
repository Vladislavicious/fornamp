from BaH.user import User
class UserHandler:
    users = list()
    key = None

    @classmethod
    def SaveToFile(cls, filepath):
        
        with open(filepath, "wb") as file:
            prelast_index = len(cls.users) - 1

            for user in cls.users[:prelast_index]:
                file.write(user.serialize(cls.key))
                file.write(b'next_one')

            file.write(cls.users[prelast_index].serialize(cls.key))
    
    @classmethod
    def ReadFromFile(cls, filepath):
        
        with open(filepath, "rb") as file:
            text = file.read()
            print(len(text))
            text = text.split(b'next_one')

            Users = list()

            for code in text:
                Users.append(User.deserialize(code, cls.key))
        
        return Users
