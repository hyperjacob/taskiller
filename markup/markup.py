# импортируем специальные типы телеграм бота для создания элементов интерфейса
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
# импортируем настройки и утилиты
from settings import config
# импортируем класс-менеджер для работы с библиотекой
from data_base.dbalchemy import DBManager
from emoji import emojize
from datetime import datetime

from settings import utility


class Keyboards:
    """
    Класс Keyboards предназначен для создания и разметки интерфейса бота
    """
    # инициализация разметки

    def __init__(self):
        self.markup = None
        # инициализируем менеджер для работы с БД
        self.BD = DBManager()

    def set_btn(self, name, step=0, quantity=0, userid=0):
        """
        Создает и возвращает кнопку по входным параметрам
        """

        return KeyboardButton(config.KEYBOARD[name])

    # Работа с основным меню
    def start_menu(self):
        '''
        создаем разметку кнопок в основном меню (кнопочным)
        '''
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('INBOX')
        itm_btn_2 = self.set_btn('EVENT')
        itm_btn_3 = self.set_btn('FOLDERS')
        itm_btn_4 = self.set_btn('INFO')
        itm_btn_5 = self.set_btn('SETTINGS')
        # располагаем кнопки в меню
        self.markup.row(itm_btn_1, itm_btn_2, itm_btn_3)
        self.markup.row(itm_btn_4, itm_btn_5)
        return self.markup

    def back_menu(self):
        '''
        создаем разметку кнопок в основном меню info
        '''
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('<<')
        # располагаем кнопки в меню
        self.markup.row(itm_btn_1)
        return self.markup

    def cancel_menu(self):
        '''
        создаем разметку кнопок в основном меню info
        '''
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('X')
        # располагаем кнопки в меню
        self.markup.row(itm_btn_1)
        return self.markup

    def settings_menu(self, userid):
        '''
        создаем разметку кнопок в основном меню settings
        '''
        self.markup = ReplyKeyboardMarkup(True, True)

        if self.BD.show_settings("lang", userid) == "RU":
            itm_btn_1 = self.set_btn('LANGRU')
        elif self.BD.show_settings("lang", userid) == "EN":
            itm_btn_1 = self.set_btn('LANGEN')
        else:
            itm_btn_1 = self.set_btn('X')
        itm_btn_2 = self.set_btn('HARD', userid=userid)
        itm_btn_3 = self.set_btn('CHANGE_NAME')
        itm_btn_4 = self.set_btn('<<')
        # располагаем кнопки в меню
        self.markup.row(itm_btn_1, itm_btn_2)
        self.markup.row(itm_btn_3, itm_btn_4)
        return self.markup

    def remove_menu(self):
        '''
        удаляем старое меню
        '''

        return ReplyKeyboardRemove()



    def set_inline_btn(self, name, id):
        '''
        :param name: имя кнопки
        :return: возвращаем созданную инлайн кнопку
        '''

        return InlineKeyboardButton(str(name),
                                    callback_data=id)

    #Входящие
    def set_inline_inbox(self, teleid):
        '''
        :param name: идентификатор пользователя
        :return: возвращает список задач из папки "Входящие"
        '''
        inbox_list = self.BD.select_all_inbox_by_user(teleid)
        self.markup = InlineKeyboardMarkup(row_width=2)
        if inbox_list:
            mass = []
            for el in inbox_list:
                if el[2]:
                    self.markup.row(self.set_inline_btn(el[0], "i.task." + str(el[1])))
                else:
                    text = utility.strike(el[0])
                    mass.append([emojize("️✅ ") + text, "i.task." + str(el[1])])
            for el in mass:
                self.markup.row(self.set_inline_btn(el[0], el[1]))
            self.markup.row(self.set_inline_btn(emojize("⚪ Выбрать"), "i.1.None"), self.set_inline_btn(emojize("📆 В события"), "i.2.None"))
        self.markup.add(self.set_inline_btn(emojize("⏪ Назад"), "back"))
        return self.markup


    def set_inline_inbox_event(self, teleid):
        '''
        Создает разметку инлайн кнопок для преобразования входящих задач в события
        :param teleid: идентификатор пользователя
        :return: возвращает список задач из папки "входящие"
        '''
        self.markup = InlineKeyboardMarkup(row_width=1)
        if self.BD.select_all_inbox_by_user(teleid):
            for el in self.BD.select_all_inbox_by_user(teleid):
                self.markup.add(self.set_inline_btn(emojize(el[0] + " 📤"), "i.event." + str(el[1])))
        self.markup.add(self.set_inline_btn(emojize("⏪ Назад"), "d.back"))
        return self.markup

    def set_inline_inbox_task(self, teleid):
        '''
        Создает разметку инлайн кнопок для массового выбора задач с целью их дальнейшего удаления или перемещения в папку
        :param teleid: идентификатор пользователя
        :return: возвращает список задач и кнопки управления: "удалить" и "переместить в папку"
        '''
        self.markup = InlineKeyboardMarkup(row_width=2)
        '''
        загружаем в названия инлайн кнопок данные из БД
        '''
        text = "🔘 Выбрать все"
        if self.BD.select_all_inbox_by_user(teleid):
            choise = self.BD.show_task_bufer(teleid)
            complete_task = []
            alltask = self.BD.select_all_inbox_by_user(teleid)
            for el in alltask:
                print("choise", el, choise)
                if el[1] not in choise and el[2]:
                    print(choise)
                    self.markup.add(self.set_inline_btn(emojize("⚪️") + emojize(el[0]), "i.choise." + str(el[1])))
                elif el[1] in choise and el[2]:
                    self.markup.add(self.set_inline_btn(emojize("🔘") + emojize(el[0]), "i.choise." + str(el[1])))
                elif el[1] not in choise and not el[2]:
                    text = utility.strike(el[0])
                    complete_task.append([emojize("⚪ ️️") + emojize("️✅ ") + text, "i.choise." + str(el[1])])
                elif el[1] in choise and not el[2]:
                    text = utility.strike(el[0])
                    complete_task.append([emojize("🔘 ") + emojize("️✅ ") + text, "i.choise." + str(el[1])])
            print(complete_task)
            for el in complete_task:
                self.markup.add(self.set_inline_btn(el[0], el[1]))
            if len(choise) == len(alltask):
                text = "⚪️️ Снять выбор"
            else:
                text = "🔘 Выбрать все"
        self.markup.row(self.set_inline_btn(emojize("📁 В папку"), "i.folder.None"),self.set_inline_btn(emojize(text), "i.select.None"), self.set_inline_btn(emojize("❌ Удалить"), "i.del.None"))
        self.markup.add(self.set_inline_btn(emojize("⏪ Назад"), "d.back"))
        return self.markup


    def show_relocate_folder_inbox(self, teleid):
        '''
        Создает разметку инлайн кнопок для выбора целевой папки, в которую нужно переместить входящие
        :param teleid: идентификатор пользователя
        :return: возвращает список папок
        '''
        self.markup = InlineKeyboardMarkup(row_width=2)
        tasks = self.BD.show_task_bufer(teleid)
        if bool(tasks):
            for el in self.BD.select_all_folders_from_user(teleid):
                self.markup.add(self.set_inline_btn(emojize(el[0]) + " " + emojize(el[1]), "i.relocdomass." + str(el[2])))
        self.markup.add(self.set_inline_btn(emojize("⏪ Назад"), "d.back"))
        return self.markup

    #Работа с папками
    def set_inline_folders(self, teleid):
        '''
        Возвращает список папок пользователя, включая расшаренные ему
        :param teleid: id пользователя
        :return: возвращает список
        '''
        self.markup = InlineKeyboardMarkup(row_width=2)
        shared = ""
        if bool(self.BD.select_all_folders_from_user(teleid)):
            for el in self.BD.select_all_folders_from_user(teleid):
                if el[3]:
                    shared = emojize(" 🔗")
                else:
                    shared = ""
                self.markup.add(self.set_inline_btn(emojize(el[0]) + " " + emojize(el[1]) + shared, "f." + str(el[2])))
        if bool(self.BD.show_share_folder(teleid)):
            for el in self.BD.show_share_folder(teleid):
                self.markup.add(self.set_inline_btn(emojize(el[0]) + " " + emojize(el[1]) + " 👥", "f.sharedtask." + str(el[2]) + "." + str(el[3])))
        self.markup.row(self.set_inline_btn(emojize("➕ Создать"), "f.new"), self.set_inline_btn(emojize("✏️ Редактировать"), "f.edit"))
        self.markup.add(self.set_inline_btn(emojize("⏪ Назад"), "back"))
        return self.markup

    #Общие функции
    def set_inline_emoji(self, id, content):
        self.markup = InlineKeyboardMarkup(row_width=3)
        icons = []
        lable = ""
        if content == "folder":
            icons = config.FICON
            lable = "f.newicon"
        elif content == "task":
            icons = config.TICON
            lable = "t.newicon"
        elif content == "event":
            icons = config.EICON
            lable = "e.newicon"
        for i in range(0, len(icons), 3):
            self.markup.row(self.set_inline_btn(emojize(icons[i]), lable + "." + str(i) + "." +  str(id)), self.set_inline_btn(emojize(icons[i+1]), lable + "." + str(i+1) + "." +  str(id)), self.set_inline_btn(emojize(icons[i+2]), lable + "." + str(i+2) + "." +  str(id)))
        self.markup.add(self.set_inline_btn(emojize("Пропустить ⏩"), lable + ".next." + str(id)))
        return self.markup


    def set_inline_folders_edit(self, teleid):
        '''
        список для редактирования папок
        '''
        self.markup = InlineKeyboardMarkup(row_width=1)

        if bool(self.BD.select_all_folders_from_user(teleid)):
            for el in self.BD.select_all_folders_from_user(teleid):
                self.markup.add(self.set_inline_btn(emojize(el[0]) + " " + emojize(el[1]) + " ✏️", "f.editfolder." + str(el[2])))
        if bool(self.BD.show_share_folder(teleid)):
            for el in self.BD.show_share_folder(teleid):
                self.markup.add(self.set_inline_btn(emojize(el[0]) + " " + emojize(el[1]) + " 👥"+ " ✏️", "f.editfolder." + str(el[2]) + "." + str(el[3])))
        self.markup.add(self.set_inline_btn(emojize("⏪ Назад"), "f.mine"))
        return self.markup

    def edit_folder_settings(self, folderid):
        '''
        Показывает опции редактирования папок
        '''
        self.markup = InlineKeyboardMarkup(row_width=3)
        self.markup.row(self.set_inline_btn(emojize("📝 Переименовать"), "f.rename."  + str(folderid)),
                        self.set_inline_btn(emojize("🌅 Значок"), "f.reicon."  + str(folderid)),
                        self.set_inline_btn(emojize("❌ Удалить"), "f.del."  + str(folderid)))
        self.markup.row(self.set_inline_btn(emojize("#️⃣ Тег"), "f.teg."  + str(folderid)),
                        self.set_inline_btn(emojize("👥 Общий доступ"), "f.share."  + str(folderid)),
                        self.set_inline_btn(emojize("📧 Экспортировать"), "f.export."  + str(folderid)))
        self.markup.row(self.set_inline_btn(emojize("⬅️ Предыдущая"), "f.slide.l."  + str(folderid)),
                        self.set_inline_btn(emojize("➡️ Следующая"), "f.slide.r."  + str(folderid)))
        self.markup.add(self.set_inline_btn(emojize("⏪ Назад"), "f.mine"))
        return self.markup

    def edit_shared_folder_settings(self, folderid):
        '''
        Показывает опции редактирования внешних папок
        '''
        self.markup = InlineKeyboardMarkup(row_width=1)
        self.markup.row(self.set_inline_btn(emojize("⬅️ Назад"), "f.mine"),
                        self.set_inline_btn(emojize("💔 Разорвать связь"), "s.cancel."  + str(folderid)))
        return self.markup

    def folder_shared(self, idfolder):
        self.markup = InlineKeyboardMarkup(row_width=2)
        self.markup.row(self.set_inline_btn(emojize("📶 Уровень доступа"), "s.change."  + str(idfolder)),
                        self.set_inline_btn(emojize("💔 Закрыть доступ"), "s.cancel."  + str(idfolder)))
        self.markup.add(self.set_inline_btn(emojize("⏪ Назад"), "f.mine"))
        return self.markup

    def set_access_lvl(self, idfolder):
        self.markup = InlineKeyboardMarkup(row_width=1)
        i = 0
        for el in config.access_level:
            self.markup.add(self.set_inline_btn(el, "s.alvl." + str(idfolder) + "." + str(i)))
            i += 1
        self.markup.add(self.set_inline_btn(emojize("⏩ Пропустить"), "f.mine"))
        return self.markup

    def folder_not_shared(self, idfolder):
        self.markup = InlineKeyboardMarkup(row_width=1)
        self.markup.add(self.set_inline_btn(emojize("🗣 Пригласить"), "s.invite."+ str(idfolder)))
        self.markup.add(self.set_inline_btn(emojize("⏪ Назад"), "f.mine"))
        return self.markup



    def show_task_in_folder(self, teleid, folderid):
        '''
        перечень задач в папке
        '''
        access_lvl = -1
        friendid = False
        if not self.BD.is_folder_owner(folderid, teleid):
            friendid = teleid
            access_lvl = self.BD.is_already_share(folderid)[1]
            teleid = self.BD.find_teleid(self.BD.folder_owner(folderid))
            print(f"teleid: {teleid}, friendid: {friendid}")
        self.markup = InlineKeyboardMarkup(row_width=2)
        if bool(self.BD.select_all_tasks_from_folder(teleid, folderid)):
            print("del_all_task_in_bufer", self.BD.del_all_task_in_bufer(teleid))
            complete_task = []
            for el in self.BD.select_all_tasks_from_folder(teleid, folderid):
                if el[3]:
                    self.markup.add(self.set_inline_btn(emojize(el[0]) + " " + emojize(el[1]) , "t.list." + str(el[2]) + "." + str(folderid)))
                else:
                    text = utility.strike(el[1])
                    complete_task.append([emojize("️✅ ") + emojize(el[0]) + text, "t.list." + str(el[2]) + "." + str(folderid)])
            for el in complete_task:
                self.markup.add(self.set_inline_btn(el[0], el[1]))
        #Проверка, что пользователь является создателем папки, либо имеет доступ на создание задач

        if not friendid or access_lvl == 4:
             self.markup.row(self.set_inline_btn(emojize("✏️ Редактировать"), "t.edit." + str(folderid)), self.set_inline_btn(emojize("⚪️ Выбрать"), "t.choise." + str(folderid)))
        self.markup.row(self.set_inline_btn(emojize("⏪ Назад"), "t.back1." + str(folderid)), self.set_inline_btn(emojize("️🔄 Обновить"), "t.list." + str(teleid) + "." + str(folderid)))
        return self.markup


    def show_task_in_folder_for_edit(self, teleid, folderid):
        '''
        перечень задач в папке
        '''
        if not self.BD.is_folder_owner(folderid, teleid):
            friendid = teleid
            teleid = self.BD.find_teleid(self.BD.folder_owner(folderid))
        self.markup = InlineKeyboardMarkup(row_width=2)
        if bool(self.BD.select_all_tasks_from_folder(teleid, folderid)):
            print("del_all_task_in_bufer", self.BD.del_all_task_in_bufer(teleid))
            complete_task = []
            for el in self.BD.select_all_tasks_from_folder(teleid, folderid):
                if el[3]:
                    self.markup.add(self.set_inline_btn(emojize(el[0]) + " " + emojize(el[1]) + " ✏", "t.task." + str(el[2]) + "." + str(folderid)))
                else:
                    text = utility.strike(el[1])
                    complete_task.append([emojize("️✅ ") + emojize(el[0]) + text + " ✏", "t.task." + str(el[2]) + "." + str(folderid)])
            for el in complete_task:
                self.markup.add(self.set_inline_btn(el[0], el[1]))
        self.markup.add(self.set_inline_btn(emojize("⏪ Назад"), "f." + str(folderid)))
        return self.markup

    def show_task_in_shared_folder(self, friendid, folderid, ):
        '''
        перечень задач в папке
        '''
        self.markup = InlineKeyboardMarkup(row_width=2)
        if bool(self.BD.select_all_tasks_from_folder(friendid, folderid)):
            print("del_all_task_in_bufer", self.BD.del_all_task_in_bufer(friendid))
            complete_task = []
            for el in self.BD.select_all_tasks_from_folder(friendid, folderid):
                if el[3]:
                    self.markup.add(self.set_inline_btn(emojize(el[0]) + " " + emojize(el[1]) , "t.listshared." + str(el[2]) + "." + str(folderid)+ "." + str(folderid)))
                else:
                    text = utility.strike(el[1])
                    complete_task.append([emojize("️✅ ") + emojize(el[0]) + text, "t.listshared." + str(el[2]) + "." + str(folderid)])
            for el in complete_task:
                self.markup.add(self.set_inline_btn(el[0], el[1]))
        self.markup.row(self.set_inline_btn(emojize("⏪ Назад"), "t.back1."  + str(folderid)), self.set_inline_btn(emojize("⚪️ Выбрать"), "t.choise." + str(folderid)))
        return self.markup


    def show_task_edit_options(self, taskid):
        '''
        выводит опции редактирования задачи
        '''
        folderid = self.BD.task_location(taskid)
        self.markup = InlineKeyboardMarkup(row_width=3)
        self.markup.row(self.set_inline_btn(emojize("📝 Переименовать"), "t.rename."  + str(taskid)),
                        self.set_inline_btn(emojize("🌅 Значок"), "t.reicon."  + str(taskid)),
                        self.set_inline_btn(emojize("❌ Удалить"), "t.del."  + str(taskid)))
        self.markup.row(self.set_inline_btn(emojize("📤 Переместить"), "t.reloc."  + str(taskid)),
                        self.set_inline_btn(emojize("📣 Напоминание"), "t.remind."  + str(taskid)),
                        self.set_inline_btn(emojize("🗓 Событие"), "t.event."  + str(taskid)))
        self.markup.row(self.set_inline_btn(emojize("⬅️ Предыдущая"), "t.slide.l."  + str(taskid)),
                        self.set_inline_btn(emojize("➡️ Следующая"), "t.slide.r."  + str(taskid)))
        self.markup.add(self.set_inline_btn(emojize("⏪ Назад"), "f."  + str(folderid)))
        return self.markup



    def show_relocate_folder(self, idfolder, taskid, teleid):
        self.markup = InlineKeyboardMarkup(row_width=2)
        '''
        показать список папок для переноса
        '''
        if bool(self.BD.select_all_folders_from_user(teleid)):
            for el in self.BD.select_all_folders_from_user(teleid):
                if el[2] != idfolder:
                    self.markup.add(self.set_inline_btn(emojize(el[0]) + " " + emojize(el[1]), "t.relocdo." + str(taskid) + "." + str(el[2])))
        self.markup.add(self.set_inline_btn(emojize("⏪ Назад"), "t.task." + str(taskid)))
        return self.markup


    def show_task_for_choise(self, teleid, folderid):
        '''
        перечень задач в папке для выбора
        '''
        choise = self.BD.show_task_bufer(teleid)
        self.markup = InlineKeyboardMarkup(row_width=2)
        if not self.BD.is_folder_owner(folderid, teleid):
            teleid = self.BD.find_teleid(self.BD.folder_owner(folderid))
        alltask = self.BD.select_all_tasks_from_folder(teleid, folderid)
        if bool(alltask):
            complete_task = []
            for el in self.BD.select_all_tasks_from_folder(teleid, folderid):
                if el[2] not in choise and el[3]:
                    print("choise", choise, el[2])
                    self.markup.add(self.set_inline_btn("⚪️" + emojize(el[0]) + " " + emojize(el[1]), "t.choisetask." + str(el[2])))
                elif el[2] in choise and el[3]:
                    self.markup.add(self.set_inline_btn("🔘" + emojize(el[0]) + " " + emojize(el[1]), "t.choisetask." + str(el[2])))
                elif el[2] not in choise and not el[3]:
                    text = utility.strike(el[1])
                    complete_task.append(["⚪️️" + emojize(el[0]) + text, "t.choisetask." + str(el[2])])
                elif el[2] in choise and not el[3]:
                    text = utility.strike(el[1])
                    complete_task.append(["🔘" + emojize(el[0]) + " " + text, "t.choisetask." + str(el[2])])
            for el in complete_task:
                self.markup.add(self.set_inline_btn(el[0], el[1]))
        if len(choise) == len(alltask):
            text = "⚪️️ Снять выбор"
        else:
            text = "🔘 Выбрать все"
        self.markup.row(self.set_inline_btn(emojize("📤 Переместить"), "t.massreloc." + str(folderid)), self.set_inline_btn(emojize(text), "t.select." + str(folderid)), self.set_inline_btn(emojize("❌ Удалить"), "t.massdel." + str(folderid)))
        self.markup.add(self.set_inline_btn(emojize("⏪ Отмена"), "f." + str(folderid)))
        return self.markup

    def show_relocate_folder_mass(self, teleid, idfolder):
        '''
        Выбор папки для массового перемещения задач
        '''
        self.markup = InlineKeyboardMarkup(row_width=2)

        tasks = self.BD.show_task_bufer(teleid)
        if bool(tasks):
            for el in self.BD.select_all_folders_from_user(teleid):
                if el[2] != idfolder:
                    self.markup.add(self.set_inline_btn(emojize(el[0]) + " " + emojize(el[1]), "t.relocdomass." + str(el[2])))
        self.markup.add(self.set_inline_btn(emojize("⏪ Назад"), "f." + str(idfolder)))
        return self.markup

    #Работа с событиями
    def set_inline_events(self, teleid):
        '''
        Меню отображения списка событий
        '''
        self.markup = InlineKeyboardMarkup(row_width=2)
        events = self.BD.show_event_list(teleid)
        if events:
            for el in events:
                self.markup.add(self.set_inline_btn(el[2].strftime('%d.%m.%Y') + " " + emojize(el[0]) + " " + emojize(el[1]) , "e.list." + str(el[3])))
        self.markup.row(self.set_inline_btn(emojize("📋 Отчет"), "e.everyday_events"), self.set_inline_btn(emojize("⚪️ Выбрать"), "e.chouse"))
        self.markup.add(self.set_inline_btn(emojize("⏪ Назад"), "back"))
        return self.markup



    def event_edit(self, eventid, context):
        '''
        Меню отображения кнопок редактирования события
        '''

        self.markup = InlineKeyboardMarkup(row_width=3)
        self.markup.row(self.set_inline_btn(emojize("📝 Переименовать"), "e.rename."  + str(eventid)),
                        self.set_inline_btn(emojize("🌅 Значок"), "e.reicon."  + str(eventid)),
                        self.set_inline_btn(emojize("❌ Удалить"), "e.del."  + str(eventid)))
        self.markup.row(self.set_inline_btn(emojize("📆 Изменить дату"), "e.changedate."  + str(eventid)),
                        self.set_inline_btn(emojize("⏱ Изменить периодичность"), "e.period."  + str(eventid)),
                        self.set_inline_btn(emojize("⏰ Задать время"), "e.alarm."  + str(eventid)))
        self.markup.row(self.set_inline_btn(emojize("⬅️ Предыдущая"), "e.slide.l."  + str(eventid)),
                        self.set_inline_btn(emojize("➡️ Следующая"), "e.slide.r."  + str(eventid)))
        self.markup.add(self.set_inline_btn(emojize("⏪ Назад"), "e.back."  + str(context)))
        return self.markup





