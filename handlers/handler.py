# импортируем библиотеку abc для реализации абстрактных классов
import abc
# импортируем разметку клавиатуры и клавиш
from markup.markup import Keyboards
# импортируем класс-менеджер для работы с библиотекой
from data_base.dbalchemy import DBManager
# импортируем логгер
from settings.logger import Logger


class Handler(metaclass=abc.ABCMeta):

    def __init__(self, bot):
        # получаем объект бота
        self.bot = bot
        # инициализируем разметку кнопок
        self.keybords = Keyboards()
        # инициализируем менеджер для работы с БД
        self.BD = DBManager()
         # инициализируем логгер
        self.Log = Logger()

    @abc.abstractmethod
    def handle(self):
        pass
