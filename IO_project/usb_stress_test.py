import subprocess
from datetime import datetime
import time
import os
import csv

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
            
            
          
            while time.monotonic() <= end_time:#現測試時間小於結束時間
                
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
                
        with open('USB_Stress_Test_Result.csv', mode='w', encoding='utf-8') as f: 
            csv_writer = csv.writer(f)
            
            
            
            print('\n' + '=' * 45 + '\n')
            
    

            
        