"""Phase 1: Python Basics - Functions"""

def check_cpu(usage):
    if usage > 90:
        return "CRITICAL"
    elif usage > 70:
        return "WARNING"
    return "OK"

def check_memory(used_gb, total_gb):
    percent = (used_gb / total_gb) * 100
    status = check_cpu(percent)
    return status, percent

def get_system_summary(name, cpu, ram, disk):
    return {
        "server": name,
        "cpu_status": check_cpu(cpu),
        "ram_status": check_cpu(ram),
        "disk_status": check_cpu(disk),
        "overall": "HEALTHY" if all(check_cpu(x) == "OK" for x in (cpu, ram, disk)) else "ISSUES DETECTED"
    }

cpu = 45
ram = 72
disk = 30
server = "db-server-02"

status, ram_pct = check_memory(14.5, 16)
print(f"Memory: {ram_pct:.1f}% - {status}")

summary = get_system_summary(server, cpu, ram, disk)
print("\nSystem Summary:")
for key, value in summary.items():
    print(f"  {key}: {value}")
