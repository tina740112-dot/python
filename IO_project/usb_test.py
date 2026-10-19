import subprocess
import time
import os
import csv
import json
import platform
from datetime import datetime
from app_paths import get_app_folder

IS_WINDOWS = platform.system() == 'Windows'

def _detect_usb_targets_windows(): #用PowerShell列出USB隨身碟，回傳[(usbname, 'D:\\'), ...]
  targets = []
  disk_number_result=subprocess.run(
    ['powershell',
    '-Command',
    '(Get-Disk | Where-Object {$_.BusType -eq "USB"}).Number'
],
    capture_output=True,
    text=True,
    encoding='big5'     #指定抓回來的文字編碼為 big5,正確解碼中文字
    )

  disk_numbers = disk_number_result.stdout.splitlines()

  for disk_number in disk_numbers:
      usbname_command = f'(Get-Disk -Number {disk_number}).FriendlyName'
      usbname_result=subprocess.run(
        ['powershell', '-Command', usbname_command],
        capture_output=True,
        text=True,
        encoding='big5'
      )
      usbname=usbname_result.stdout.strip()

      driveletter_command = f'(Get-Partition -DiskNumber {disk_number} | Get-Volume).DriveLetter'
      driveletter_result=subprocess.run(
        ['powershell', '-command', driveletter_command],
        capture_output=True,
        text=True,
        encoding='big5'
      )
      driveletter=driveletter_result.stdout.strip()

      if driveletter == '':
          print('USB device not found')
          continue

      targets.append((usbname, f'{driveletter}:\\'))
  return targets

def _detect_usb_targets_linux(): #用lsblk找出USB隨身碟及掛載點，回傳[(usbname, mountpoint), ...]
  targets = []
  lsblk_result = subprocess.run(
    ['lsblk', '-J', '-o', 'NAME,TRAN,MODEL,MOUNTPOINT,TYPE'],
    capture_output=True,
    text=True
  )
  try:
    data = json.loads(lsblk_result.stdout)
  except json.JSONDecodeError:
    return targets

  for device in data.get('blockdevices', []):
    if device.get('tran') != 'usb':
      continue
    usbname = (device.get('model') or 'USB Device').strip()
    partitions = device.get('children') or [device] #沒有分割區時，裝置本身就是掛載點
    for part in partitions:
      mountpoint = part.get('mountpoint')
      if mountpoint:
        targets.append((usbname, mountpoint))

  if not targets:
    print('USB device found but not mounted. Please mount the USB drive first.')
  return targets

def start_usb_test():

  #取得程式（或打包後的exe）實際所在的資料夾
  app_folder = get_app_folder()

  #join把資料夾路徑和檔案名稱組合成一個完整路徑。
  log_folder = os.path.join(app_folder, 'Logs')

  #組合資料夾或檔案路徑
  os.makedirs(log_folder, exist_ok=True)

  #join把建立測試資料夾資料夾路徑和檔案名稱組合成一個完整路徑。
  csv_file = os.path.join(log_folder, 'usb_test_results.csv')

  # 檢查 CSV 檔案是否存在，如果不存在則建立並寫入標題列
  file_exists = os.path.isfile(csv_file)

  with open(csv_file,mode='a',newline='',encoding='utf-8-sig') as f:
    # 建立 CSV 寫入器
    writer=csv.writer(f)
    # 如果 CSV 檔案不存在，寫入標題列
    if not file_exists:
      writer.writerow(['Test Time','USB Name','Drive','write Avg','read Avg','Result'])

  usb_targets = _detect_usb_targets_windows() if IS_WINDOWS else _detect_usb_targets_linux()

  if not usb_targets:
      print('No USB disks found')
      print('Please insert a USB drive.')
      return

  # 逐一測試每個偵測到的 USB 裝置
  for usbname, driveletter in usb_targets:
      print('--'*20)
      print('USB Name:',usbname)

      test_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

      test_folder = os.path.join(driveletter, 'Test_folder')
      try:
        os.makedirs(test_folder, exist_ok=True)#建立測試資料夾，如果已存在則不會報錯
      except OSError:
         print('Create Test Folder : FAIL')

         with open(csv_file,mode='a',newline='',encoding='utf-8-sig') as f:
          writer=csv.writer(f)
          writer.writerow([test_time,usbname,driveletter,'','','FAIL'])
          continue


      print('Drive:',driveletter)
      
      #建立測試資料夾
      write_speeds=[]
      read_speeds=[]
      verify_results=[]
      
      # 同一支 USB 重複測試 3 次
      for test_number in range(3):
          print(test_number+1)
          
          
        
          try:
              file = open(os.path.join(test_folder, 'write_test.txt'), 'wb')
              test_data = b"A" * (20 * 1024 * 1024)

              # 開始寫入測試的時間
              write_start_time = time.perf_counter()

              file.write(test_data)
              file.flush()  # 把 Python 的寫入緩衝資料送給作業系統。
              os.fsync(file.fileno())  # 要求作業系統同步檔案資料到儲存裝置。
              file.close()

              end_time = time.perf_counter()
              elapsed_time = end_time - write_start_time#從寫到讀的花費時間

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
              read_file= open(os.path.join(test_folder, 'write_test.txt'),"rb")
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

        with open(csv_file,mode='a',newline='',encoding='utf-8-sig')as f:
           writer=csv.writer(f)
           writer.writerow([test_time,usbname,driveletter,'','','FAIL'])

        test_file=os.path.join(test_folder,'write_test.txt')

        try:
           if os.path.isfile(test_file):
              os.remove(test_file)
        except OSError:
           print('Cleanup Test File:Fail')
        
        continue
      
      #確認read_speeds是否是否有缺資料    
      if len(read_speeds) !=3:
        print('Read Test : FAIL')
        print('ALL Tests : FAIL')
        with open(csv_file,mode='a',newline='',encoding='utf-8-sig')as f:
           writer=csv.writer(f)
           writer.writerow([test_time,usbname,driveletter,'','','FAIL'])
        # 清理 USB 測試檔案
        test_file = os.path.join(test_folder, 'write_test.txt')

        try:
            if os.path.isfile(test_file):
                os.remove(test_file)
        except OSError:
            print('Cleanup Test File : FAIL')

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
         writer.writerow([test_time,usbname,driveletter,f'{write_speed_avg:.2f}',f'{read_speed_avg:.2f}',result])

      # 刪除本次 USB 測試產生的檔案
      #join把資料夾路徑和檔案名稱組合成一個完整路徑。
      test_file = os.path.join(test_folder, 'write_test.txt')

      #確認檔案存在
      if os.path.isfile(test_file):
              #真正刪除檔案
              os.remove(test_file)
                
      
      
      

        


  return
      
    
  
  
