import subprocess
from datetime import datetime
import time
import os
import csv
import json
import platform
from concurrent.futures import ThreadPoolExecutor # 用於多線程執行 USB 壓力測試

def _start_usb_stress_test_windows():
   
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
        
        usb_disks = {}# 使用字典儲存 USB 磁碟的資訊
        
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
                
                usb_disks[disk_number] = driveletter# 將磁碟號與對應的磁碟機代號存入usb_disks字典
                
                print(f'drive letter:{driveletter}:')
          
              
                
                  
                
                    
            
        if not disk_numbers:#如果是空串列(沒有usb的話)
            print('No USB disk found')
            print('--'*30)
            
            return
        
        
         # 請使用者輸入測試時間(分鐘)
        user_input_test_time=input('please enter the test time(minutes):')
        
        print('--'*30)
        
        if  not user_input_test_time.isdigit() or int(user_input_test_time) <= 0:
            print('Invalid test duration')
        else:
            print(f'USB Stress Test Duration:{user_input_test_time} minutes')
            
            test_seconds = int(user_input_test_time) * 60 
            
            start_time=time.monotonic()#取得目前的計時數值。
            end_time=start_time + test_seconds
            
            round_count = 1# 記錄測試回合數
            pass_count = 0# 記錄通過的測試次數
            fail_count = 0# 記錄失敗的測試次數
            usb_results = {}# 記錄每個 USB 磁碟的測試結果
            
            
            def test_single_usb(disk_number, end_time):# 建立函式，接收 USB 編號和測試結束時間。測試單一 USB 磁碟的讀寫性能
          
                while time.monotonic() <= end_time:#現測試時間小於結束時間
                    print(f'Testing USB Disk {disk_number}')
                    driveletter = usb_disks[disk_number]#根據指定的 USB 磁碟編號，取得對應的磁碟機代號。
                
                    print(f'Round: {round_count}')
                
                    for disk_number in disk_numbers:
                        driveletter = usb_disks[disk_number]# 從字典中取得對應磁碟號的磁碟機代號
                        
                        
                        # 使用 setdefault() 方法，如果 usb_results 中沒有這個磁碟號，就建立預設值；如果已經有成績，就保留原本的數字。   
                        # usb_results 中的每個磁碟號都會有 'pass'、'fail' 以及 'write_speeds' 三個欄位，分別記錄通過次數、失敗次數和寫入速度列表。
                        usb_results.setdefault(disk_number,  {'pass': 0, 'fail': 0, 'write_speeds': [],'read_speeds': []})
                        #第一層：大字典 usb_results

                        #第二層：Disk1 的小字典 {}

                        #pass：0

                        #fail：0

                        #第三層：write_speeds → []
                        
                        testdata_1MB = None# 初始化測試檔案路徑變數，避免在 finally 區塊中出現未定義的錯誤
                        
                    # USB 讀寫測試
                    try:
                       
                        print('USB Stress Test Running')
                        print(f'Disk:{disk_number}-{driveletter}:')#顯示目前測試的磁碟號與磁碟機代號
                        time.sleep(1)  # 每次執行後暫停 1 秒。
                        #建立 USB 測試資料夾
                        test_folder=f'{driveletter}:\\USB_Stress_Test_Log'
                        os.makedirs(test_folder,exist_ok=True)#test_folder：指定要建立的資料夾,exist_ok=True：如果資料夾已經存在
                        test_day=datetime.now().strftime('%Y%m%d_%H%M%S')
                        
                        testdata_1MB=f'{test_folder}\\testdata_1MB_{test_day}_{round_count}.bin'
                        print(testdata_1MB)
                        
                        
                        test_data=os.urandom(1024 * 1024) #產生指定大小的隨機位元組資料 1 MB in bytes
                        #print(len(test_data))
                        
                        write_start=time.monotonic()# 記錄寫入開始的時間
                        
                        
                        # 寫入測試檔案
                        with open(testdata_1MB,'xb') as f:#'xb'：以二進位模式建立新檔案，而且不會覆蓋已存在的同名檔案。
                            f.write(test_data)
                            
                        write_end=time.monotonic()# 記錄寫入結束的時間
                        
                        write_duration=write_end-write_start# 計算寫入所花費的時間
                        
                        write_speed=1024*1024/write_duration# 計算寫入速度，單位為 bytes/s
                        
                        # 將bytes/second的寫入速度換算成 MB/s
                        write_speed_MB_s=write_speed/(1000*1000)
                         #先用 disk_number 找到該磁碟的 write_speeds 清單，再把 write_speed_MB_s 加到清單末端。
                        usb_results[disk_number]['write_speeds'].append(write_speed_MB_s)
                       
            
                        
                        
                        
                      
                        print(f'Write speed: {write_speed_MB_s:.3f} MB/second')#印出輸出速度
                        
                        print(f'Write duration: {write_duration:.3f} seconds')#印出輸出時間
                        
                        read_start = time.monotonic()# 記錄讀取開始的時間
                    
                        #讀取檔案:::確認寫入的資料跟讀取的資料是否正確
                        with open(testdata_1MB,'rb') as f:#'rb'：以二進位模式讀取檔案
                            read_data=f.read()#讀取檔案內容
                            
                        read_end = time.monotonic()# 記錄讀取結束的時間
                        read_duration = read_end - read_start# 計算讀取時間
                        read_speed_MB_s=(1024*1024/read_duration)/(1000*1000)# 計算讀取速度 MB/s)
                        # 將讀取速度加入目前 USB 的成績表
                        usb_results[disk_number]['read_speeds'].append(read_speed_MB_s)

                        if read_data == test_data:
                                print('Data verification passed')
                                pass_count += 1# 通過的測試次數加 1
                                usb_results[disk_number]['pass'] += 1#找到目前這支 USB 的成績表，把成功次數加 1
                        else:
                                print('Data verification failed')
                                fail_count += 1# 失敗的測試次數加 1
                                usb_results[disk_number]['fail'] += 1#找到目前這支 USB 的成績表，把失敗次數加 1
                               
                                
                        print(f'Read speed: {read_speed_MB_s:.3f} MB/second')#印出讀取速度
                        print(f'Read duration: {read_duration:.3f} seconds')#印出讀取時間
                        
                           
                    except OSError as error:
                            print(f'{error}')
                            fail_count += 1# 發生 OSError 時，失敗的測試次數加 1
                            usb_results[disk_number]['fail'] += 1#找到目前這支 USB 的成績表，把失敗次數加 1
                            
                    finally:
                        try:
                            if testdata_1MB is not None and os.path.exists(testdata_1MB):
                                
                                os.remove(testdata_1MB)# 刪除測試檔案
                                print('Test file removed')# 刪除測試檔案成功
                                
                        except OSError as error:
                            print(f'Cleanup failed: {error}')                    
                
                    
                 round_count = round_count + 1#每完成一輪所有 USB 的測試，回合數加 1
             
            print('--'*10+'USB Stress Test Finished'+'--'*10)
            
            total_tests=pass_count+fail_count# 計算總測試次數
            
            print('========== USB Stress Test Summary ==========')
            
            for disk_number,result in usb_results.items():#.items()同時取出字典的 key 和 value
                   driveletter = usb_disks[disk_number]# 取得目前 USB 的磁碟代號
                   print(f'Disk{disk_number}({driveletter}:)')# 顯示目前 USB 的磁碟代號
                   print(f'Passed:{result["pass"]}')# use key get USB 的成功次數並顯示
                   print(f'Failed:{result["fail"]}')# use key get USB 的失敗次數並顯示
                   if len(result['write_speeds'])>0:# 如果有寫入速度的紀錄，才顯示最小、最大和平均寫入速度
                       print(f'write speed min: {min(result["write_speeds"]):.3f} MB/s')# 顯示最小寫入速度
                       print(f'write speed max: {max(result["write_speeds"]):.3f} MB/s')# 顯示最大寫入速度
                       print(f'write speed avg: {sum(result["write_speeds"]) / len(result["write_speeds"]):.3f} MB/s')# 計算並顯示平均寫入速度
                   if len(result['read_speeds'])>0:# 如果有讀取速度的紀錄，才顯示最小、最大和平均讀取速度
                        print(f'read speed min: {min(result["read_speeds"]):.3f} MB/s')# 顯示最小讀取速度
                        print(f'read speed max: {max(result["read_speeds"]):.3f} MB/s')# 顯示最大讀取速度
                        print(f'read speed avg: {sum(result["read_speeds"]) / len(result["read_speeds"]):.3f} MB/s')# 計算並顯示平均讀取速度
            
            
            
            print(f'Total test: {total_tests}, Passed: {pass_count}, Failed: {fail_count}')# 顯示測試結果
            #最後判斷測試結果
            if fail_count == 0 and total_tests > 0:
                print('Result: PASS')
            else:
                print('Result: FAIL')
                
        csv_file_path = 'USB_Stress_Test_Result.csv'
        file_exists = os.path.exists(csv_file_path)
        
        with open(csv_file_path, mode='a', encoding='utf-8', newline='') as f: 
            csv_writer = csv.writer(f)
            if not file_exists:
                csv_writer.writerow(['Test Time','Disk','Total','Passed','Failed','Write Min','Write Max','Write Avg','Read Min','Read Max','Read Avg','Result'])

            for disk_number,result in usb_results.items():
                 driveletter=usb_disks[disk_number]
                
                 Total=result["pass"] + result["fail"]

                 Passed=result["pass"]

                 Failed=result["fail"]

                 test_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                 if len(result['write_speeds']) > 0:
                    Write_Min = min(result['write_speeds'])
                    Write_Max = max(result['write_speeds'])
                    Write_Avg = sum(result['write_speeds']) / len(result['write_speeds'])
                 else:
                    Write_Min = Write_Max = Write_Avg = 'N/A'

                 if len(result['read_speeds']) > 0:
                    Read_Min = min(result['read_speeds'])
                    Read_Max = max(result['read_speeds'])
                    Read_Avg = sum(result['read_speeds']) / len(result['read_speeds'])
                 else:
                    Read_Min = Read_Max = Read_Avg = 'N/A'

                 Result = 'PASS' if Failed == 0 and Total > 0 else 'FAIL'
                 
                 csv_writer.writerow([test_time, driveletter, Total, Passed, Failed, Write_Min, Write_Max, Write_Avg, Read_Min, Read_Max, Read_Avg, Result])
            
            print('\n' + '=' * 45 + '\n')


# Linux 使用 lsblk 偵測 USB 磁碟（不測試內建系統磁碟）
def _detect_usb_targets_linux():
    try:
        proc = subprocess.run(
            ['lsblk', '-J', '-o', 'NAME,TRAN,MODEL,MOUNTPOINT,TYPE'],
            capture_output=True, text=True, check=True
        )
        devices = json.loads(proc.stdout).get('blockdevices', [])
    except (FileNotFoundError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        print(f'Cannot detect Linux USB disks: {error}')
        return []

    targets = []

    def mounted_parts(device):
        # USB disks typically contain partition children. Handle nested structures as well.
        if device.get('mountpoint') and device.get('type') != 'disk':
            yield device
        for child in device.get('children') or []:
            yield from mounted_parts(child)

    for device in devices:
        if (device.get('tran') or '').lower() != 'usb':
            continue
        model = (device.get('model') or 'USB Disk').strip()
        parts = list(mounted_parts(device))
        # Some removable devices are formatted without a partition table.
        if not parts and device.get('mountpoint'):
            parts = [device]
        for part in parts:
            mountpoint = part.get('mountpoint')
            # Never target / or other system paths accidentally.
            if not mountpoint or mountpoint in ('/', '/boot', '/boot/efi'):
                continue
            if not os.path.isdir(mountpoint):
                continue
            targets.append((f"/dev/{part['name']}", mountpoint, model))
    return targets


def _start_usb_stress_test_linux():
    targets = _detect_usb_targets_linux()
    if not targets:
        print('No mounted USB storage disks found. Please mount the USB drive first.')
        return

    print('=== Linux USB Stress Test ===')
    for device, mountpoint, model in targets:
        print(f'{device} ({model}) -> {mountpoint}')

    # A write test changes the contents of a drive, so require explicit confirmation.
    if input('Test ALL listed USB drives? Type YES to continue: ').strip() != 'YES':
        print('USB Stress Test cancelled')
        return

    duration_text = input('Please enter the test time (minutes): ').strip()
    if not duration_text.isdigit() or int(duration_text) <= 0:
        print('Invalid test duration')
        return

    duration = int(duration_text) * 60
    deadline = time.monotonic() + duration
    results = {device: {'pass': 0, 'fail': 0, 'write_speeds': [], 'read_speeds': []}
               for device, _, _ in targets}
    count = 0

    while time.monotonic() < deadline:
        count += 1
        print(f'Round: {count}')
        for device, mountpoint, model in targets:
            # Create the test file ONLY inside the USB mountpoint.
            folder = os.path.join(mountpoint, 'USB_Stress_Test_Log')
            file_path = None
            print(f'USB: {device} -> {mountpoint}')
            try:
                os.makedirs(folder, exist_ok=True)
                filename = f"testdata_1MB_{datetime.now():%Y%m%d_%H%M%S_%f}_{count}.bin"
                file_path = os.path.join(folder, filename)
                test_data = os.urandom(1024 * 1024)

                write_start = time.monotonic()
                with open(file_path, 'xb') as f:
                    f.write(test_data)
                    f.flush()
                    os.fsync(f.fileno())  # Reduce misleading write-cache measurements.
                write_duration = max(time.monotonic() - write_start, 1e-9)
                write_speed = (len(test_data) / 1_000_000) / write_duration
                results[device]['write_speeds'].append(write_speed)

                read_start = time.monotonic()
                with open(file_path, 'rb') as f:
                    read_data = f.read()
                read_duration = max(time.monotonic() - read_start, 1e-9)
                read_speed = (len(read_data) / 1_000_000) / read_duration
                results[device]['read_speeds'].append(read_speed)

                correct = read_data == test_data
                results[device]['pass' if correct else 'fail'] += 1
                print(f'Write speed: {write_speed:.3f} MB/s')
                print(f'Read speed:  {read_speed:.3f} MB/s')
                print(f'Data verification: {"PASS" if correct else "FAIL"}')
            except OSError as error:
                results[device]['fail'] += 1
                print(f'USB read/write test failed: {error}')
            finally:
                if file_path and os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                        print('Test file removed')
                    except OSError as error:
                        results[device]['fail'] += 1
                        print(f'Cleanup failed: {error}')

    print('========== USB Stress Test Summary ==========')
    report = 'USB_Stress_Test_Result.csv'
    file_exists = os.path.isfile(report) and os.path.getsize(report) > 0
    with open(report, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Test Time', 'Disk', 'Total', 'Passed', 'Failed',
                             'Write Min', 'Write Max', 'Write Avg',
                             'Read Min', 'Read Max', 'Read Avg', 'Result'])

        def speed_stats(values):
            if not values:
                return ('N/A', 'N/A', 'N/A')
            return (f'{min(values):.3f}', f'{max(values):.3f}',
                    f'{sum(values) / len(values):.3f}')

        for device, mountpoint, model in targets:
            outcome = results[device]
            passed, failed = outcome['pass'], outcome['fail']
            total = passed + failed
            write_min, write_max, write_avg = speed_stats(outcome['write_speeds'])
            read_min, read_max, read_avg = speed_stats(outcome['read_speeds'])
            status = 'PASS' if total > 0 and failed == 0 else 'FAIL'
            print(f'{device} ({mountpoint})  Total:{total} Passed:{passed} Failed:{failed}  Result:{status}')
            print(f'  Write Min/Max/Avg: {write_min}/{write_max}/{write_avg} MB/s')
            print(f'  Read  Min/Max/Avg: {read_min}/{read_max}/{read_avg} MB/s')
            writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                             f'{device} ({mountpoint})', total, passed, failed,
                             write_min, write_max, write_avg,
                             read_min, read_max, read_avg, status])
    print(f'CSV report saved: {os.path.abspath(report)}')
    print('Note: Linux read speeds may be inflated by the OS page cache.')


def start_usb_stress_test():
    # Keep main.py unchanged: it calls this function on both platforms.
    system = platform.system()
    if system == 'Windows':
        return _start_usb_stress_test_windows()
    if system == 'Linux':
        return _start_usb_stress_test_linux()
    print(f'Unsupported system: {system}')
