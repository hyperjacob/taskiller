import datetime

class Logger:
    file_name = ""
    last_event = ""
    def write_log(self, log):
        if self.file_name != ("log_" + str(datetime.datetime.now().day) +"."+ str(datetime.datetime.now().month) + "." + str(datetime.datetime.now().year)[-2:]):
            self.file_name = "log_" + str(datetime.datetime.now().day) +"."+ str(datetime.datetime.now().month) + "." + str(datetime.datetime.now().year)[-2:]
        self.last_event = "["+str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)+"] "+ log + "\n"
        with open("./"+self.file_name, "a", encoding="UTF-8") as f:
            f.write(self.last_event)

    def clear_log(self):
        file_name = "log_" + str(datetime.datetime.now().day) +"."+ str(datetime.datetime.now().month) + "." + str(datetime.datetime.now().year)[-2:]
        with open("./"+file_name, "w", encoding="UTF-8") as f:
            f.write("")

    def get_logs(self):
        file_name = "log_" + str(datetime.datetime.now().day) +"."+ str(datetime.datetime.now().month) + "." + str(datetime.datetime.now().year)[-2:]
        get_log = []
        with open("./"+file_name, "r", encoding="UTF-8") as f:
           for list in f:
               get_log.append(list[:-1])
        return get_log


    def get_last_event(self):
        return self.last_event
