# импортируем функцию создания объекта бота
from telebot import TeleBot
# импортируем основные настройки проекта
from settings import config
# импортируем главный класс-обработчик бота
from handlers.handler_main import HandlerMain
import logging

logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


class TelBot:
    """
    Основной класс телеграмм бота (сервер), в основе которого
    используется библиотека pyTelegramBotAPI
    """
    __version__ = config.VERSION
    __author__ = config.AUTHOR

    def __init__(self):
        """
        Инициализация бота
        """
        # получаем токен
        self.token = config.TOKEN
        # инициализируем бот на основе зарегистрированного токена
        self.bot = TeleBot(self.token)
        # инициализируем оброботчик событий
        self.handler = HandlerMain(self.bot)

    def start(self):
        """
        Метод предназначен для старта обработчика событий
        """
        self.handler.handle()

    def run_bot(self):
        """
        Метод запускает основные события сервера
        """

        # обработчик событий
        self.start()
        # Enable logging

        # служит для запуска бота (работа в режиме нон-стоп)
        self.bot.polling(none_stop=True)
        # try:
        #     self.bot.polling(none_stop=True)
        # except:
        #     pass
        # while True:
        #     try:
        #         self.bot.polling(none_stop=True)
        #     except Exception as e:
        #         print(e)
        #         traceback.print_exc()
        #         time.sleep(15)


if __name__ == '__main__':
    bot = TelBot()
    bot.run_bot()
