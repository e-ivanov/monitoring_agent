from BaseStat import BaseStat


class DiskStats(BaseStat):

    def __init__(self):
        BaseStat.__init__(self)
        self.__total_disk_space = 0
        self.__used_disk_space = 0
        self.__free_disk_space = 0
        self.__perc_of_used_disk = 0

    def set_total_disk_space(self, total_disk_space):
        self.__total_disk_space = total_disk_space

    def set_used_disk_space(self, used_disk_space):
        self.__used_disk_space = used_disk_space

    def set_free_disk_space(self, free_disk_space):
        self.__free_disk_space = free_disk_space

    def set_perc_of_used_disk(self, perc_of_used_disk):
        self.__perc_of_used_disk = perc_of_used_disk

    def get_threshhold_value(self):
        return 0

    def __getstate__(self):
        state = {"total_disk_space": self.__total_disk_space,
                 "used_disk_space":  self.__used_disk_space,
                 "free_disk_space": self.__free_disk_space,
                 "perc_of_used_disk": self.__perc_of_used_disk}
        return state