
from BaseStat import BaseStat


class NetworkStats(BaseStat):

    def __init__(self):
        BaseStat.__init__(self)
        self.__bytes_sent = 0
        self.__bytes_recv = 0
        self.__packets_sent = 0
        self.__packets_recv = 0

    def set_bytes_sent(self, bytes_sent):
        self.__bytes_sent = bytes_sent

    def set_bytes_recv(self, bytes_recv):
        self.__bytes_recv = bytes_recv

    def set_packets_sent(self, packets_sent):
        self.__packets_sent = packets_sent

    def set_packets_recv(self, packets_recv):
        self.__packets_recv = packets_recv

    def get_threshhold_value(self):
        return 0

    def __getstate__(self):
        state = {"bytes_sent": self.__bytes_sent,
                 "bytes_recv":  self.__bytes_recv,
                 "packets_sent": self.__packets_sent,
                 "packets_recv": self.__packets_recv}
        return state