import subprocess
from datetime import datetime
import time

def start_usb_stress_test():
    user_input_test_time=input('please enter the test time(minutes):')
    
    if  not user_input_test_time.isdigit() or int(user_input_test_time) <= 0:
        print('Invalid test duration')
    else:
        print(f'USB Stress Test Duration:{user_input_test_time} minutes')
        
        test_seconds = int(user_input_test_time) * 60 
        
        start_time=time.perf_counter()
        end_time=start_time + test_seconds
        
        while time.perf_counter() <= end_time:#現測試時間小於結束時間
            pass
        
        disk_number_result = subprocess.run(
            ['powershell',
            '-Command',
            '(Get-Disk | Where-Object {$_.BusType -eq "USB"}).Number'
            ],#-eq = equal等於
            capture_output=True,
            text=True,
            encoding='big5'
        )
        
        print(disk_number_result.stdout)