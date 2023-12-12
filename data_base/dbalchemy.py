from os import path
from datetime import datetime
from datetime import timedelta

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, joinedload
from data_base.dbcore import Base

from settings import config
from models.users import Users
from models.events import Events
from models.settings import Settings
from models.inbox import Inbox
from models.folders import Folders
from models.tasks import Tasks
from models.bufertask import Bufertask
from settings import utility


class Singleton(type):
    """
    Патерн Singleton предоставляет механизм создания одного
    и только одного объекта класса,
    и предоставление к нему глобальной точки доступа.
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class DBManager(metaclass=Singleton):
    """
    Класс-менеджер для работы с БД
    """

    def __init__(self):
        """
        Инициализация сессии и подключения к БД
        """
        self.engine = create_engine(config.DATABASE)
        session = sessionmaker(bind=self.engine)
        self._session = session()
        if not path.isfile(config.DATABASE):
            Base.metadata.create_all(self.engine)

    def close(self):
        """
        Закрывает сесию
        """
        self._session.close()

    def add_inbox(self, msg, teleid):
        userid = self.select_user_id(teleid)
        userinbox = Inbox(date=datetime.now(), message=msg, user_id=userid, is_active = True)
        self._session.add(userinbox)
        self._session.commit()
        self.close()

    def add_url_inbox(self, msg, teleid):
        userid = self.select_user_id(teleid)
        userinbox = Inbox(date=datetime.now(), message=msg, url = msg, user_id=userid, is_active = True)
        self._session.add(userinbox)
        self._session.commit()
        result = userinbox.id
        self.close()
        return result

    def inbox_rename(self, teleid, name, inboxid):
        userid = self.select_user_id(teleid)
        try:
            inbox_holder = self._session.query(Inbox.user_id).filter_by(
                id=inboxid).one()
            if inbox_holder == userid:
                self._session.query(Inbox).filter_by(
                    id=inboxid).update({Inbox.message: name})
                return True
            else:
                pass
        except:
            return False

    def change_inbox_active(self, inboxid):
        try:
            inbox_active = self._session.query(Inbox.is_active).filter_by(
                id=inboxid).one()
            if inbox_active[0]:
                self._session.query(Inbox).filter_by(
                    id=inboxid).update({Inbox.is_active: False})
            else:
                self._session.query(Inbox).filter_by(
                    id=inboxid).update({Inbox.is_active: True})
            self._session.commit()
            self.close()
            return True
        except:
            return False

    def select_all_inbox_by_user(self, teleid):
        userid = self.select_user_id(teleid)
        if bool(self.find_inbox(userid)):
            result = self._session.query(Inbox.message, Inbox.id, Inbox.is_active).filter_by(
                user_id=userid).all()
            self.close()
            print(result)
            return result
        else:
            return False

    def del_inbox_task(self, teleid, incomeid):
        userid = self.select_user_id(teleid)
        if bool(self.user_owner_inbox(userid, incomeid)):
            self._session.query(Inbox).filter_by(id=incomeid).delete()
            self._session.commit()
            self.close()

    def user_owner_inbox(self, userid, incomeid):
        result = self._session.query(Inbox).filter_by(
            user_id=userid).filter_by(id=incomeid).all()
        self.close()
        return result

    def get_inbox_name(self, inboxid):
        try:
            result = self._session.query(Inbox.message).filter_by(
            id=inboxid).one()
            self.close()
            return result[0]
        except:
            return False

    def migrate_inbox_to_folder(self, teleid, idfolder):
        pass



    # Работа с папками

    def select_all_folders_from_user(self, teleid):
        userid = self.select_user_id(teleid)
        result = self._session.query(Folders.icon, Folders.name, Folders.id, Folders.friend).filter_by(
            user_id=userid).all()
        self.close()
        print(result)
        return result

    def add_foldername(self, name, teleid):
        userid = self.select_user_id(teleid)
        try:
            new_folder = Folders(date=datetime.now(), name=name, id_type=1, is_active=True, icon="📂", user_id=userid)
            self._session.add(new_folder)
            self._session.commit()
            result = new_folder.id
            print("id folder = ", result)
            self.close()
            return result
        except:
            return False

    def rename_folder(self, newname, fid, teleid):
        userid = self.select_user_id(teleid)
        if bool(self.find_folder(fid, userid)):
            try:
                self._session.query(Folders).filter_by(
                    id=fid).update({Folders.name: newname})
                self._session.commit()
                self.close()
                return True
            except:
                pass
        return False

    def add_emoji(self, icon, fid, teleid):
        userid = self.select_user_id(teleid)
        oldfoldericon = self.find_folder(fid, userid)
        if bool(oldfoldericon):
            try:
                self._session.query(Folders).filter_by(
                    id=fid).update({Folders.icon: icon})
                self._session.commit()
                self.close()
                return oldfoldericon
            except:
                pass
        return False

    def del_folder(self, teleid, incomeid):
        userid = self.select_user_id(teleid)
        if bool(self.find_folder(incomeid, userid)):
            self._session.query(Folders).filter_by(id=incomeid).delete()
            self._session.commit()
            self.close()

    def if_teg(self, idfolder):
        try:
            result = self._session.query(Folders.teg).filter_by(
            id=idfolder).one()
            self.close()
            print(result[0])
            return result[0]
        except:
            return False

    def add_teg(self, idfolder, teg):
        try:
            self._session.query(Folders).filter_by(
                        id=idfolder).update({Folders.teg: teg})
            self._session.commit()
            self.close()
            return True
        except:
            return False

    def find_teg(self, teg, teleid):
        userid = self.select_user_id(teleid)
        try:
            result = self._session.query(Folders.id).filter_by(
            teg=teg, user_id = userid).one()
            self.close()
            print(result[0])
            return result[0]
        except:
            return False

    def is_already_share(self, idfolder):
        try:
            result = self._session.query(Folders.friend, Folders.access_lvl).filter_by(
            id=idfolder).one()
            self.close()
            print(result)
            return result
        except:
            pass
        return False

    def share_folder(self, idfolder, teleid):
        '''
        Принимает на вход id пользователя и папки, которую нужно для него расшарить
        Расшаривает папку для пользователя и возвращает статус операции
        '''
        try:
            self._session.query(Folders).filter_by(
                        id=idfolder).update({Folders.friend: teleid, Folders.access_lvl: 1})
            self._session.commit()
            self.close()
            return True
        except:
            pass
        return False

    def folder_owner(self, idfolder):
        try:
            result = self._session.query(Folders.user_id).filter_by(
            id=idfolder).one()
            self.close()
            print(result)
            return result[0]
        except:
            pass
        return False

    def is_folder_owner(self, idfolder, teleid):
        userid = self.select_user_id(teleid)
        print("teleid", teleid, "userid", userid)
        if userid and userid == self.folder_owner(idfolder):
            print("is_folder_owner", userid, self.folder_owner(idfolder))
            return True
        else:
            return False

    def access_lvl(self, idfolder, teleid):
        friend = self.is_already_share(idfolder)
        if friend and friend[0] == teleid:
            return friend[1]
        else:
            return False

    def change_access_lvl(self, idfolder, teleid, lvl):
        friend = self.is_already_share(idfolder)
        if friend:
            try:
                self._session.query(Folders).filter_by(
                        id=idfolder).update({Folders.access_lvl: lvl})
                self._session.commit()
                self.close()
                return friend[0]
            except:
                pass
        return False

    def cancel_access(self, idfolder):
        friend = self.is_already_share(idfolder)
        if friend:
            try:
                self._session.query(Folders).filter_by(
                        id=idfolder).update({Folders.friend: None, Folders.access_lvl: None})
                self._session.commit()
                self.close()
                return friend[0]
            except:
                pass
        return False







    # Работа с задачами

    def select_all_tasks_from_folder(self, teleid, folderid):
        userid = self.select_user_id(teleid)
        if bool(self.find_folder(folderid, userid)):
            result = self._session.query(Tasks.icon, Tasks.name, Tasks.id, Tasks.is_active, Tasks.date).filter_by(
                folder_id=folderid).order_by(desc(Tasks.last_touch)).all()
            self.close()
            print(result)
            return result

    def add_task(self, name, idfolder, teleid):
        userid = self.select_user_id(teleid)
        if bool(self.find_folder(idfolder, userid)):
            new_task = Tasks(date=datetime.now(), is_active=True, last_touch=datetime.now(), icon="🗓", name=name,
                             folder_id=idfolder)
            try:
                self._session.add(new_task)
                self._session.commit()
                result = new_task.id
                self.close()
                return result
            except:
                pass
        return False

    def change_complite_task(self, taskid):
        try:
            task_status = self._session.query(Tasks.is_active).filter_by(id=taskid).one()
            print("task_status", task_status)
            if task_status[0]:
                try:
                    self._session.query(Tasks).filter_by(
                        id=taskid).update({Tasks.is_active: False, Tasks.last_touch: datetime.now()})
                    self._session.commit()
                    self.close()
                    return True
                except:
                    pass
            else:
                try:
                    self._session.query(Tasks).filter_by(
                        id=taskid).update({Tasks.is_active: True, Tasks.last_touch: datetime.now()})
                    self._session.commit()
                    self.close()
                    return True
                except:
                    pass
        except:
            pass
        return False

    def task_location(self, idtask):
        try:
            result = self._session.query(Tasks.folder_id).filter_by(
                id=idtask).one()
            self.close()
        except:
            return False
        return result[0]

    def task_name(self, idtask):
        try:
            result = self._session.query(Tasks.icon, Tasks.name).filter_by(
                id=idtask).one()
            self.close()
        except:
            return False
        return result

    def task_rename(self, idtask, newname):
        try:
            oldtname = self.task_name(idtask)
            self._session.query(Tasks).filter_by(
                id=idtask).update({Tasks.name: newname})
            self._session.commit()
            self.close()
            return oldtname
        except:
            return False

    def task_icon(self, idtask, icon):
        try:
            oldicon = self.task_name(idtask)
            self._session.query(Tasks).filter_by(id=idtask).update({Tasks.icon: icon})
            self._session.commit()
            self.close()
            return oldicon
        except:
            return False

    def task_del(self, idtask):
        try:
            taskinfo = self.task_name(idtask)
            self._session.query(Tasks).filter_by(id=idtask).delete()
            self._session.commit()
            self.close()
            return taskinfo
        except:
            return False

    def change_task_location(self, idtask, target_f):
        try:
            self._session.query(Tasks).filter_by(id=idtask).update({Tasks.folder_id: target_f})
            self._session.commit()
            self.close()
            return True
        except:
            return False

    def add_task_bufer(self, taskid, teleid):
            userid = self.select_user_id(teleid)
            new_bufer_task = Bufertask(date=datetime.now(), task_id = taskid, user_id = userid)
            try:
                self._session.add(new_bufer_task)
                self._session.commit()
                result = new_bufer_task.id
                self.close()
                return result
            except:
                return False

    def show_task_bufer(self, teleid):
        userid = self.select_user_id(teleid)
        result = self._session.query(Bufertask.task_id).filter_by(user_id=userid).all()
        self.close()
        return utility._convert(result)

    def del_task_from_bufer(self, taskid, teleid):
        bufer = self.show_task_bufer(teleid)
        if taskid in bufer:
            try:
                self._session.query(Bufertask).filter_by(task_id=taskid).delete()
                self._session.commit()
                self.close()
                return True
            except:
                return False
        return False

    def del_all_task_in_bufer(self, teleid):
        userid = self.select_user_id(teleid)
        try:
            self._session.query(Bufertask).filter_by(user_id=userid).delete()
            self._session.commit()
            self.close()
            return True
        except:
            return False




    def users_count(self):
        result = self._session.query(Users.id).count()
        self.close()
        return result

    def select_all_user_id(self):
        result = self._session.query(Users.id).all()
        self.close()
        return result

    def select_user_id(self, user):
        """
        Возвращает id пользователя в БД или создает нового.
        """
        if self.find_user(user):
            result = self._session.query(
                Users.id).filter_by(teleid=user).one()
            self.close()
        else:
            self.add_user("User" + str(user)[:4], user)
            result = self._session.query(
                Users.id).filter_by(teleid=user).one()
            self.close()
        return result.id

    def add_user(self, name, teleid):
        '''
        Добавляет нового игрока в БД
        '''
        user = Users(name=name, teleid=teleid, is_activ=1)
        self._session.add(user)
        self._session.commit()
        self.close()

    def update_user_name(self, uname, teleid):
        """
        Обновляет имя указанного пользователя
        """
        self._session.query(Users).filter_by(
            teleid=teleid).update({Users.name: uname})
        self._session.commit()
        self.close()

    def find_user(self, tid):
        '''
        Ищет игрока, прикладная функция для других методов
        '''
        result = self._session.query(Users).filter_by(
            teleid=tid).all()
        self.close()
        return result

    def find_inbox(self, userid):
        '''
        Ищет у пользователя папку "входящие"
        '''
        try:
            result = self._session.query(Inbox).filter_by(
                user_id=userid).all()
            self.close()
            return result
        except:
            return False

    # def find_folders(self, userid):
    #     '''
    #     Ищет у пользователя папки
    #     '''
    #     result = self._session.query(Folders).filter_by(
    #         user_id=userid).all()
    #     self.close()
    #     return result

    def find_settings(self, userid):
        '''
        Ищет настройки игрока, прикладная функция для других методов
        '''
        result = self._session.query(Settings).filter_by(
            user_id=userid).all()
        self.close()
        return result

    def find_user_name(self, teleid):
        '''
        ищет имя пользователя
        '''
        result = self._session.query(Users.name).filter_by(teleid=teleid).one()
        self.close()
        return result

    def find_folder(self, fid, iduser):
        '''
        ищет папку у пользователя и возращает ее имя
        '''
        try:
            result = self._session.query(Folders.icon, Folders.name, Folders.teg, Folders.friend, Folders.access_lvl).filter_by(id=fid).filter_by(user_id=iduser).one()
            self.close()
            print(result)
            return result
        except:
            pass
        return False

    def show_share_folder(self, teleid):
        try:
            result = self._session.query(Folders.icon, Folders.name, Folders.id, Folders.user_id).filter_by(friend=teleid).all()
            self.close()
            print(result)
            return result
        except:
            pass
        return False

    def find_teleid(self, userid):
        try:
            result = self._session.query(Users.teleid).filter_by(id=userid).one()
            self.close()
            print(result)
            return result[0]
        except:
            pass
        return False

    #События

    def show_event_list(self, teleid):
        try:
            userid = self.select_user_id(teleid)
            result = self._session.query(Events.icon, Events.name, Events.date, Events.id).filter_by(user_id=userid).order_by(Events.date).all()
            self.close()
            print(result)
            return result
        except:
            pass
        return False
    def show_event_info(self, idevent):
        try:
            result = self._session.query(Events.icon, Events.name, Events.date, Events.id).filter_by(id=idevent).one()
            self.close()
            print(result)
            return result
        except:
            pass
        return False

    def add_new_event(self, name, date, teleid, icon=""):
        userid = self.select_user_id(teleid)

        new_event = Events(date=date, create_at=datetime.now(), period=1, icon=icon, name=name,
                             user_id=userid)
        try:
            self._session.add(new_event)
            self._session.commit()
            result = new_event.id
            self.close()
            return result
        except:
            pass
        return False

    def event_rename(self, idevent, newname):
        try:
            oldname = self._session.query(Events.name).filter_by(id=idevent).one()
            self.close()
            self._session.query(Events).filter_by(
                id=idevent).update({Events.name: newname})
            self._session.commit()
            self.close()
            return oldname[0]
        except:
            return False

    def add_event_emoji(self, icon, idevent):
        try:
            oldicon= self._session.query(Events.icon).filter_by(id=idevent).one()
        except:
            oldicon= False
        print(oldicon)
        try:
            self._session.query(Events).filter_by(
                    id=idevent).update({Events.icon: icon})
            self._session.commit()
            self.close()
            return oldicon[0]
        except:
            pass
        return False




    def update_user_timer(self, teleid):
        '''
        Показывает сколько времени прошло между активностью пользователя/ обновляет счетчик
        '''
        time = datetime.now()
        print(time)
        try:
                userid = self.select_user_id(teleid)
                oldtime = self._session.query(Users.last_login).filter_by(id=userid).one()
                self.close()
        except:
                oldtime = time
        try:
            self._session.query(Users).filter_by(
            teleid=teleid).update({Users.last_login: time})
            self._session.commit()
            self.close()
            return (time - oldtime[0])
        except:
            return 0





    def add_utc(self, teleid, value):
        userid = self.select_user_id(teleid)
        self.make_settings(teleid)
        self._session.query(Settings).filter_by(
            user_id=userid).update({Settings.utc: value})
        self.close()
