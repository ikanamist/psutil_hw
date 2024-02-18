import psutil
import time


def get_cpu():
    cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
    list_cpu = []
    for i, percentage in enumerate(cpu_usage):
        filler = int(int(percentage) / 100 * 20)
        a = (f"Загруженность ядра {i+1}:[{'|' * filler:<20}")
        if len(str(percentage)) == 3:
            a += (f" {percentage} %]")
        else:
            a += (f"{percentage} %]")
        list_cpu.append(a)
    return list_cpu


def get_memory():
    mem_usage = psutil.virtual_memory()
    total_memory = mem_usage.total / (1024**3)
    used_memory = mem_usage.used / (1024**3)
    memory = (f"Использование памяти: {used_memory:.2f}G/{total_memory:.2f}G")
    return memory


def get_swap():
    swap = psutil.swap_memory()
    total_swap = swap.total / (1024**3)
    used_swap = swap.used / (1024**3)
    swap_data = (f"Использование своп-пространства: {used_swap:.2f}G/{total_swap:.2f}G")
    return swap_data


def get_load():
    load1, load5, load15 = psutil.getloadavg()
    load = (f"Load average: {load1} {load5} {load15}")
    return load


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


def get_disk():
    disk_partit = psutil.disk_partitions()
    list_disk = []
    for partition in disk_partit:
        a = (f"Устройство: {partition.device}\n  Файловая система: {partition.fstype}")
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            a += (f"\n  Общий объем: {usage.total / (1024**3):.2f}G")
            a += (f"\n  Использовано: {usage.used / (1024**3):.2f}G")
            a += (f"\n  Свободно: {usage.free / (1024**3):.2f}G")
            a += (f"\n  Процент использования: {usage.percent}%")
        except PermissionError:
            a += ("Нет доступа к информации об использовании для этого раздела")
        a += ("\n")
        list_disk.append(a)
    return list_disk         


def get_net():
    net_io = psutil.net_io_counters(pernic=True)
    list_net = []
    for interface, stats in net_io.items():
        if stats.bytes_sent > 0 or stats.bytes_recv > 0:
            a = (f"Интерфейс: {interface}")
            a += (f"\n  Отправлено байт: {stats.bytes_sent / (1024**2):.2f}M")
            a += (f"\n  Получено байт: {stats.bytes_recv / (1024**2):.2f}M")
            a += (f"\n  Отправлено пакетов: {stats.packets_sent / (1024**2):.2f}M")
            a += (f"\n  Получено пакетов: {stats.packets_recv / (1024**2):.2f}M\n ")
            list_net.append(a)
    return list_net   


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
    print(f"{cpu[0]:<50} {cpu[4]:<80}") 
    print(f"{cpu[1]:<50} {cpu[5]:<80}")
    print(f"{cpu[2]:<50} {cpu[6]:<80}") 
    print(f"{cpu[3]:<50} {cpu[7]:<80}")
    print(f"{mem:<50} {load:<80}")
    print(f"{swap:<50} {uptime:<80}\n")
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
