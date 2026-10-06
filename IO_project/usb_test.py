import subprocess
import time
def start_usb_test():
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


  disk_numbers = disk_number_result.stdout.splitlines()#把disk_number_result    裡面的標準輸出 stdout，依照每一行切開，然後存進disk_numbers。
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
      driveletter=driveletter_result.stdout.strip()
      print('--'*20)
      print('Disk Number:',disk_number)
      print('Drive Letter:',driveletter)
      #print(f'{driveletter}:\\write_test.txt')

      write_speeds=[]
      for test_number in range(3):# 同一支 USB 重複測試 3 次
          print(test_number+1)

        
          try:
              file = open(f'{driveletter}:\\write_test.txt', 'wb')
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
          except IOError:
              print('Write test : Fail')
    

          read_start_time=time.perf_counter()
          read_file= open(f'{driveletter}:\\write_test.txt',"rb")#打開這支 USB 的 write_test.txt
          read_data=read_file.read()#把內容讀出來，存進 read_data
          read_file.close()
          read_end_time=time.perf_counter()

          read_elapsed_time=read_end_time-read_start_time
          read_speed=20/read_elapsed_time
          print(f'read elapsed time : {read_elapsed_time:.6f}second')
          print(f'read speed:{read_speed:.2f}MB/s')

          if test_data==read_data:
            print('Data Verify : PASS')
          else:
            
            print('Data Verify : FAIL')
          write_speed_min = min(write_speeds)
          write_speed_max = max(write_speeds)
          write_speed_avg = sum(write_speeds)/len(write_speeds)
          

      print(write_speeds)
      print(f'Write Speed Min: {write_speed_min:.2f}MB/s')
      print(f'Write Speed Max: {write_speed_max:.2f}MB/s')
      print(f'Write Speed Avg: {write_speed_avg:.2f}MB/s')

        


  return
      
    
  
  
#######write test#############
  write_speeds=[]
  read_speeds=[]
 
  for i in range(3):  # 進行三次測試
    try:
      file=open(f'{driveletter_result.stdout.strip()}:\\write_test.txt','wb')#開啟/建立write_test.txt檔案
      test_data=b'A'*(20*1024*1024) # ① 先準備 20 MB
      start_time =time.perf_counter() # ② 效能計數器開始計時 
                                    #()=呼叫計數器=碼表功能，取得開始寫入檔案的效能計時器數值
      file.write(test_data)# ③ 寫入 20 MB內容寫變數test data
      file.close()#檔案關閉
      end_time = time.perf_counter()# ④ 結束計時
                                    #()=呼叫計數器=碼表功能，取得結束寫入檔案的效能計時器數值
      elapsed_time = end_time - start_time   # ⑤ 算經過時間
      write_speed = 20/elapsed_time# ⑥ 計算寫入速度
      write_speeds.append(write_speed)
      print('Write Test : PASS')
      print(f'Write Elapsed Time: {elapsed_time:.6f} seconds')
      print(f'Write Speed: {write_speed:.2f}MB/s')
    
    except IOError:
      print('Write Test : Fail')

  ########read test#########

    try:
      file=open(f'{driveletter_result.stdout.strip()}:\\write_test.txt','rb')
      read_start_time =time.perf_counter()
      read_data=file.read()# 把檔案內容讀出來
      file.close()
      read_end_time =time.perf_counter()
      print('Read Test : Pass')
      read_elapsed_time = read_end_time-read_start_time
      read_speed=20/read_elapsed_time
      read_speeds.append(read_speed)
      print(f'Read Elapsed Time : {read_elapsed_time:.6f}seconds')
      print(f'Read Speed : {read_speed:.2f}MB/s')
      
    except IOError as error:
      print('Read test : Fail')
      print(error)
########### Verify test:Check if read and write data are the same
    if read_data == test_data :
      print('Verify test : Pass')
    else:
      print('Verify test : Fail')

  print(write_speeds)
  print(read_speeds)



  
  
  
  

    
      
    

  
#練習
# def show_name(name):
#   print('name:',name)
  
# show_name("amy")
