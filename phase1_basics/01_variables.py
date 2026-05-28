"""Phase 1: Python Basics - Variables & Data Types"""

cpu_percent = 75.5
ram_total_gb = 16
ram_used_gb = 10.2
disk_free_gb = 120
server_name = "web-server-01"
is_online = True
active_connections = 42

print("=" * 50)
print("SYSTEM STATUS VARIABLES")
print("=" * 50)
print(f"Server: {server_name}")
print(f"CPU Usage: {cpu_percent}%")
print(f"RAM: {ram_used_gb}/{ram_total_gb} GB used")
print(f"Disk Free: {disk_free_gb} GB")
print(f"Online: {is_online}")
print(f"Active Connections: {active_connections}")

total_ram_percent = (ram_used_gb / ram_total_gb) * 100
print(f"\nRAM Usage Percentage: {total_ram_percent:.1f}%")
