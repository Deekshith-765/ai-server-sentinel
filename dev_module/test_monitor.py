"""Tests for the Dev Module system monitor."""

from system_monitor import SystemMonitor


def test_monitor_creates_snapshots():
    mon = SystemMonitor()
    snap = mon.collect_snapshot()
    assert "timestamp" in snap
    assert "cpu" in snap
    assert "memory" in snap
    assert "disk" in snap
    assert "network" in snap
    print("PASS: monitor creates valid snapshots")


def test_cpu_metrics():
    mon = SystemMonitor()
    cpu = mon.get_cpu()
    assert 0 <= cpu["percent"] <= 100
    assert cpu["cores"] >= 1
    print("PASS: CPU metrics in valid range")


def test_memory_metrics():
    mon = SystemMonitor()
    mem = mon.get_memory()
    assert 0 <= mem["percent"] <= 100
    assert mem["total_gb"] > 0
    print("PASS: Memory metrics in valid range")


def test_disk_metrics():
    mon = SystemMonitor()
    disk = mon.get_disk()
    assert 0 <= disk["percent"] <= 100
    assert disk["total_gb"] > 0
    print("PASS: Disk metrics in valid range")


def test_save_and_load():
    import json, os
    mon = SystemMonitor()
    mon.collect_snapshot()
    path = mon.save_json(filename="/tmp/test_metrics.json")
    assert os.path.exists(path)
    with open(path) as f:
        data = json.load(f)
    assert len(data) == 1
    os.remove(path)
    print("PASS: JSON save/load works")


if __name__ == "__main__":
    test_monitor_creates_snapshots()
    test_cpu_metrics()
    test_memory_metrics()
    test_disk_metrics()
    test_save_and_load()
    print("\nAll Dev Module tests passed!")
