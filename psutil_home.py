import psutil
import time

""" get_file_str and get_file_list - decorators that write data to a file
decorated functions get data about my pc
last 2 functions show data in terminal """


def get_file_str(func):
    with open(f"{func.__name__}.txt", "a") as file:
        file.write(f"{func()} \n")
    return(func)


def get_file_list(func):
    list = func()
    data = []
    for i in list:
        data.append(i)
    with open(f"{func.__name__}.txt", "a") as file:
        file.write(f"{data} \n")
    return(func)


@get_file_list
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


@get_file_str
def get_memory():
    mem_usage = psutil.virtual_memory()
    total_memory = mem_usage.total / (1024**3)
    used_memory = mem_usage.used / (1024**3)
    memory = (f"Memory usage: {used_memory:.2f}G/{total_memory:.2f}G")
    return memory


@get_file_str
def get_swap():
    swap = psutil.swap_memory()
    total_swap = swap.total / (1024**3)
    used_swap = swap.used / (1024**3)
    swap_data = (f"Swap Usage: {used_swap:.2f}G/{total_swap:.2f}G")
    return swap_data


@get_file_str
def get_load():
    load1, load5, load15 = psutil.getloadavg()
    load = (f"Load average: {load1} {load5} {load15}")
    return load


@get_file_str
def get_uptime():
    boot_time = psutil.boot_time()
    current_time = time.time()
    uptime_seconds = current_time - boot_time
    uptime_days = uptime_seconds // (24*3600)
    uptime_hours = (uptime_seconds % (24*3600)) // 3600
    uptime_minutes = (uptime_seconds % 3600) // 60
    uptime_seconds = uptime_seconds % 60 
    uptime = (f"Uptime: {int(uptime_days)} days {int(uptime_hours)}:{int(uptime_minutes)}:{int(uptime_seconds)}")
    return uptime


@get_file_str
def get_disk():
    disk_partit = psutil.disk_partitions()
    list_disk = []
    for partition in disk_partit:
        a = (f"Device: {partition.device}\n  File system: {partition.fstype}")
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            a += (f"\n  Total memory: {usage.total / (1024**3):.2f}G")
            a += (f"\n  Used: {usage.used / (1024**3):.2f}G")
            a += (f"\n  Empty: {usage.free / (1024**3):.2f}G")
            a += (f"\n  Usage percent: {usage.percent}%")
        except PermissionError:
            a += ("No usage information available for this device")
        a += ("\n")
        list_disk.append(a)
    return list_disk         


@get_file_str
def get_net():
    net_io = psutil.net_io_counters(pernic=True)
    list_net = []
    for interface, stats in net_io.items():
        if stats.bytes_sent > 0 or stats.bytes_recv > 0:
            a = (f"Interface: {interface}")
            a += (f"\n  Bytes sent: {stats.bytes_sent / (1024**2):.2f}M")
            a += (f"\n  Bytes received: {stats.bytes_recv / (1024**2):.2f}M")
            a += (f"\n  Packages sent: {stats.packets_sent / (1024**2):.2f}M")
            a += (f"\n  Packages received: {stats.packets_recv / (1024**2):.2f}M\n ")
            list_net.append(a)
    return list_net   


@get_file_str
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


def show(cpu, mem, swap, load, uptime, pids):
    print(f"{cpu[0]:<45} {cpu[4]:<70}") 
    print(f"{cpu[1]:<45} {cpu[5]:<70}")
    print(f"{cpu[2]:<45} {cpu[6]:<70}") 
    print(f"{cpu[3]:<45} {cpu[7]:<70}")
    print(f"{mem:<45} {load:<70}")
    print(f"{swap:<45} {uptime:<70}\n")
    disk = get_disk()
    for i in disk:
        print(i)
    net = get_net()
    for i in net:
        print(i)
    print(f"{'Pid':<6} {'User':<22} {'CPU%':<5} {'Mem,mb':<8} Name")
    data = pids
    for i in data:
        print(i)     


def main():
    cpu_info = get_cpu()
    mem_info = get_memory()
    swap_info = get_swap()
    load_info = get_load()
    time_info = get_uptime()
    pids_info = get_pids()
    show(cpu_info, mem_info, swap_info, load_info, time_info, pids_info)


if __name__ == "__main__":
    main()
