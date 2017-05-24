from BaseStat import BaseStat


class CpuData(BaseStat):
    name = "CPU_UTILIZATION"

    def __init__(self):
        BaseStat.__init__(self)
        self.__usage = 0
        self.__num_of_cores = 0

    def get_usage(self):
        return self.__usage

    def get_num_of_cores(self):
        return self.__num_of_cores

    def set_num_of_cores(self, num_of_cores):
        self.__num_of_cores = num_of_cores

    def set_usage(self, usage):
        self.__usage = usage


    def __getstate__(self):
        state = {"usage": self.__usage,
                 "num_of_cores": self.__num_of_cores}
        return state





