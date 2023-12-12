# конвертирует список с p[(5,),(8,),...] к [5,8,...]
from datetime import datetime
import datetime as dt


def _convert(list_convert):

    return [itm[0] for itm in list_convert]

def mounth_to_word(num):
    mon = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]
    return mon[num-1]

def get_data(date):
    return f"Сегодня {date.day} {mounth_to_word(date.month)} {date.year} года"



print(get_data(datetime.now()))
delta = dt.timedelta()
date1 = datetime.fromtimestamp(1673117140)
date2 = datetime.now()
delta = date2 - date1
print(delta.seconds//60//24)
# print(dt.timedelta(datetime.fromtimestamp(1673117140).time()-datetime.now().time()))
print(datetime.now().time())
print(dt.tzinfo())

def strike(text):
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result

