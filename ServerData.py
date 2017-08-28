from CpuData import CpuData
from DiskStats import DiskStats
from MemoryStats import MemoryStats
from NetworkStats import NetworkStats
import datetime, uuid


class ServerData:
    def __init__(self, stat_provider, config):
        self.__serverId = config.get("server_id", "serverid")
        self.__stat_provider = stat_provider
        self.__processList = []
        self.__memoryData = MemoryStats()
        self.__cpuData = CpuData()
        self.__diskData = DiskStats()
        self.__networkData = NetworkStats()
        self.__system_uptime = 0
        self.__timestamp = 0
        self.__uuid = ''

    def get_process_list(self):
        return self.__processList

    def get_cpu_data(self):
        return self.__cpuData

    def get_memory_data(self):
        return self.__memoryData

    def get_disk_data(self):
        return self.__diskData

    def get_network_data(self):
        return self.__networkData

    def get_uuid(self):
        return self.__uuid

    def refreshData(self):
        self.__stat_provider.get_cpu_data(self.__cpuData)
        self.__stat_provider.get_disk_data(self.__diskData)
        self.__stat_provider.get_memory_data(self.__memoryData)
        self.__stat_provider.get_network_data(self.__networkData)
        self.__system_uptime = self.__stat_provider.get_system_uptime()
        self.__processList = self.__stat_provider.get_process_list()
        self.__timestamp = datetime.datetime.now()
        self.__uuid = str(uuid.uuid4())

    def __getstate__(self):
        state = {"serverId": self.__serverId,
                 "memoryData": self.__memoryData,
                 "cpuData": self.__cpuData,
                 "diskData": self.__diskData,
                 "networkData": self.__networkData,
                 "system_uptime": self.__system_uptime,
                 "processList": self.__processList,
                 "timestamp": self.__timestamp,
                 "uuid": self.__uuid}
        return state

    def publish(self):
        pass
