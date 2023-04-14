import os

class FileManager():
    """Класс для работы с файлами приложения"""
    def __init__(self) -> None:
        self.__config_dir_path = os.getenv('APPDATA') + "\\factory-engine"
        self.working_directory = os.getcwd()
        self.readConfig()

    def readConfig(self):
        dir_name = self.__config_dir_path
        in_dir_path = "\\.ordconfig"
        try:
            config_file = open(dir_name + in_dir_path, "r", encoding="utf-8")
        except FileNotFoundError:
            os.makedirs(dir_name, exist_ok = True)
            self.orders_dir_path = self.working_directory + "\\orders"
            self.statistics_dir_path = self.working_directory + "\\statistics"
            self.accounts_filepath = self.__config_dir_path
            self.saveNewConfig()

            return
        
        lines = [line.rstrip() for line in config_file]
        
        self.__parsePath(lines)

        config_file.close()
    
    def __parsePath(self, config_lines: list):
        self.orders_dir_path = (config_lines[0].split(": "))[1].strip()
        self.statistics_dir_path = (config_lines[1].split(": "))[1].strip()
        self.accounts_filepath = (config_lines[2].split(": "))[1].strip()

    
    def saveNewConfig(self):
        file = open(self.__config_dir_path + "\\.ordconfig", "w", encoding="utf-8")
        file.write("Orders Directory Path: " + self.orders_dir_path + "\n")  
        file.write("Statistics Directory Path: " + self.statistics_dir_path + "\n")
        file.write("Accounts Filepath: " + self.accounts_filepath + "\n")        
        file.close() 