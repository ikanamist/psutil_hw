import get_data as gd
import show

def main():
    cpu_info = gd.get_cpu()
    mem_info = gd.get_memory()
    swap_info = gd.get_swap()
    load_info = gd.get_load()
    time_info = gd.get_uptime()
    disk_info = gd.get_disk()
    net_info = gd.get_net()
    pids_info = gd.get_pids()
    show.show(cpu_info, mem_info, swap_info, load_info, time_info, disk_info, net_info, pids_info)


if __name__ == "__main__":
    main()