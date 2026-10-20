import subprocess
from datetime import datetime
import time
import os

def start_usb_stress_test():
   
        disk_number_result = subprocess.run(
            ['powershell',
            '-Command',
            '(Get-Disk | Where-Object {$_.BusType -eq "USB"}).Number'
            ],#-eq = equal等於
            capture_output=True,
            text=True,
            encoding='big5'
        )
        
        disk_numbers = disk_number_result.stdout.splitlines()
        
        for disk_number in disk_numbers:
                print(f'USB Disk Number: {disk_number}')
                
                driveletter_command = f'(Get-Partition -DiskNumber {disk_number} | Get-Volume).DriveLetter'
                driveletter_result=subprocess.run(
                                ['powershell', '-command', driveletter_command],
                                capture_output=True,
                                text=True,
                                encoding='big5'
                                )
                driveletter=driveletter_result.stdout.strip()
                print(f'drive letter:{driveletter}:')
                print('--'*30)
                
                test_folder=f'{driveletter}:\\USB_Stress_Test_Log'
                os.makedirs(test_folder,exist_ok=True)#test_folder：指定要建立的資料夾,exist_ok=True：如果資料夾已經存在
                test_day=datetime.now().strftime('%Y%m%d_%H%M%S')
                testdata_1MB=f'{test_folder}\\testdata_1MB_{test_day}.bin'
                print(testdata_1MB)
                
                
                test_data=os.urandom(1024 * 1024) #產生指定大小的隨機位元組資料 1 MB in bytes
                print(len(test_data))
                
                with open(testdata_1MB,'xb') as f:#'xb'：以二進位模式建立新檔案，而且不會覆蓋已存在的同名檔案。
                    f.write(test_data)
                 
                  
                with open(testdata_1MB,'rb') as f:#'rb'：以二進位模式讀取檔案
                    read_data=f.read()#讀取檔案內容
                    
                
                    
            
        if not disk_numbers:#如果是空串列(沒有usb的話)
            print('No USB disk found')
            print('--'*30)
            
            return
        
        
            
        user_input_test_time=input('please enter the test time(minutes):')
        
        if  not user_input_test_time.isdigit() or int(user_input_test_time) <= 0:
            print('Invalid test duration')
        else:
            print(f'USB Stress Test Duration:{user_input_test_time} minutes')
            
            test_seconds = int(user_input_test_time) * 60 
            
            start_time=time.perf_counter()
            end_time=start_time + test_seconds
            
          
        #     while time.perf_counter() <= end_time:#現測試時間小於結束時間
        #         pass
            
    

            
        