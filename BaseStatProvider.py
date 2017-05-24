from abc import abstractmethod


class BaseStatProvider:

    @abstractmethod
    def get_cpu_data(self, cpu_data):
        """not implemented error"""

    @abstractmethod
    def get_disk_data(self, disk_data):
        """not implemented error"""

    @abstractmethod
    def get_memory_data(self, memory_data):
         """not implemented error"""

    @abstractmethod
    def get_network_data(self, network_data):
        """not implemented error"""

    @abstractmethod
    def get_system_uptime(self, uptime):
        """not implemented error"""

    @abstractmethod
    def get_process_list(self):
        """not implemented error"""

