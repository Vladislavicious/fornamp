"""
Config manager - класс, который отвечает за пользовательскую конфигурацию. По умолчанию, считывает файл из App Dat'ы,
а в этом хранятся все пользовательские настройки - местоположение папок с заказами, шрифты, цветовая гамма
"""
import os
import pickle
from cryptography.fernet import Fernet


class ConfigManager():
    @classmethod
    def standard_cm(cls):
        dir_name = os.getenv('APPDATA') + "\\fornamp"
        in_dir_path = "\\.ordconfig"

        try:
            with open(dir_name + in_dir_path, "rb") as file:
                cm = pickle.load(file, encoding="utf-8")
        except FileNotFoundError:
            os.makedirs(dir_name, exist_ok=True)
            cm = ConfigManager()
            cm.save()

        return cm

    def __init__(self) -> None:
        self.__config_dir_path = os.getenv('APPDATA') + "\\fornamp"
        self.working_directory = os.getcwd()

        self.orders_dir_path = self.working_directory + "\\orders"
        self.statistics_dir_path = self.working_directory + "\\statistics"
        self.accounts_filepath = self.__config_dir_path + "\\accs.b"
        self.key = Fernet.generate_key()

        self.font_family = "Century gothic"

    def save(self):
        with open(self.__config_dir_path + "\\.ordconfig", "wb") as file:
            pickle.dump(self, file)
