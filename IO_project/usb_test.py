import subprocess
import time
import os
import csv

def start_usb_test():
  
  # 把檔案名稱存進 csv_file 變數
  csv_file = 'usb_test_results.csv'
  # 檢查 CSV 檔案是否存在，如果不存在則建立並寫入標題列
  file_exists = os.path.isfile(csv_file)
  
  with open(csv_file,mode='a',newline='',encoding='utf-8-sig') as f:
    # 建立 CSV 寫入器
    writer=csv.writer(f)
    # 如果 CSV 檔案不存在，寫入標題列
    if not file_exists:
      writer.writerow(['Drive','write Avg','read Avg','Result'])
  
  disk_number_result=subprocess.run(
    ['powershell',
    '-Command',
    '(Get-Disk | Where-Object {$_.BusType -eq "USB"}).Number'
],


                        #取得 Windows 的 PnP 裝置
                        # -PresentOnly 只顯示目前存在的裝置
                        # -Class USB 只顯示 USB 類別的裝置
    capture_output=True,#capture(抓取) output(輸出)PowerShell 的輸出抓回Python,
                        # True ：要!!開啟這個功能。
    text=True,          #抓回來的東西，我要用「文字」處理。
                        #PowerShell 的輸出被 Python 抓回來之後，可以用不同形式處理。在這裡我們用str輸出。
    encoding='big5'     #指定抓回來的文字編碼為 big5,正確解碼中文字
    )

#把disk_number_result    裡面的標準輸出 stdout，依照每一行切開，然後存進disk_numbers。
  disk_numbers = disk_number_result.stdout.splitlines()
  print(disk_numbers)
  for disk_number in disk_numbers:# 逐一取得每個 USB 的 Disk Number
      #print(usb_number)
      driveletter_command = f'(Get-Partition -DiskNumber {disk_number} | Get-Volume).DriveLetter'
      #print(driveletter_command)
      driveletter_result=subprocess.run(
        ['powershell',
         '-command',
         driveletter_command
         ],
        capture_output=True,
        text=True,
        encoding='big5'
        
      )
      #print(driveletter_result.stdout.strip())
      
      #切開後的字串，即取得的磁碟機代號
      driveletter=driveletter_result.stdout.strip()
      
      # 確認 USB 是否仍存在
      if driveletter == '':
          print('USB device not found')
          continue
      
      test_folder = f'{driveletter}:\\Test_folder'#第一個test是資料夾的路徑名稱，第二個test是資料夾的名稱
      os.makedirs(test_folder, exist_ok=True)#建立測試資料夾，如果已存在則不會報錯
      print('--'*20)
      print('Disk Number:',disk_number)
      print('Drive Letter:',driveletter)
      #print(f'{driveletter}:\\write_test.txt')
      
      #建立測試資料夾
      write_speeds=[]
      read_speeds=[]
      verify_results=[]
      
      # 同一支 USB 重複測試 3 次
      for test_number in range(3):
          print(test_number+1)
          
          
        
          try:
              file = open(f'{test_folder}\\write_test.txt', 'wb')
              test_data = b"A" * (20 * 1024 * 1024)

              start_time = time.perf_counter()

              file.write(test_data)
              file.close()

              end_time = time.perf_counter()
              elapsed_time = end_time - start_time#從寫到讀的花費時間

              write_speed=20/elapsed_time#MB/s = MB ÷ 秒
              write_speeds.append(write_speed)
              print(f'Write Elapsed Time : { elapsed_time:.6f}second')
              print(f'Write speed:{write_speed:.2f}MB/s')
          except IOError :
              print('Write test : Fail')
              
              continue  # 如果發生錯誤，跳過本次並接續下一次測試, 譬如第二次錯誤便跳過繼續第三次
    
          # 讀取測試開始時間
          read_start_time=time.perf_counter()
          try:
              #打開這支 USB 的test_folder的 write_test.txt
              read_file= open(f'{test_folder}\\write_test.txt',"rb")
              read_data=read_file.read()#把內容讀出來，存進 read_data
              read_file.close()
              read_end_time=time.perf_counter()
              
             

              read_elapsed_time=read_end_time-read_start_time
              read_speed=20/read_elapsed_time
              read_speeds.append(read_speed)
              print(f'read elapsed time : {read_elapsed_time:.6f}second')
              print(f'read speed:{read_speed:.2f}MB/s')
          except IOError:
              print('Read test : Fail')
              continue
            
          
          
          # 驗證讀取的資料是否與寫入的資料一致
          if test_data==read_data:
            print('Data Verify : PASS')
          else:
            print('Data Verify : FAIL')
            
          verify_results.append(test_data == read_data)
          
     
      if False in verify_results  or len(verify_results) != 3:
        print('Data Verify Overall : FAIL')
      else:
        print('Data Verify Overall : PASS')
        
      #確認write_speeds是否有缺資料       
      if len(write_speeds) !=3:
        print('Write Test : FAIL')
        print('ALL Tests : FAIL')
        
        continue
      
      #確認read_speeds是否是否有缺資料    
      if len(read_speeds) !=3:
        print('Read Test : FAIL')
        print('ALL Tests : FAIL')
        continue
            
      write_speed_min = min(write_speeds)
      write_speed_max = max(write_speeds)
      write_speed_avg = sum(write_speeds)/len(write_speeds)
      
      read_speed_min = min(read_speeds)
      read_speed_max = max(read_speeds)
      read_speed_avg = sum(read_speeds)/len(read_speeds)
      
      #print(write_speeds)
      #print(read_speeds)
      
      if(len(write_speeds)==3 
         and len(read_speeds)==3 
         and len(verify_results)==3 
         and False not in verify_results):
        result = 'PASS'
        print('All Tests : PASS')
      else:
        result = 'FAIL'
        print('All Tests : FAIL')

      print('**'*20)
      print(f'Write Speed Min: {write_speed_min:.2f}MB/s')
      print(f'Write Speed Max: {write_speed_max:.2f}MB/s')
      print(f'Write Speed Avg: {write_speed_avg:.2f}MB/s')

      print(f'Read Speed Min: {read_speed_min:.2f}MB/s')
      print(f'Read Speed Max: {read_speed_max:.2f}MB/s')
      print(f'Read Speed Avg: {read_speed_avg:.2f}MB/s')
      
      with open(csv_file,mode='a',newline='',encoding='utf-8-sig') as f:
         writer=csv.writer(f)
         writer.writerow([driveletter,write_speed_avg,read_speed_avg,result])
      
      
      
      

        


  return
      
    
  
  
