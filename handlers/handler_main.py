# импортируем класс HandlerCommands обработка команд
from handlers.handler_com import HanderCommands
# импортируем класс HandlerAllText обработка нажатия на кнопки и иные сообщения
from handlers.handler_all_txt import HendlerAllText
# импортируем класс HandlerInlineQuery обработка нажатия на кнопки инлайн
from handlers.handler_inline_query import HandlerInlineQuery


class HandlerMain:
    """
    Класс компоновщик
    """
    def __init__(self, bot):
        # получаем нашего бота
        self.bot = bot
        # здесь будет иницаилизация обработчиков
        self.handler_commands = HanderCommands(self.bot)
        self.handler_all_text = HendlerAllText(self.bot)
        self.handler_inline_query = HandlerInlineQuery(self.bot)


    def handle(self):
        # здесь будет запуск обработчиков
        self.handler_commands.handle()
        self.handler_all_text.handle()
        self.handler_inline_query.handle()
