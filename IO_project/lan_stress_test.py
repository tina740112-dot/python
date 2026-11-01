import time
from datetime import datetime
import subprocess
import json
import os
from app_paths import get_app_folder

def _run_iperf_round(ip, round_seconds):
    iperf_result = subprocess.run(
        ['iperf3', '-c', ip, '-t', str(round_seconds), '-J'],
        capture_output=True,
        text=True
    )
    try:
        result_json = json.loads(iperf_result.stdout)
        bits_per_second = result_json['end']['sum_received']['bits_per_second']
        return bits_per_second / 1_000_000
    except (json.JSONDecodeError, KeyError):
        return None

def start_lan_stress_test():
    ip1 = input("Please enter the first IP address to test: ")
    ip2 = input("Please enter the second IP address to test: ")
    test_minutes_input = int(input("Please enter the test duration in minutes: "))
    print('testing')
    minutes_to_seconds = test_minutes_input * 60
    round_seconds = 5
    start_now = time.time()
    end_time = start_now + minutes_to_seconds
    fail_count = {ip1: 0, ip2: 0}
    count = 0
    bitrates = {ip1: [], ip2: []}
    
    while time.time() < end_time:
        for ip in (ip1, ip2):
            mbps = _run_iperf_round(ip, round_seconds)
            if mbps is None:
                fail_count[ip] += 1
                bitrates[ip].append(None)
            else:
                bitrates[ip].append(mbps)
        count += 1
        print(f"Round {count} completed")
    
    successful_rounds = [v for v in bitrates[ip1] + bitrates[ip2] if v is not None]
    if not successful_rounds:
        print("All rounds failed. No data to report.")
        return
    
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _stats_block(ip):
        data = [v for v in bitrates[ip] if v is not None]
        if not data:
            return f"    target ip:{ip}\n    all rounds failed (fail count:{fail_count[ip]})\n"
        return (
            f"    target ip:{ip}\n"
            f"    min bitrate:{min(data):.2f} Mbps\n"
            f"    max bitrate:{max(data):.2f} Mbps\n"
            f"    avg bitrate:{sum(data)/len(data):.2f} Mbps\n"
            f"    fail count:{fail_count[ip]}\n"
        )
    
    LAN_stress_test = (
        f"LAN stress test report (iperf3 throughput):\n"
        f"    test time:{now_time}\n"
        f"    total rounds:{count}\n\n"
        f"{_stats_block(ip1)}\n"
        f"{_stats_block(ip2)}"
    )
    print(LAN_stress_test)
    
    report_filename = f"stress_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    report_path = os.path.join(get_app_folder(), report_filename)
    
    with open(report_path, mode='a', encoding='utf-8') as f:
        f.write(LAN_stress_test)