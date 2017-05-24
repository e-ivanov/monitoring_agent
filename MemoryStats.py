from BaseStat import BaseStat


class MemoryStats(BaseStat):
    def __init__(self):
        BaseStat.__init__(self)
        self.__total = 0
        self.__used = 0
        self.__free = 0
        self.__usage_percent = 0

    def get_total_memory(self):
        return self.__total

    def get_used_memory(self):
        return self.__used

    def get_usage_percent(self):
        return self.__usage_percent

    def get_free_memory(self):
        return self.__free

    def set_total_memory(self, total_memory):
        self.__total = total_memory

    def set_used_memory(self, used_memory):
        self.__used = used_memory

    def set_free_memory(self, free_memory):
        self.__free = free_memory

    def set_usage_percent(self, usage_percent):
        self.__usage_percent = usage_percent

    def get_threshhold_value(self):
        return 0

    def __getstate__(self):
        state = {"total": self.__total,
                 "used":  self.__used,
                 "free": self.__free,
                 "usage_percent": self.__usage_percent}
        return state
