def show(cpu, mem, swap, load, uptime, disk, net, pids):
    print(f"{cpu[0]:<45} {cpu[4]:<70}") 
    print(f"{cpu[1]:<45} {cpu[5]:<70}")
    print(f"{cpu[2]:<45} {cpu[6]:<70}") 
    print(f"{cpu[3]:<45} {cpu[7]:<70}")
    print(f"{mem[0]:<45} {load[0]:<70}")
    print(f"{swap[0]:<45} {uptime[0]:<70}")
    disk_data = disk
    for i in disk_data:
        print(i)
    net_data = net
    for i in net_data:
        print(i)
    print(f"\n{'Pid':<6} {'User':<22} {'CPU%':<5} {'Mem,mb':<8} Name")
    data = pids
    for i in data:
        print(i)     
