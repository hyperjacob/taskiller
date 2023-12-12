from settings.message import MESSAGES
from handlers.handler import Handler
from settings import config

from emoji import emojize
from random import randint
from datetime import datetime
from datetime import timedelta

class HendlerAllText(Handler):
    # класс обрабатывает входящие текстовые сообщения от нажатия на кнопку



    def __int__(self, bot):
        super().__init__(bot)



    def first_location(self, message):
        timezone = datetime.fromtimestamp(message.date) - datetime.now()
        self.BD.add_utc(message.from_user.id, timezone)


    def add_new_event(self, message):
        first = message.text.split(" ")
        if "/" in first[0]:
            date = first[0].split("/")
        elif ":" in first[0]:
            date = first[0].split(":")






    def get_inbox(self, message):
        url = False
        if message.text[:3] == "http":
            url = "message.text"
        try:
            msg, teg = message.text.split("#")
        except:
            msg = message.text
            teg = False
        idfolder = False
        if teg:
            idfolder = self.BD.find_teg(teg, message.from_user.id)
        if idfolder:
            try:
                self.BD.add_task(msg, idfolder, message.from_user.id)
                userid = self.BD.select_user_id(message.from_user.id)
                folder = self.BD.find_folder(idfolder, userid)
                print("teg", idfolder)
                self.bot.send_message(message.chat.id, emojize(f'📥 Добавлено в папку <code> {folder[0]} {folder[1]}</code>'),  parse_mode="HTML")
            except:
                self.bot.send_message(message.chat.id, emojize(f'⚠️ Произошла ошибка при попыке добавления'),
                                            parse_mode="HTML")
        else:
            if url:
                try:
                    inboxid = self.BD.add_url_inbox(msg, message.from_user.id)
                    config.is_url[message.from_user.id] = inboxid
                    config.inbox[message.from_user.id] = False
                    self.bot.send_message(message.chat.id, emojize(f'Ссылка успешно добавлена, введите название'),
                                        parse_mode="HTML",
                                        reply_markup=self.keybords.back_menu())
                except:
                    self.bot.send_message(message.chat.id, emojize(f'⚠️ Произошла ошибка при попыке добавления ссылки'),
                                        parse_mode="HTML",
                                        reply_markup=self.keybords.back_menu())
            else:
                try:
                    self.BD.add_inbox(msg, message.from_user.id)
                    print("ok")
                    if teg and not idfolder:
                        self.bot.send_message(message.chat.id, emojize(f'📥 Добавлено в папку "Входящие", указанный вами тег не обнаружен'),
                                                parse_mode="HTML")
                    else:
                        self.bot.send_message(message.chat.id, emojize(f'📥 Добавлено в папку "Входящие"'))
                except:
                    self.bot.send_message(message.chat.id, emojize(f'⚠️ Произошла ошибка при попыке добавления'),
                                            parse_mode="HTML",
                                            reply_markup=self.keybords.back_menu())

    def rename_inbox(self, message, inboxid):
        config.is_url[message.from_user.id] = False
        config.inbox[message.from_user.id] = True
        status = self.BD.inbox_rename(message.from_user.id, message.text, inboxid)
        if status:
            self.bot.send_message(message.chat.id, emojize(f'📥 Добавлено в папку "Входящие"'),
                                                parse_mode="HTML")
        else:
            self.bot.send_message(message.chat.id, emojize(f'⚠️  Не удалось добавить имя'),
                                                parse_mode="HTML")


    def send_inbox_list(self, teleid):
        # self.bot.send_message(message.chat.id,MESSAGES['order_number'].format(
        #     self.step+1), parse_mode="HTML")
        inbox_list = self.BD.select_all_inbox_by_user(teleid)
        text = "Нажмите на задачу для отметки о ее выполнении"
        if not inbox_list:
            text = "Папка пуста"
        self.bot.send_message(teleid,
                              f"<code>📥 Входящие</code>\n\n\n{text}",
                              parse_mode="HTML",
                              reply_markup= self.keybords.set_inline_inbox(teleid))
    #События
    def send_events_list(self, message):
        event_list = self.BD.show_event_list(message.from_user.id)
        text = "Список ваших событий"
        if not event_list:
            text = "Папка пуста"
        self.bot.send_message(message.from_user.id,
                              f"<code>🗓 События</code>\n\n\n{text}",
                              parse_mode="HTML",
                              reply_markup= self.keybords.set_inline_events(message.from_user.id))


    def get_event_day(self, message, inbox_id):
        date_time_obj = ""

        if ":" in message.text:
            try:
                date_time_obj = datetime.strptime(message.text, '%d:%m:%Y')
            except:
                self.bot.send_message(message.chat.id, emojize(f'⚠️ Не верный формат даты, введите дату в следующем формате: DD:MM:YYYY, например: 11:06:2025. Повторите попытку'),
                                parse_mode="HTML",
                                reply_markup=self.keybords.back_menu())
        elif "/" in message.text:
            try:
                date_time_obj = datetime.strptime(message.text, '%d/%m/%Y')
            except:
                self.bot.send_message(message.chat.id, emojize(f'⚠️ Не верный формат даты, введите дату в следующем формате: DD/MM/YYYY, например: 11/06/2025. Повторите попытку'),
                                parse_mode="HTML",
                                reply_markup=self.keybords.back_menu())
        elif "-" in message.text:
            try:
                date_time_obj = datetime.strptime(message.text, '%d-%m-%Y')
            except:
                self.bot.send_message(message.chat.id, emojize(f'⚠️ Не верный формат даты, введите дату в следующем формате: DD-MM-YYYY, например: 11-06-2025. Повторите попытку'),
                                parse_mode="HTML",
                                reply_markup=self.keybords.back_menu())
        elif "." in message.text:
            try:
                date_time_obj = datetime.strptime(message.text, '%d.%m.%Y')
            except:
                self.bot.send_message(message.chat.id, emojize(f'⚠️ Не верный формат даты, введите дату в следующем формате: DD.MM.YYYY, например: 11.06.2025. Повторите попытку'),
                                parse_mode="HTML",
                                reply_markup=self.keybords.back_menu())
        else:
            self.bot.send_message(message.chat.id, emojize(f'⚠️ Не верный формат даты, введите дату в следующем формате: DD.MM.YYYY, например: 11.06.2025. Повторите попытку'),
                                parse_mode="HTML",
                                reply_markup=self.keybords.back_menu())
        if date_time_obj and date_time_obj > datetime.now():
            try:
                print(date_time_obj)
                config.inbox[message.from_user.id] = True
                config.eventdate[message.from_user.id] = False
                name = self.BD.get_inbox_name(inbox_id)
                print(name)
                self.BD.del_inbox_task(message.from_user.id, inbox_id)
                prt = self.BD.add_new_event(name, date_time_obj, message.from_user.id)
                print(prt)
                self.bot.send_message(message.from_user.id,
                              "✅ Сообщение успешно преобразовано в событие",
                              parse_mode="HTML",
                              reply_markup= self.keybords.remove_menu())
                self.bot.send_message(message.from_user.id,
                                      f'<b>Событие ХХХХХ</b>\n\n\nВыбирите действие:',
                                      parse_mode="HTML",
                                      reply_markup=self.keybords.event_edit(prt, "inbox"))
                                      # reply_markup=self.keybords.set_inline_inbox_event(message.from_user.id))
            except:
                self.bot.send_message(message.chat.id, emojize(f'⚠️ Произошла ошибка, попробуйте позднее'),
                                parse_mode="HTML",
                                reply_markup=self.keybords.back_menu())
        elif date_time_obj:
            self.bot.send_message(message.from_user.id, emojize(f'⚠️ Дата должна быть больше сегодняшнего числа, повторите попытку'),
                                parse_mode="HTML",
                                reply_markup=self.keybords.back_menu())

    def get_eventname(self,message, eventid):
        try:
            oldname = self.BD.event_rename(eventid, message.text)
            config.eventname[message.from_user.id] = False
            config.inbox[message.from_user.id] = True
            self.bot.send_message(message.from_user.id,
                              f'✅ Событие "{oldname}" успешно переименовано в "{message.text}"',
                              parse_mode="HTML",
                              reply_markup= self.keybords.remove_menu())
            self.bot.send_message(message.from_user.id,
                                  f'<code>Событие {message.text}</code>',
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.event_edit(eventid, "eventlist"))
        except:
            self.bot.send_message(message.chat.id, emojize(f'⚠️ Произошла ошибка при попыке переименования события'),
                                parse_mode="HTML",
                                reply_markup=self.keybords.back_menu())


    def send_folders_list(self, message):
        '''
        Вывод папок пользователя
        '''
        text = ""
        if message.text == config.KEYBOARD["FOLDERS"]:
            text = "👋 Добро пожаловать в меню Ваших папок!\n\n<i>Здесь можно создавать, группировать и делиться своими списками задач и важных дел</i>"
        elif message.text == config.KEYBOARD['X']:
            text =  "❌ Вы отменили действие"
        self.bot.send_message(message.from_user.id,
                              text,
                              parse_mode="HTML",
                              reply_markup= self.keybords.remove_menu())
        print(message.message_id)
        config.welcomemsg[message.from_user.id] = message.message_id+1
        self.bot.send_message(message.from_user.id,
                              f"📚 Список ваших папок:",
                              parse_mode="HTML",
                              reply_markup= self.keybords.set_inline_folders(message.from_user.id))
        print(message.message_id)

    def get_foldername(self, message):
        if config.foldername[message.from_user.id] == "New":
            print(message.text, "New")
            try:
                idfolder = self.BD.add_foldername(message.text, message.from_user.id)
                print(idfolder, "ok")
                config.foldername[message.from_user.id] = False
                config.inbox[message.from_user.id] = True
                self.bot.send_message(message.from_user.id,
                              "✅ Папка успешно создана",
                              parse_mode="HTML",
                              reply_markup= self.keybords.remove_menu())
                self.bot.send_message(message.from_user.id,
                                  f'Выберите значок из предложенных emoji:',
                                  parse_mode="HTML",
                                  reply_markup= self.keybords.set_inline_emoji(str(idfolder), "folder"))

            except:
                self.bot.send_message(message.chat.id, emojize(f'⚠️ Произошла ошибка при попыке создания папки'),
                                    parse_mode="HTML",
                                    reply_markup=self.keybords.back_menu())
        else:
            try:
                print(config.foldername[message.from_user.id], config.inbox[message.from_user.id], config.inbox[message.from_user.id])
                set_new_name = self.BD.rename_folder(message.text, config.foldername[message.from_user.id], message.from_user.id)
                config.foldername[message.from_user.id] = False
                config.inbox[message.from_user.id] = True
                if set_new_name:
                    self.bot.send_message(message.from_user.id,
                              "✅ Папка успешно переименована",
                              parse_mode="HTML",
                              reply_markup= self.keybords.remove_menu())
                    self.bot.send_message(message.from_user.id,
                                  f'<code>Список папок</code>',
                                  parse_mode="HTML",
                                  reply_markup= self.keybords.set_inline_folders(message.from_user.id))
                else:
                    self.bot.send_message(message.chat.id, emojize(f'<code>Список папок</code>\n\n\n⚠️ Произошла ошибка при попыке создания папки'),
                                    parse_mode="HTML",
                                    reply_markup=self.keybords.set_inline_folders(message.from_user.id))
            except:
                self.bot.send_message(message.chat.id, emojize(f'<code>Список папок</code>\n\n\n⚠️ Произошла ошибка при попыке создания папки'),
                                    parse_mode="HTML",
                                    reply_markup=self.keybords.set_inline_folders(message.from_user.id))

    def get_folderteg(self, message, idfolder):
        config.addfolderteg[message.from_user.id] = False
        config.inbox[message.from_user.id] = True
        status = self.BD.add_teg(idfolder, message.text)
        print(status)
        if status:
            userid = self.BD.select_user_id(message.from_user.id)
            folder = self.BD.find_folder(idfolder, userid)
            self.bot.send_message(message.from_user.id,
                              "✅ Тег успешно добавлен",
                              parse_mode="HTML",
                              reply_markup= self.keybords.remove_menu())
            self.bot.send_message(message.from_user.id,
                              emojize(f"<code>Папка {folder[0]} {folder[1]}</code>\n\n:keycap_#:Тег папки: <code>{message.text}</code>\n\nВыбирите действие:"),
                              parse_mode="HTML",
                              reply_markup= self.keybords.edit_folder_settings(idfolder))
        else:
            self.bot.send_message(message.chat.id, emojize(f'<code>Редактирование папки</code>\n\n\n⚠️ Произошла ошибка при добавить тег папке'),
                                    parse_mode="HTML",
                                    reply_markup=self.keybords.set_inline_folders(message.from_user.id))

    def get_folder_share(self, message, idfolder):
        config.share[message.from_user.id] = False
        config.inbox[message.from_user.id] = True
        if self.BD.find_user(message.text):
            status = self.BD.share_folder(idfolder, message.text)
            if status:
                userid = self.BD.select_user_id(message.from_user.id)
                folder = self.BD.find_folder(idfolder, userid)
                self.bot.send_message(message.text,
                              f"✅  Вам был предоставлен доступ к папке {folder[0]} {folder[1]} пользователя {message.from_user.id}",
                              parse_mode="HTML",
                              reply_markup= self.keybords.remove_menu())
                self.bot.send_message(message.from_user.id,
                              f"✅ Пользователю {folder[3]} успешно предоставлен доступ к данной папке (только на чтение)",
                              parse_mode="HTML",
                              reply_markup= self.keybords.remove_menu())
                self.bot.send_message(message.from_user.id,
                              emojize(f"<code>Папка {folder[0]} {folder[1]}</code>\n\nТег папки: <code>{folder[2]}</code>\n\nПри необходимости измените уровень доступа:"),
                              parse_mode="HTML",
                              reply_markup= self.keybords.set_access_lvl(idfolder))
            else:
                self.bot.send_message(message.chat.id, emojize(f'<code>Общий доступ к папке</code>\n\n\n⚠️ Произошла ошибка БД'),
                                    parse_mode="HTML",
                                   reply_markup=self.keybords.back_menu())
        else:
            self.bot.send_message(message.chat.id, emojize(f'<code>Общий доступ к папке</code>\n\n\n⚠️ Произошла ошибка: пользователь с таким идентификатором не найден'),
                                    parse_mode="HTML",
                                   reply_markup=self.keybords.back_menu())


    def get_taskname(self, message, fid):
        try:
            if not self.BD.is_folder_owner(fid, message.from_user.id):
                teleid = self.BD.find_teleid(self.BD.folder_owner(int(fid)))
            else:
                teleid = message.from_user.id
            taskid = self.BD.add_task(message.text, fid, teleid)
            task = self.BD.task_name(taskid)
            # self.bot.delete_message(message.from_user.id, message.message.message_id)
            self.bot.send_message(message.from_user.id,
                                  emojize(f'<code>Задача {task[0]} {task[1]}</code>\n\n✅ Новая задача успешно добавлена'),
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.show_task_in_folder(message.from_user.id, fid))
        except:
            self.bot.send_message(message.chat.id, emojize(f'⚠️ Произошла ошибка при попыке создания задачи'),
                                parse_mode="HTML",
                                reply_markup=self.keybords.back_menu())

    def get_taskrename(self, message, taskid):
        try:
            oldtask = self.BD.task_rename(taskid, message.text)
            config.taskrename[message.from_user.id] = False
            config.inbox[message.from_user.id] = True
            self.bot.send_message(message.from_user.id,
                              f'✅ Задача "{oldtask[1]}" успешно переименована в "{message.text}"',
                              parse_mode="HTML",
                              reply_markup= self.keybords.remove_menu())
            self.bot.send_message(message.from_user.id,
                                  f'<code>Задача {oldtask[0]} {message.text}</code>',
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.show_task_edit_options(taskid))
        except:
            self.bot.send_message(message.chat.id, emojize(f'⚠️ Произошла ошибка при попыке переименования задачи'),
                                parse_mode="HTML",
                                reply_markup=self.keybords.back_menu())











    def pressed_btn_settings(self, message):
        '''
        обработка сообщений от нажатия кнопки settings
        '''
        try:
            self.BD.show_settings("hard", message.from_user.id)
            self.BD.make_settings(message.from_user.id)
        except ReferenceError:
            self.Log.write_log("user id: " + str(message.from_user.id) + ". Ошибка доступа к БД. Не удалось проверить наличие настроеки и профиля пользователя при входе в настройки")
        self.bot.send_message(message.chat.id, MESSAGES['settings'],
                              parse_mode="HTML",
                              reply_markup=self.keybords.settings_menu(message.from_user.id))

    def default_settings(self, message):
        config.inbox[message.from_user.id] = True
        config.taskname[message.from_user.id] = False
        config.taskrename[message.from_user.id] = False
        config.eventdate[message.from_user.id] = False
        config.addfolderteg[message.from_user.id] = False
        config.share[message.from_user.id] = False





    def pressed_btn_back(self, message):
        '''
        обработка сообщений от нажатия кнопки back
        '''
        foldername = {}
        config.inbox[message.from_user.id] = True
        config.taskname[message.from_user.id] = False
        config.taskrename[message.from_user.id] = False
        config.eventdate[message.from_user.id] = False
        config.addfolderteg[message.from_user.id] = False
        config.share[message.from_user.id] = False
        self.bot.send_message(message.chat.id, 'Вы вернулись назад',
                              parse_mode="HTML",
                              reply_markup=self.keybords.start_menu())





    def handle(self):
        '''
        обработчик (декоратор) сообщений
        обрабатывает входящии сообщения от нажатия кнопок
        '''

        @self.bot.message_handler(func=lambda message: True)
        def handle(message):

            #Проверка таймаута пользователя для сброса ввода названия задачи
            if message.text and self.BD.update_user_timer(message.from_user.id) > timedelta(minutes=10):
                print(f"user {message.from_user.id} timeout")
                self.default_settings(message)

            # универсальная кнопка почти для всех меню

            if message.text == config.KEYBOARD['<<']:
                self.pressed_btn_back(message)


            # Главное меню
            if message.text == config.KEYBOARD["INBOX"]:
                self.send_inbox_list(message.from_user.id)
            if message.text == config.KEYBOARD["EVENT"]:
                self.send_events_list(message)

            # Меню инлайн папок (также при отмене действия)

            if message.text == config.KEYBOARD["FOLDERS"] or message.text == config.KEYBOARD['X']:
                self.send_folders_list(message)

            # Ввод текста в бота

            #Добавление задачи в inbox
            if message.text not in config.KEYBOARD.values() and config.inbox.get(message.from_user.id, True) and message.text != "":
                self.get_inbox(message)
            #Добавление ссылки
            if message.text not in config.KEYBOARD.values() and config.is_url.get(message.from_user.id, False) and message.text != "":
                self.rename_inbox(message, config.is_url[message.from_user.id])
            #Ввод названия папки при создании
            if message.text not in config.KEYBOARD.values() and config.foldername.get(message.from_user.id, False) and message.text != "":
                self.get_foldername(message)
            #Ввод названия задачи при создании
            if message.text not in config.KEYBOARD.values() and config.taskname.get(message.from_user.id, False) and message.text != "":
                self.get_taskname(message, config.taskname[message.from_user.id])
            #Изменение названия задачи
            if message.text not in config.KEYBOARD.values() and config.taskrename.get(message.from_user.id, False) and message.text != "":
                self.get_taskrename(message, config.taskrename[message.from_user.id])
            #Изменение названия события
            if message.text not in config.KEYBOARD.values() and config.eventname.get(message.from_user.id, False) and message.text != "":
                self.get_eventname(message, config.eventname[message.from_user.id])
            #Ввод даты события при создании
            if message.text not in config.KEYBOARD.values() and config.eventdate.get(message.from_user.id, False) and message.text != "":
                print(config.eventdate[message.from_user.id])
                self.get_event_day(message, config.eventdate[message.from_user.id])
            #Ввод тега для папки
            if message.text not in config.KEYBOARD.values() and config.addfolderteg.get(message.from_user.id, False) and message.text != "":
                print(config.addfolderteg[message.from_user.id])
                self.get_folderteg(message, config.addfolderteg[message.from_user.id])
            #Ввод ID пользователя для совместного доступа к папке
            if message.text not in config.KEYBOARD.values() and config.share.get(message.from_user.id, False) and message.text != "":
                print(message)
                print(config.share[message.from_user.id])
                self.get_folder_share(message, config.share[message.from_user.id])



