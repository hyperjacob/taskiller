# импортируем класс родитель
from handlers.handler import Handler
# импортируем сообщения пользователю

from settings import config
from emoji import emojize
import os
from datetime import datetime

class HandlerInlineQuery(Handler):
    """
    Класс обрабатывает входящие текстовые
    сообщения от нажатия на инлайн-кнопоки
    """

    def __init__(self, bot):
        super().__init__(bot)

    # Меню "Входящие"


    def pressed_btn_inbox(self, call, code, code2):
        """
        Обрабатывает входящие запросы на нажатие inline-кнопок входящих
        """
        if code == "1":
            self.BD.del_all_task_in_bufer(call.from_user.id)
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id,
                                  f'<code>📥 Входящие</code>\n\n\nВыберите сообщения',
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.set_inline_inbox_task(call.from_user.id))
        elif code == "2":
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id,
                                  f'Выберите сообщение, которое нужно добавить в события:',
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.set_inline_inbox_event(call.from_user.id))
        elif code == "task":
            self.BD.change_inbox_active(int(code2))
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id,
                              f"<code>📥 Входящие</code>\n\n\nНажмите на сообщения для отметки о его выполнении",
                              parse_mode="HTML",
                              reply_markup= self.keybords.set_inline_inbox(call.from_user.id))
        elif code == "choise":
            choise = self.BD.show_task_bufer(call.from_user.id)
            if int(code2) not in choise:
               self.BD.add_task_bufer(int(code2), call.from_user.id)
               print("no", choise, int(code2))
            else:
                self.BD.del_task_from_bufer(int(code2), call.from_user.id)
                print("yes", choise, int(code2))
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id,
                             f'<code>📥 Входящие</code>\n\n\nВыберите сообщения для переноса',
                              parse_mode="HTML",
                              reply_markup= self.keybords.set_inline_inbox_task(call.from_user.id))
        elif code == "folder":
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            try:
                if bool(self.BD.show_task_bufer(call.from_user.id)):
                    text = f'<code>Перемещение задач</code>\n\n\nВыберите папку, в которую требуется переместить задачи'
                else:
                    text = "Вы ничего не выбрали"
                self.bot.send_message(call.from_user.id,
                             text,
                              parse_mode="HTML",
                              reply_markup= self.keybords.show_relocate_folder_inbox(call.from_user.id))
            except:
                self.bot.send_message(call.from_user.id, f'⚠️ Произошла ошибка при попыке переместить задачи',
                                parse_mode="HTML",
                                reply_markup=self.keybords.back_menu())
        elif code == "relocdomass":
            inboxes = self.BD.show_task_bufer(call.from_user.id)
            self.BD.del_all_task_in_bufer(call.from_user.id)
            for el in inboxes:
                name = self.BD.get_inbox_name(el)
                print(el)
                print(name)
                self.BD.add_task(name, int(code2), call.from_user.id)
                self.BD.del_inbox_task(call.from_user.id, el)
            userid = self.BD.select_user_id(call.from_user.id)
            folder = self.BD.find_folder(int(code2), userid)
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id,
                              f"<code>📥 Входящие</code>\n\n\nВыбранные сообщения успешно перенесены в папку {folder[0]} {folder[1]}",
                              parse_mode="HTML",
                              reply_markup= self.keybords.set_inline_inbox(call.from_user.id))
        elif code == "del":
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            inboxes = self.BD.show_task_bufer(call.from_user.id)
            self.BD.del_all_task_in_bufer(call.from_user.id)
            try:
                if bool(inboxes):
                    for el in inboxes:
                        self.BD.del_inbox_task(call.from_user.id, el)
                    text = f'<code>📥 Входящие</code>\n\n\n✅ Сообщения успешно удалены'
                else:
                    text = f'<code>📥 Входящие</code>\n\n\nВы ничего не выбрали'
                self.bot.send_message(call.from_user.id,
                             text,
                              parse_mode="HTML",
                              reply_markup= self.keybords.set_inline_inbox_task(call.from_user.id))
            except:
                self.bot.send_message(call.from_user.id, f'⚠️ Произошла ошибка при попыке переместить задачи',
                                parse_mode="HTML",
                                reply_markup=self.keybords.back_menu())
        elif code == "event":
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            config.inbox[call.from_user.id] = False
            config.eventdate[call.from_user.id] = int(code2)
            self.bot.send_message(call.from_user.id,
                            "Укажите дату события в формате DD.MM.YYYY:",
                            parse_mode="HTML",
                            reply_markup=self.keybords.back_menu())
        elif code == "select":
            '''
            Выбрать все задачи во входящих
            '''
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            choise = self.BD.show_task_bufer(call.from_user.id)
            all_inbox = self.BD.select_all_inbox_by_user(call.from_user.id)
            if len(all_inbox) == len(choise):
                self.BD.del_all_task_in_bufer(call.from_user.id)
            else:
                for el in all_inbox:
                    if el[1] not in choise:
                        self.BD.add_task_bufer(el[1], call.from_user.id)
                    # print("no", choise, el[1])
            self.bot.send_message(call.from_user.id,
                                  f'<code>📥 Входящие</code>\n\n\nВыберите сообщения для переноса',
                                  parse_mode="HTML",
                                  reply_markup= self.keybords.set_inline_inbox_task(call.from_user.id))




    def pressed_btn_inbox_del(self, call, code):
        """
        Обрабатывает входящие запросы на нажатие inline-кнопок входящих
        """
        if code == "back":
            inbox_list = self.BD.select_all_inbox_by_user(call.from_user.id)
            text = "Нажмите на задачу для отметки о ее выполнении"
            if not inbox_list:
                text = "Папка пуста"
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id,
                                  f"<code>📥 Входящие:</code>\n\n\n{text}",
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.set_inline_inbox(call.from_user.id))
        else:
            try:
                self.BD.del_inbox_task(call.from_user.id, int(code))
            except ReferenceError:
                self.Log.write_log("user id: " + str(call.from_user.id) + ". Ошибка доступа к БД. Не удалось изменить уровень сложности")
            # self.bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=None)
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id,
                                  f'Сообщение успешно удалено:',
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.set_inline_inbox_delete(call.from_user.id))


    # Меню "Папки"
    def pressed_btn_folder(self, call, code, code2 = False, code3 = False):
        if config.welcomemsg[call.from_user.id]:
                    print(config.welcomemsg[call.from_user.id], call.message.message_id)
                    self.bot.delete_message(call.from_user.id, config.welcomemsg[call.from_user.id])

                    config.welcomemsg[call.from_user.id] = False
        if code == "new":
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            config.inbox[call.from_user.id] = False
            config.foldername[call.from_user.id] = "New"
            self.bot.send_message(call.from_user.id,
                              "Введите название папки",
                                parse_mode="HTML",
                                reply_markup=self.keybords.cancel_menu())
        elif code == "edit":
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id,
                                  f'Выберите папку для редактирования:',
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.set_inline_folders_edit(call.from_user.id))
        elif code == "mine":
            config.taskname[call.from_user.id] = False
            config.inbox[call.from_user.id] = True
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id,
                              f"📚 Список ваших папок:",
                              parse_mode="HTML",
                              reply_markup= self.keybords.set_inline_folders(call.from_user.id))
        elif code == "editfolder":
            if not self.BD.is_folder_owner(int(code2), call.from_user.id):
                teleid = self.BD.find_teleid(self.BD.folder_owner(int(code2)))
            else:
                teleid = call.from_user.id
            userid = self.BD.select_user_id(teleid)
            folder = self.BD.find_folder(int(code2), userid)
            teg = self.BD.if_teg(int(code2))
            if not teg:
                teg = "Не установлен"
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            if teleid == call.from_user.id:
                self.bot.send_message(call.from_user.id,
                              emojize(f"<code>Папка {folder[0]} {folder[1]}</code>\n\nТег папки: <code>{teg}</code>\n\nВыбирите действие:"),
                              parse_mode="HTML",
                              reply_markup= self.keybords.edit_folder_settings(int(code2)))
            else:

                self.bot.send_message(call.from_user.id,
                              emojize(f"Папка <code>{folder[0]} {folder[1]}</code> (Внешняя папка)\n<b>Уровень доступа:</b>  {config.access_level[folder[4]]}\n\nВыбирите действие:"),
                              parse_mode="HTML",
                              reply_markup= self.keybords.edit_shared_folder_settings(int(code2)))
        elif code == "del":
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            try:
                self.BD.del_folder(call.from_user.id, int(code2))
            except:
                self.bot.send_message(call.from_user.id,
                                  f'<code>Список папок</code>\n\n\n⚠️ Произошла ошибка при попыке удаления задачи:',
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.set_inline_folders(call.from_user.id))
            # self.bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=None)
            self.bot.send_message(call.from_user.id,
                                  f'<code>Список папок</code>\n\n\nПапка успешно удалена:',
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.set_inline_folders(call.from_user.id))
        elif code == "rename":
            config.foldername[call.from_user.id] = int(code2)
            config.inbox[call.from_user.id] = False
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id,
                                  f'<code>📝 Переименование папки</code>\n\n\nВведите новое название:',
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.cancel_menu())
        elif code == "reicon":
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id,
                              f'Выберите значок из предложенных emoji:',
                              parse_mode="HTML",
                              reply_markup= self.keybords.set_inline_emoji(code2, "folder"))
        elif code == "newicon":
            if code2 == "next":
                self.bot.delete_message(call.from_user.id, call.message.message_id)
                self.bot.send_message(call.from_user.id,
                                  f"<code>Список папок</code>\n\n\nВы не задали значок:",
                                  parse_mode="HTML",
                                  reply_markup= self.keybords.set_inline_folders(call.from_user.id))
            else:
                self.BD.add_emoji(config.FICON[int(code2)], int(code3), call.from_user.id)
                self.bot.delete_message(call.from_user.id, call.message.message_id)
                self.bot.send_message(call.from_user.id,
                                  f"<code>Список папок</code>\n\n\nЗначок успешно выбран:",
                                  parse_mode="HTML",
                                  reply_markup= self.keybords.set_inline_folders(call.from_user.id))
        elif code == "teg":
            config.addfolderteg[call.from_user.id] = int(code2)
            config.inbox[call.from_user.id] = False
            teg = self.BD.if_teg(int(code2))
            if not teg:
                teg = "Не установлен"
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id,
                                  f'Текущий тег: <code>{teg}</code>\n\n\nВведите новый тег:',
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.cancel_menu())
        elif code == "share":
            userid = self.BD.select_user_id(call.from_user.id)
            folder = self.BD.find_folder(int(code2), userid)
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            is_shared = self.BD.is_already_share(int(code2))
            if is_shared[0]:
                self.bot.send_message(call.from_user.id,
                                  f'<code>{folder[0]} {folder[1]}</code>\n\n\nК этой папке настроен совместный доступ с пользователем: <code>{is_shared[0]}</code>\nУровень доступа: <code>{config.access_level[is_shared[1]]}</code>',
                                  parse_mode="HTML",
                                  reply_markup= self.keybords.folder_shared(code2))
            else:
                self.bot.send_message(call.from_user.id,
                                  f'<code>{folder[0]} {folder[1]}</code>\n\n\nК этой папке еще не настроен совместный доступ',
                                  parse_mode="HTML",
                                  reply_markup= self.keybords.folder_not_shared(code2))


        elif code == "slide":
            folder_list = self.BD.select_all_folders_from_user(call.from_user.id)
            id_el = 0
            userid = self.BD.select_user_id(call.from_user.id)
            for el in folder_list:
                if el[2] == int(code3):
                    id_el = folder_list.index(el)
            if id_el == len(folder_list) - 1:
                right = folder_list[0]
                left = folder_list[id_el - 1]
            elif id_el == 0:
                left = folder_list[-1]
                right = folder_list[id_el + 1]
            else:
                right = folder_list[id_el + 1]
                left = folder_list[id_el - 1]
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            print("right", right)
            if code2 == "l":
                folder = self.BD.find_folder(left[2], userid)
                self.bot.send_message(call.from_user.id,
                             f'<code>Папка {folder[0]} {folder[1]}</code>\n\n\nВыбирите действие:',
                              parse_mode="HTML",
                              reply_markup= self.keybords.edit_folder_settings(left[2]))
            elif code2 == "r":
                folder = self.BD.find_folder(right[2], userid)
                self.bot.send_message(call.from_user.id,
                             f'<code>Папка {folder[0]} {folder[1]}</code>\n\n\nВыбирите действие:',
                              parse_mode="HTML",
                              reply_markup= self.keybords.edit_folder_settings(right[2]))
        elif code == "sharedtask":
            text = ""
            folder = self.BD.find_folder(int(code2), int(code3))
            print(folder[3])
            friendteleid = self.BD.find_teleid(int(code3))
            if self.BD.is_folder_owner(int(code2), call.from_user.id) or (folder[4] in [2,3,4]):
                config.inbox[call.from_user.id] = False
                config.taskname[call.from_user.id] = int(code2)
            if not self.BD.select_all_tasks_from_folder(friendteleid, int(code2)):
                text = "\n🕸 В этой папке пока пусто"
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            if folder[3]:
                friendid = self.BD.find_teleid(int(code3))
                friend = "<b>Владелец папки:</b>  " + "<code>" + str(friendid) + "</code>"
            self.bot.send_message(call.from_user.id,
                                  f'<code>{folder[0]} {folder[1]}</code> (Внешняя папка)\n\n{friend}\n<b>Уровень доступа:</b>  {config.access_level[folder[4]]}\n{text}',
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.show_task_in_folder(call.from_user.id, int(code2)))
        elif code == "export":
            if not self.BD.is_folder_owner(int(code2), call.from_user.id):
                teleid = self.BD.find_teleid(self.BD.folder_owner(int(code2)))
            else:
                teleid = call.from_user.id
            path = str(call.from_user.id)
            if not os.path.exists(path):
                os.mkdir(path)
            userid = self.BD.select_user_id(teleid)
            folder = self.BD.find_folder(int(code2), userid)
            filename = datetime.now().strftime('%Y_%m_%d') + "_" + folder[1] + ".csv"
            try:
                tasks = self.BD.select_all_tasks_from_folder(teleid, int(code2))
            except:
                self.bot.send_message(call.from_user.id,
                                  f'<code>Список папок</code>\n\n\n⚠️ Произошла ошибка при попыке экспорта папки:',
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.set_inline_folders(call.from_user.id))
                return False
            with open(path + "/" + filename, "w") as f:
                    complite = ["Выполнено", "Не выполнено"]
                    f.write("Дата;Название;Отметка о выполнении\n")
                    for el in tasks:
                        f.write(el[4].strftime('%Y.%m.%d %H:%M:%S') +";" +el[1] + ";"+ complite[int(el[3])] + "\n")
            self.bot.send_document(call.from_user.id, open(path + "/" + filename, 'rb'))
        else:
            self.BD.del_all_task_in_bufer(call.from_user.id)
            text = ""
            if not self.BD.is_folder_owner(int(code), call.from_user.id):
                teleid = self.BD.find_teleid(self.BD.folder_owner(int(code)))
            else:
                teleid = call.from_user.id
            friend = ""
            userid = self.BD.select_user_id(teleid)
            folder = self.BD.find_folder(int(code), userid)
            if self.BD.is_folder_owner(int(code), call.from_user.id) or (folder[4] in [2,3,4]):
                config.inbox[call.from_user.id] = False
                config.taskname[call.from_user.id] = int(code)
            if not self.BD.select_all_tasks_from_folder(teleid, int(code)):
                text = "\nВ этой папке пока пусто"
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            teg = folder[2]
            if not teg:
                teg = "отсутствует"
            if folder[3]:
                friend = "<b>Совместный доступ:</b>  " + "<code>" + str(folder[3]) + "</code>"
            self.bot.send_message(call.from_user.id,
                                  f'<code>{folder[0]} {folder[1]}</code>\n\n<b>Тег:</b>  <code>{teg}</code>\n{friend}\n{text}',
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.show_task_in_folder(call.from_user.id, int(code)))


    def share_folder(self, call, code, code2, code3 = None):
        if code == "invite":
            userid = self.BD.select_user_id(call.from_user.id)
            folder = self.BD.find_folder(int(code2), userid)
            config.share[call.from_user.id] = int(code2)
            config.inbox[call.from_user.id] = False
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id,
                                  f'<code>{folder[0]} {folder[1]}</code>\n\nВведите ID пользователя, которого хотите добавить <i>(ID можно узнать зайдя в настройки у добавляемого пользователя)</i>',
                                  parse_mode="HTML", reply_markup=self.keybords.cancel_menu())
        elif code == "alvl":
            userid = self.BD.select_user_id(call.from_user.id)
            folder = self.BD.find_folder(int(code2), userid)
            friend = self.BD.change_access_lvl(int(code2), call.from_user.id, int(code3))
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id,
                                  f'Уровень доступа к папке <code>{folder[0]} {folder[1]}</code> для пользователя {friend} успешно изменен на "{config.access_level[int(code3)]}"',
                                  parse_mode="HTML", reply_markup=self.keybords.set_inline_folders(call.from_user.id))
        elif code == "cancel":
            oldfriend = self.BD.cancel_access(int(code2))
            if not self.BD.is_folder_owner(int(code2), call.from_user.id):
                teleid = self.BD.find_teleid(self.BD.folder_owner(int(code2)))
            else:
                teleid = call.from_user.id
            userid = self.BD.select_user_id(teleid)
            folder = self.BD.find_folder(int(code2), userid)
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id,
                                  f'💔Доступ пользователя {oldfriend} к папке {folder[0]} {folder[1]} прекращен',
                                  parse_mode="HTML", reply_markup=self.keybords.set_inline_folders(call.from_user.id))
        elif code == "change":
            userid = self.BD.select_user_id(call.from_user.id)
            folder = self.BD.find_folder(int(code2), userid)
            access_lvl = self.BD.is_already_share(int(code2))
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id,
                                  f'<code>{folder[0]} {folder[1]}</code>\n\nТекущий уровень доступа пользователя {access_lvl[0]}: "<b>{config.access_level[access_lvl[1]]}</b>"\n\nВыберите новый уровень доступа для данного пользователя:',
                                  parse_mode="HTML", reply_markup=self.keybords.set_access_lvl(int(code2)))

    def pressed_btn_folder_del(self, call, code):
        if code == "back":
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id,
                              f"📚 Список ваших папок:",
                              parse_mode="HTML",
                              reply_markup= self.keybords.set_inline_folders(call.from_user.id))
        else:
            try:
                self.BD.del_folder(call.from_user.id, int(code))
            except:
                self.Log.write_log("user id: " + str(call.from_user.id) + ". Ошибка доступа к БД. Не удалось удалить папку")
            # self.bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=None)
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id,
                                  f'Папка успешно удалена:',
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.set_inline_folders_del(call.from_user.id))


    # Задачи
    def pressed_btn_tasks_list(self, call, code, code2 = None, fid = None):
        if code == "new":
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            config.inbox[call.from_user.id] = False
            config.taskname[call.from_user.id] = int(code2)
            self.bot.send_message(call.from_user.id,
                              "Введите название задачи",
                                parse_mode="HTML",
                                reply_markup=self.keybords.cancel_menu())
        elif code == "edit":
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id,
                                   f"<code>✏️ Редактировать задачу </code>\n\n\nВыберите задачу для того, чтобы начать ее редактировать:",
                              parse_mode="HTML",
                              reply_markup= self.keybords.show_task_in_folder_for_edit(call.from_user.id, int(code2)))
        elif code == "back1":
            config.taskname[call.from_user.id] = False
            config.inbox[call.from_user.id] = True
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id,
                              f"📚 Список ваших папок:",
                              parse_mode="HTML",
                              reply_markup= self.keybords.set_inline_folders(call.from_user.id))
        elif code == "list":
            friend = ""
            teg = ""
            if not self.BD.is_folder_owner(int(fid), call.from_user.id):
                teleid = self.BD.find_teleid(self.BD.folder_owner(int(fid)))
            else:
                teleid = call.from_user.id
            userid = self.BD.select_user_id(teleid)
            folder = self.BD.find_folder(int(fid), userid)
            if self.BD.is_folder_owner(int(fid), call.from_user.id) or (folder[4] in [1,3,4]):
                self.BD.change_complite_task(int(code2))
            if self.BD.is_folder_owner(int(fid), call.from_user.id) or (folder[4] in [2,3,4]):
                config.inbox[call.from_user.id] = False
                config.taskname[call.from_user.id] = int(fid)
            if folder[2]:
                teg = folder[2]
            else:
                teg = "отсутствует"
            text = f"{folder[0]} <code>{folder[1]}</code>\n\n<b>Тег:</b> <code>{teg}</code>\n\n<i>ℹ️ Для добавления задач в папку просто введите их с клавиатуры</i>"
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            if folder[3]:
                friend = "<b>Владелец папки:</b>  " + "<code>" + str(teleid) + "</code>"
                text = f'<code>{folder[0]} {folder[1]}</code> (Внешняя папка)\n\n{friend}\n<b>Уровень доступа:</b>  {config.access_level[folder[4]]}\n'
            self.bot.send_message(call.from_user.id,
                                  text,
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.show_task_in_folder(call.from_user.id, int(fid)))
        elif code == "select":
            ''' Выбать все задачи в папке '''
            if not self.BD.is_folder_owner(int(code2), call.from_user.id):
                teleid = self.BD.find_teleid(self.BD.folder_owner(int(code2)))
            else:
                teleid = call.from_user.id
            userid = self.BD.select_user_id(teleid)
            folder = self.BD.find_folder(int(code2), userid)
            choise = self.BD.show_task_bufer(call.from_user.id)
            print("select", choise)
            all_tasks = self.BD.select_all_tasks_from_folder(teleid, int(code2))
            if len(choise) == len(all_tasks):
                self.BD.del_all_task_in_bufer(call.from_user.id)
            else:
                for el in all_tasks:
                    if el[2] not in choise:
                        self.BD.add_task_bufer(el[2], call.from_user.id)
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id,
                                  f'<code>{folder[0]} {folder[1]}</code>\n\n\nВыберите задачи',
                                  parse_mode="HTML",
                                  reply_markup= self.keybords.show_task_for_choise(call.from_user.id, int(code2)))
        elif code == "task":
            task = self.BD.task_name(int(code2))
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id,
                                  f'<code>Задача {task[0]} {task[1]}</code>\n\n\nВыбирите действие:',
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.show_task_edit_options(int(code2)))
        elif code == "rename":
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            config.inbox[call.from_user.id] = False
            config.taskrename[call.from_user.id] = int(code2)
            self.bot.send_message(call.from_user.id,
                              "📝 Введите новое название задачи",
                                parse_mode="HTML",
                                reply_markup=self.keybords.cancel_menu())
        elif code == "reicon":
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id,
                              f'Выберите значок из предложенных emoji:',
                              parse_mode="HTML",
                              reply_markup= self.keybords.set_inline_emoji(code2, "task"))
        elif code == "newicon":
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            if code2 == "next":
                task = self.BD.task_name(int(fid))
                self.bot.send_message(call.from_user.id,
                                  f'<code>Задача {task[0]} {task[1]}</code>\n\n\nВыбирите действие:',
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.show_task_edit_options(int(fid)))
            else:
                # print(int(fid), config.TICON[int(code2)])
                oldicon = self.BD.task_icon(int(fid), config.TICON[int(code2)])
                print(oldicon)
                self.bot.send_message(call.from_user.id,
                                 f'<code>Задача {config.TICON[int(code2)]} {oldicon[1]}</code>\n\n\nЗначок была изменена {oldicon[0]} ➡️ {config.TICON[int(code2)]}',
                                  parse_mode="HTML",
                                  reply_markup= self.keybords.show_task_edit_options(int(fid)))
        elif code == "del":
            try:
                idfolder = self.BD.task_location(int(code2))
                if not self.BD.is_folder_owner(int(idfolder), call.from_user.id):
                    teleid = self.BD.find_teleid(self.BD.folder_owner(int(idfolder)))
                else:
                    teleid = call.from_user.id
                userid = self.BD.select_user_id(teleid)
                folder = self.BD.find_folder(idfolder, userid)
                taskdel = self.BD.task_del(int(code2))
                self.bot.delete_message(call.from_user.id, call.message.message_id)
                self.bot.send_message(call.from_user.id,
                             f'<code>{folder[0]} {folder[1]}</code>\n\n\nЗадача {taskdel[0]} {taskdel[1]} удалена',
                              parse_mode="HTML",
                              reply_markup= self.keybords.show_task_in_folder(call.from_user.id, idfolder))
            except:
                self.bot.send_message(call.from_user.id, f'⚠️ Произошла ошибка при попыке удаления задачи',
                                parse_mode="HTML",
                                reply_markup=self.keybords.back_menu())
        elif code == "reloc":
            try:
                idfolder = self.BD.task_location(int(code2))
                task = self.BD.task_name(int(code2))
                self.bot.delete_message(call.from_user.id, call.message.message_id)
                self.bot.send_message(call.from_user.id,
                             f'<code>Задача {task[0]} {task[1]}</code>\n\n\nВыберите папку, в которую требуется переместить задачу',
                              parse_mode="HTML",
                              reply_markup= self.keybords.show_relocate_folder(idfolder, int(code2), call.from_user.id))
            except:
                self.bot.send_message(call.from_user.id, f'⚠️ Произошла ошибка при попыке переместить задачу')

        elif code == "relocdo":
            status = self.BD.change_task_location(int(code2), int(fid))
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            task = self.BD.task_name(int(code2))
            if status:
                userid = self.BD.select_user_id(call.from_user.id)
                folder = self.BD.find_folder(int(fid), userid)
                self.bot.send_message(call.from_user.id,
                             f'<code>Задача {task[0]} {task[1]}</code>\n\n\nЗадача {task[0]} {task[1]} была успешно перемещена в папку {folder[0]} {folder[1]}',
                              parse_mode="HTML",
                              reply_markup= self.keybords.show_task_edit_options(int(code2)))
        elif code == "remind":
            pass





        elif code == "slide":
            idfolder = self.BD.task_location(int(fid))
            if not self.BD.is_folder_owner(int(idfolder), call.from_user.id):
                teleid = self.BD.find_teleid(self.BD.folder_owner(int(idfolder)))
            else:
                teleid = call.from_user.id

            all_task_list = self.BD.select_all_tasks_from_folder(teleid, idfolder)
            task_list = []
            for el in all_task_list:
                if el[3]:
                    task_list.append(el)
            id_el = 0
            for el in task_list:
                if el[2] == int(fid):
                    id_el = task_list.index(el)
            if id_el == len(task_list) - 1:
                right = task_list[0]
                left = task_list[id_el - 1]
            elif id_el == 0:
                left = task_list[-1]
                right = task_list[id_el + 1]
            else:
                right = task_list[id_el + 1]
                left = task_list[id_el - 1]
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            print("right", right)
            if code2 == "l":
                task = self.BD.task_name(left[2])
                self.bot.send_message(call.from_user.id,
                             f'<code>Задача {task[0]} {task[1]}</code>\n\n\nВыбирите действие:',
                              parse_mode="HTML",
                              reply_markup= self.keybords.show_task_edit_options(left[2]))
            elif code2 == "r":
                task = self.BD.task_name(right[2])
                self.bot.send_message(call.from_user.id,
                             f'<code>Задача {task[0]} {task[1]}</code>\n\n\nВыбирите действие:',
                              parse_mode="HTML",
                              reply_markup= self.keybords.show_task_edit_options(right[2]))
        elif code == "choise":
            if not self.BD.is_folder_owner(int(code2), call.from_user.id):
                teleid = self.BD.find_teleid(self.BD.folder_owner(int(code2)))
            else:
                teleid = call.from_user.id
            userid = self.BD.select_user_id(teleid)
            folder = self.BD.find_folder(int(code2), userid)
            print("first idf", int(code2))
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id,
                             f'<code>{folder[0]} {folder[1]}</code>\n\n\nВыберите задачи',
                              parse_mode="HTML",
                              reply_markup= self.keybords.show_task_for_choise(call.from_user.id, int(code2)))
        elif code == "choisetask":
            idfolder = self.BD.task_location(int(code2))
            if not self.BD.is_folder_owner(idfolder, call.from_user.id):
                teleid = self.BD.find_teleid(self.BD.folder_owner(idfolder))
            else:
                teleid = call.from_user.id
            userid = self.BD.select_user_id(teleid)

            idfolder = self.BD.task_location(int(code2))
            folder = self.BD.find_folder(idfolder, userid)
            print("idf",idfolder)
            choise = self.BD.show_task_bufer(call.from_user.id)
            if int(code2) not in choise:
               self.BD.add_task_bufer(int(code2), call.from_user.id)
               print("no", choise, int(code2))
            else:
                self.BD.del_task_from_bufer(int(code2), call.from_user.id)
                print("yes", choise, int(code2))
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id,
                             f'<code>{folder[0]} {folder[1]}</code>\n\n\nВыберите задачи',
                              parse_mode="HTML",
                              reply_markup= self.keybords.show_task_for_choise(call.from_user.id, idfolder))
        elif code == "massreloc":

            self.bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=None)
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            try:
                if bool(self.BD.show_task_bufer(call.from_user.id)):
                    text = f'<code>Перемещение задач</code>\n\n\nВыберите папку, в которую требуется переместить задачи'
                else:
                    text = "Вы ничего не выбрали"
                self.bot.send_message(call.from_user.id,
                             text,
                              parse_mode="HTML",
                              reply_markup= self.keybords.show_relocate_folder_mass(call.from_user.id, int(code2)))
            except:
                self.bot.send_message(call.from_user.id, f'⚠️ Произошла ошибка при попыке переместить задачи',
                                parse_mode="HTML",
                                reply_markup=self.keybords.back_menu())
        elif code == "relocdomass":
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            try:
                tasks = self.BD.show_task_bufer(call.from_user.id)
                self.BD.del_all_task_in_bufer(call.from_user.id)
                for el in tasks:
                    status = self.BD.change_task_location(el, int(code2))

                userid = self.BD.select_user_id(call.from_user.id)
                folder = self.BD.find_folder(int(code2), userid)
                self.bot.send_message(call.from_user.id,
                                 f'<code>{folder[0]} {folder[1]}</code>\n\n\nЗадачи успешно перемещены в папку {folder[0]} {folder[1]}',
                                  parse_mode="HTML",
                                  reply_markup= self.keybords.show_task_in_folder(call.from_user.id, int(code2)))
            except:
                self.bot.send_message(call.from_user.id, f'⚠️ Произошла ошибка при попыке переместить задачи',
                                parse_mode="HTML",
                                reply_markup=self.keybords.back_menu())
        elif code == "massdel":
            try:
                if not self.BD.is_folder_owner(int(code2), call.from_user.id):
                    teleid = self.BD.find_teleid(self.BD.folder_owner(int(code2)))
                else:
                    teleid = call.from_user.id
                userid = self.BD.select_user_id(teleid)
                print(userid)
                folder = self.BD.find_folder(int(code2), userid)
                tasks = self.BD.show_task_bufer(call.from_user.id)
                self.BD.del_all_task_in_bufer(call.from_user.id)
                if tasks:
                    for el in tasks:
                        taskdel = self.BD.task_del(el)
                    print(taskdel)
                    text = "Задачи удалены"
                else:
                    text = "Вы ничего не выбрали"
                self.bot.delete_message(call.from_user.id, call.message.message_id)
                self.bot.send_message(call.from_user.id,
                             f'<code>{folder[0]} {folder[1]}</code>\n\n\n{text}',
                              parse_mode="HTML",
                              reply_markup= self.keybords.show_task_in_folder(call.from_user.id, int(code2)))
            except:
                self.bot.send_message(call.from_user.id, f'⚠️ Произошла ошибка при попыке удаления задачи',
                                parse_mode="HTML",
                                reply_markup=self.keybords.back_menu())

    #События

    def pressed_btn_event(self, call, code, code2 = None, code3 = None):
        self.bot.delete_message(call.from_user.id, call.message.message_id)
        #Редактирование
        if code == "rename":
            config.eventname[call.from_user.id] = int(code2)
            config.inbox[call.from_user.id] = False
            self.bot.send_message(call.from_user.id,
                                  f'<code>📝 Переименование события</code>\n\n\nВведите новое название:',
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.cancel_menu())
        elif code == "reicon":
            self.bot.send_message(call.from_user.id,
                              f'Выберите значок из предложенных emoji:',
                              parse_mode="HTML",
                              reply_markup= self.keybords.set_inline_emoji(code2, "event"))
        elif code == "newicon":
                oldicon = self.BD.add_event_emoji(config.EICON[int(code2)], int(code3))
                event = self.BD.show_event_info(int(code3))
                text = ""
                print("oldicon", oldicon, "event", event)
                if oldicon:
                    text = 'c ' + oldicon
                    print("oldicon true")
                self.bot.send_message(call.from_user.id,
                                  f"Событие {event[0]} <b>{event[1]}</b>\n\nИконка успешно изменена {text} на {event[0]}\nВыбирите действие:",
                                      parse_mode="HTML",
                                      reply_markup=self.keybords.event_edit(int(code2), "eventlist"))
        elif code == "list":
            print(code2)
            event = self.BD.show_event_info(int(code2))
            self.bot.send_message(call.from_user.id,
                                  f"<b>Событие {event[0]} {event[1]}</b>\n\n\nВыбирите действие:",
                                  parse_mode="HTML",
                                   reply_markup=self.keybords.event_edit(int(code2), "eventlist"))
        elif code == "back":
            if code2 == "eventlist":
                event_list = self.BD.show_event_list(call.from_user.id)
                text = "Список ваших событий"
                if not event_list:
                    text = "Папка пуста"
                self.bot.send_message(call.from_user.id,
                                      f"<code>🗓 События</code>\n\n\n{text}",
                                      parse_mode="HTML",
                                      reply_markup= self.keybords.set_inline_events(call.from_user.id))
            elif code2 == "inbox":
                inbox_list = self.BD.select_all_inbox_by_user(call.from_user.id)
                text = "Нажмите на задачу для отметки о ее выполнении"
                if not inbox_list:
                    text = "Папка пуста"
                self.bot.send_message(call.from_user.id,
                                      f"<code>📥 Входящие</code>\n\n\n{text}",
                                      parse_mode="HTML",
                                      reply_markup= self.keybords.set_inline_inbox(call.from_user.id))




    #Выход из инлайн меню в основное
    def pressed_btn_back(self, call):
        self.bot.delete_message(call.from_user.id, call.message.message_id)
        self.bot.send_message(call.from_user.id,
                              "Вы вернулись в главное меню",
                              reply_markup=self.keybords.start_menu())


    def handle(self):
        # обработчик(декоратор) запросов от нажатия на кнопки товара.
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            code = call.data.split(".")
            print(code)
            if code[0] == "back":
                self.pressed_btn_back(call)
            if code[0] == "i":
                # Обработка входящих
                self.pressed_btn_inbox(call, code[1], code[2])
            if code[0] == "d":
                # Обработка удаления из папки входящих
                self.pressed_btn_inbox_del(call, code[1])

            if code[0] == "f":
                # Обработка списка папок
                if len(code) == 2:
                    self.pressed_btn_folder(call, code[1])
                elif len(code) == 3:
                    self.pressed_btn_folder(call, code[1], code[2])
                elif len(code) == 4:
                    self.pressed_btn_folder(call, code[1], code[2], code[3])

            if code[0] == "fd":
                # Удаление папки
                self.pressed_btn_folder_del(call, code[1])

            if code[0] == "t":
                # Действия с задачей в списке
                if len(code) == 3:
                    self.pressed_btn_tasks_list(call, code[1], code[2])
                elif len(code) == 4:
                    self.pressed_btn_tasks_list(call, code[1], code[2], code[3])

            if code[0] =="s":
                # расшаривание папки
                if len(code) == 3:
                    self.share_folder(call, code[1], code[2])
                elif len(code) == 4:
                    self.share_folder(call, code[1], code[2], code[3])

            if code[0] =="e":
                if len(code) == 3:
                    self.pressed_btn_event(call, code[1], code[2])
                elif len(code) == 4:
                    self.pressed_btn_event(call, code[1], code[2], code[3])
