import datetime

from BaseStat import BaseStat


class OSProcess(BaseStat):

    def __init__(self):
        self.__pid = 0
        self.__name = ""
        self.__create_time = ""
        self.__status = ""
        self.__cpu_usage = 0.0
        self.__memory_usage = 0.0
        self.__serverId = -1
        self.__timestamp = ""

    def set_pid(self, pid):
        self.__pid = pid;

    def set_name(self, name):
        self.__name = name

    def set_create_time(self, create_time):
        self.__create_time = create_time

    def set_status(self, status):
        self.__status = status

    def set_cpu_usage(self, cpu_usage):
        self.__cpu_usage = cpu_usage

    def set_memory_usage(self, memory_usage):
        self.__memory_usage = memory_usage

    def set_server_id(self, server_id):
        self.__serverId = server_id

    def set_timestamp(self, timestamp):
        self.__timestamp = timestamp

    def __getstate__(self):
        state = {"pid": self.__pid,
                 "name":  self.__name,
                 "create_time": self.__create_time,
                 "status": self.__status,
                 "cpu_usage": self.__cpu_usage,
                 "memory_usage": self.__memory_usage,
                 "server_id": self.__serverId,
                 "timestamp": datetime.datetime.now()}
        return state
