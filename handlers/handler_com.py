# добавляем класс-родитель
from handlers.handler import Handler
from settings.message import MESSAGES

# Наследуемся от него
class HanderCommands(Handler):
    """
    Класс будет обрабатывать входящие команды:
    /start
    /help
    """

    def __init__(self, bot):
        super().__init__(bot)

    # обработка /start
    def pressed_btn_start(self, message):
        self.bot.send_message(message.chat.id,
                              f'Добро пожаловать в "Ремайндер"!',
                              reply_markup=self.keybords.start_menu())
    # обработка /help
    def pressed_btn_help(self, message):
        self.bot.send_message(message.chat.id, MESSAGES['onboard'], parse_mode="HTML",
                              reply_markup=self.keybords.start_menu())

    def handle(self):
        #Обработчик сообщений, который обрабатывает входящие /start и /help сообщения
        @self.bot.message_handler(commands = ['start', 'help'])
        def handle(message):
            print(message)
            if message.text == '/start':
                self.pressed_btn_start(message)
            if message.text == '/help':
                self.pressed_btn_help(message)







