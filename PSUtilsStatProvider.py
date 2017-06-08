from datetime import datetime

from BaseStatProvider import BaseStatProvider
import psutil

from OSProcess import OSProcess


class PSUtilStatProvider(BaseStatProvider):

    def __init__(self, config):
        self.__config = config

    def get_disk_data(self, disk_data):
        disk_stats = psutil.disk_usage("/");
        disk_data.set_total_disk_space(disk_stats.total)
        disk_data.set_used_disk_space(disk_stats.used)
        disk_data.set_free_disk_space(disk_stats.free)
        disk_data.set_perc_of_used_disk(disk_stats.percent)

    def get_memory_data(self, memory_data):
        mem = psutil.virtual_memory()
        memory_data.set_total_memory(mem.total)
        memory_data.set_used_memory(mem.used)
        memory_data.set_free_memory(mem.free)
        memory_data.set_usage_percent(mem.percent)

    def get_network_data(self, network_data):
        network = psutil.net_io_counters()
        network_data.set_bytes_sent(network.bytes_sent)
        network_data.set_bytes_recv(network.bytes_recv)
        network_data.set_packets_sent(network.packets_sent)
        network_data.set_packets_recv(network.packets_recv)

    def get_cpu_data(self, cpu_data):
        cpu_data.set_num_of_cores(psutil.cpu_count())
        cpu_data.set_usage(psutil.cpu_percent(interval=1, percpu=False))

    def get_process_list(self):
        process_list = []
        for proc in psutil.process_iter():
            try:
                process = OSProcess();
                process.set_cpu_usage(proc.cpu_percent())
                process.set_pid(proc.pid)
                process.set_create_time(proc.create_time())
                process.set_name(proc.name())
                process.set_memory_usage(proc.memory_percent())
                process.set_status(proc.status())
                process.set_server_id(self.__config.getServerId())
                process_list.append(process)
            except psutil.NoSuchProcess:
                pass
        return process_list

    def get_system_uptime(self):
        return datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")





