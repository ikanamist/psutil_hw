import psutil
import time
from textwrap import dedent
import decorator as dec

@dec.get_file()
def get_cpu():
    cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
    list_cpu = []
    for i, percentage in enumerate(cpu_usage):
        filler = int(int(percentage) / 100 * 20)
        a = (f"Core usage {i+1}:[{'|' * filler:<20}")
        if len(str(percentage)) == 3:
            a += (f" {percentage} %]")
        else:
            a += (f"{percentage} %]")
        list_cpu.append(a)
    return list_cpu


@dec.get_file()
def get_memory():
    memory = []
    mem_usage = psutil.virtual_memory()
    total_memory = mem_usage.total / (1024**3)
    used_memory = mem_usage.used / (1024**3)
    memory.append(f"Memory usage: {used_memory:.2f}G/{total_memory:.2f}G")
    return memory


@dec.get_file()
def get_swap():
    swap_data =[]
    swap = psutil.swap_memory()
    total_swap = swap.total / (1024**3)
    used_swap = swap.used / (1024**3)
    swap_data.append(f"Swap Usage: {used_swap:.2f}G/{total_swap:.2f}G")
    return swap_data


@dec.get_file()
def get_load():
    load =[]
    load1, load5, load15 = psutil.getloadavg()
    load.append(f"Load average: {load1} {load5} {load15}")
    return load


@dec.get_file()
def get_uptime():
    uptime = []
    boot_time = psutil.boot_time()
    current_time = time.time()
    uptime_seconds = current_time - boot_time
    uptime_days = uptime_seconds // (24*3600)
    uptime_hours = (uptime_seconds % (24*3600)) // 3600
    uptime_minutes = (uptime_seconds % 3600) // 60
    uptime_seconds = uptime_seconds % 60 
    uptime.append(f"Uptime: {int(uptime_days)} days {int(uptime_hours)}:{int(uptime_minutes)}:{int(uptime_seconds)}")
    return uptime


@dec.get_file()
def get_disk():
    disk_partit = psutil.disk_partitions()
    list_disk = []
    for partition in disk_partit:
        a = dedent(f"""
             Device: {partition.device}
             File system: {partition.fstype}""")
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            a += dedent(f"""
                        Total memory: {usage.total / (1024**3):.2f}G
                        Used: {usage.used / (1024**3):.2f}G
                        Empty: {usage.free / (1024**3):.2f}G
                        Usage percent: {usage.percent}%""")
        except PermissionError:
            a += ("No usage information available for this device")
        list_disk.append(a)
    return list_disk         


@dec.get_file()
def get_net():
    net_io = psutil.net_io_counters(pernic=True)
    list_net = []
    for interface, stats in net_io.items():
        if stats.bytes_sent > 0 or stats.bytes_recv > 0:
            a = dedent(f"""
                        Interface: {interface}
                        Bytes sent: {stats.bytes_sent / (1024**2):.2f}M
                        Bytes received: {stats.bytes_recv / (1024**2):.2f}M
                        Packages sent: {stats.packets_sent / (1024**2):.2f}M
                        Packages received: {stats.packets_recv / (1024**2):.2f}M """)
            list_net.append(a)
    return list_net   


@dec.get_file()
def get_pids():
    pids_list = []
    for pid in psutil.pids():
        try:
            p = psutil.Process(pid)
            a = (f"{pid:<6} {p.username():<22} {p.cpu_percent():<5} {p.memory_info().rss / (1024**2):<8.2f} {p.name()}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
        pids_list.append(a)
    return pids_list