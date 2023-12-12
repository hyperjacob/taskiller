import os
# импортируем модуль emoji для отображения эмоджи
from emoji import emojize
from settings import word_gen

# токен выдается при регистрации приложения
TOKEN = ''
# название БД
NAME_DB = 'rmdb.db'
# версия приложения
VERSION = '1.0.2'
# автор приложния
AUTHOR = 'Jacob'


foldername = {}
eventname = {}
inbox = {}
taskname = {}
taskrename = {}
eventdate = {}
addfolderteg = {}
share = {}
welcomemsg = {}
is_url = {}

# родительская директория
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# путь до базы данных
DATABASE = os.path.join('sqlite:///'+BASE_DIR, NAME_DB)




def newword(LANG, DIFF):
    if LANG == "RU":
        neww = word_gen.dictionary(BASE_DIR+"/dictru.txt", DIFF)
    elif LANG == "EN":
        neww = word_gen.dictionary(BASE_DIR+"/dict.txt", DIFF)
    return neww
# neww = ""


# кнопки управления
KEYBOARD = {
    'EVENT': emojize('🗓 Добавить событие'),
    'INFO': emojize(':information: Справка'),
    'SETTINGS': emojize('⚙️ Настройки'),
    'INBOX': emojize('📥 Входящие'),
    'FOLDERS': emojize('🗂 Папки'),
    'LANGRU': emojize('💬 Выбран язык: :Russia:'),
    'CHANGE_NAME': emojize('👤 Изменить имя'),
    'RELOAD': emojize('🔄 Загадать другое слово'),
    'TIPS': emojize(':white_flag: Подсказка'),
    'END_GAME': emojize('❌ Закончить игру'),
    'SCORE': emojize('🏅 Общий зачет'),
    'ABSSCRE': emojize('👑 Абсолютный зачет'),
    'GAMES': emojize('🕹 Количество игр'),
    'YOURSTATS': emojize('📊 Твоя статистика'),
    'RANK': emojize('🏆 Зал славы'),
    'HARD': emojize(f'📈 Сложность 1 из 3'),
    '<<': emojize('⏪ Назад'),
    'ORDER': emojize('✅ ЗАКАЗ'),
    'X': emojize('❌ Отмена'),
    'COPY': '©️'
}

FICON = [
    "✅️", "❗️","❓", "💊", "️⚒", "✈️", "🎁", "🎬", "🛒","🚙", "♻️️", "❤️"
]

TICON = [
    "🙂", "☠️️","🦄", "📌", "️⚡️", "📱️️", "📚", "💐", "🎉","⭐️", "🔅️️", "⚜️️"
]

EICON = [
    "✈️", "🎮","🎭", "🩺", "️🍻", "🎉️", "⚒", "🚙", "🛒","🍖", "⛹️️", "❤️"
]
access_level = [
    "Только чтение", "Чтение и отметка о выполнении", "Чтение и запись новых задач", "Чтение, отметка о выполнении и запись новых задач", "Все права доступа"
]

# названия команд
COMMANDS = {
    'START': "start",
    'HELP': "help",
}
