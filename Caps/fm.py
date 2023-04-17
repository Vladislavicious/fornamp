import os
from cryptography.fernet import Fernet

from BaH.order import Order
from BaH.uh import UserHandler


class FileManager():
    """Класс для работы с файлами приложения"""
    def __init__(self) -> None:
        self.__config_dir_path = os.getenv('APPDATA') + "\\factory-engine"
        self.working_directory = os.getcwd()
        self.__readConfig()
        self.__parseOrderFilenames()

        self.user_handler = UserHandler(self.key, self.accounts_filepath)

    def __readConfig(self):
        dir_name = self.__config_dir_path
        in_dir_path = "\\.ordconfig"
        try:
            config_file = open(dir_name + in_dir_path, "r", encoding="utf-8")
        except FileNotFoundError:
            os.makedirs(dir_name, exist_ok = True)
            self.orders_dir_path = self.working_directory + "\\orders"
            self.statistics_dir_path = self.working_directory + "\\statistics"
            self.accounts_filepath = self.__config_dir_path + "\\accs.b"
            self.key = Fernet.generate_key()
            self.saveNewConfig()

            return
        
        lines = [line.rstrip() for line in config_file]
        
        self.__parsePath(lines)

        config_file.close()
    
    def __parsePath(self, config_lines: list):
        self.orders_dir_path = (config_lines[0].split(": "))[1].strip()
        self.statistics_dir_path = (config_lines[1].split(": "))[1].strip()
        self.accounts_filepath = (config_lines[2].split(": "))[1].strip()
        self.key = bytes((config_lines[3].split(": "))[1].strip(), encoding="utf-8")

    
    def saveNewConfig(self):
        file = open(self.__config_dir_path + "\\.ordconfig", "w", encoding="utf-8")
        file.write("Orders Directory Path: " + self.orders_dir_path + "\n")  
        file.write("Statistics Directory Path: " + self.statistics_dir_path + "\n")
        file.write("Accounts Filepath: " + self.accounts_filepath + "\n")
        file.write("Key: " + self.key.decode("utf-8") + "\n")     
        file.close() 

    def __parseOrderFilenames(self):
        order_filenames = os.listdir(self.orders_dir_path)
        self.ordered_filenames = self.__getOrderStatusPairs(order_filenames)

    def __getOrderStatusPairs(self, order_filenames):
        """Возвращает словарь Айди заказа: статус"""
        orders = dict()
        for ord_file in order_filenames:
            status = ord_file[0]
            id = ord_file[1:12]
            orders[id] = status
        return orders
    
    def getOrderByID(self, ID: int):
        """Возвращает Order либо None"""
        filename = self.__getOrderFilename(ID)
        if filename == "":
            return None
        
        return Order.fromFile(filename)
    
    def deleteOrderByID(self, ID: int) -> bool:
        """Удаляет как файл, так и элемент словаря"""
        filename = self.__getOrderFilename(ID)
        if filename == "":
            return False
        
        os.remove(filename)
        del self.ordered_filenames[str(ID)]
        return True
        

        
    def __getOrderFilename(self, ID: int):
        """Возвращает имя файла, либо '' """
        id_str = str(ID)
        try:
            filename = self.orders_dir_path + "\\" + self.ordered_filenames[id_str] + id_str + ".order"
        except KeyError:
            filename = ""
        
        return filename
        
