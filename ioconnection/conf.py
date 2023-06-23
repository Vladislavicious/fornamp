"""
Config manager - класс, который отвечает за пользовательскую конфигурацию. По умолчанию, считывает файл из App Dat'ы,
а в этом хранятся все пользовательские настройки - местоположение папок с заказами, шрифты, цветовая гамма
"""
import os
import pickle
from cryptography.fernet import Fernet
from UIadjusters.fontFabric import FontStruct
from UIadjusters.colorFabric import ColorSetting

from ioconnection.Singletone import Singleton


class ConfigManager(metaclass=Singleton):
    @classmethod
    def get_config(cls):
        dir_name = os.getenv('APPDATA') + "\\fornamp"
        in_dir_path = "\\.ordconfig"

        try:
            with open(dir_name + in_dir_path, "rb") as file:
                config_manager = pickle.load(file, encoding="utf-8")
        except FileNotFoundError:
            os.makedirs(dir_name, exist_ok=True)
            config_manager = ConfigManager()
            config_manager.save()

        return config_manager

    def __init__(self) -> None:
        self.__config_dir_path = os.getenv('APPDATA') + "\\fornamp"
        self.working_directory = os.getcwd()

        self.orders_dir_path = self.working_directory + "\\orders"
        self.statistics_dir_path = self.working_directory + "\\statistics"
        self.accounts_filepath = self.__config_dir_path + "\\accs.b"
        self.key = Fernet.generate_key()

        self.font_struct = FontStruct(family="Century gothic", size=16)
        self.color_setting = ColorSetting(undone="#B22222", done="#FFA500", vidan="#7FFF00", border_color=None,
                                          bg="transparent", fg=None, buttons=None,
                                          error_font=None, button_hover=None,
                                          lines=None, base_font=None, lines_width=1)

    def save(self):
        with open(self.__config_dir_path + "\\.ordconfig", "wb") as file:
            pickle.dump(self, file)
