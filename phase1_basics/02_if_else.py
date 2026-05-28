"""Phase 1: Python Basics - If/Else Decisions"""

cpu = 92
ram = 85
disk = 45

print("=" * 50)
print("SYSTEM HEALTH CHECK")
print("=" * 50)

if cpu > 90:
    print("CRITICAL: CPU usage is dangerously high!")
elif cpu > 70:
    print("WARNING: CPU usage is elevated.")
else:
    print("OK: CPU usage is normal.")

if ram > 90:
    print("CRITICAL: Running out of memory!")
elif ram > 75:
    print("WARNING: Memory usage is high.")
else:
    print("OK: Memory is healthy.")

if disk > 90:
    print("CRITICAL: Disk space almost full!")
elif disk > 75:
    print("WARNING: Disk space running low.")
else:
    print("OK: Disk space is sufficient.")

if cpu > 90 or ram > 90:
    print("\nACTION REQUIRED: Server is overloaded!")
else:
    print("\nAll systems nominal.")
