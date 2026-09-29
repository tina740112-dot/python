import subprocess
import time
def start_usb_test():
  ##############第一次確認未插入usb的狀況##########################
  before_result=subprocess.run(
    ['powershell',
    '-Command',
    '(Get-PnpDevice -PresentOnly -Class USB).InstanceId'
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

  before_lines = before_result.stdout.splitlines()  #把 before_result 裡面的標準輸出 stdout，依照每一行切開，然後存                                                 進before_lines。
  
  #for item in before_lines:先不要顯示每一行的 InstanceId因為太長，所以註解掉
    #if 'InstanceId' in item:
    #  print(item)
    
  before_ids=set(before_lines)
  print('before:',before_ids) #將 before_lines 轉換成 set
  
  print('Starting first USB Test')
  print(before_result.stdout)                      #現在把抓回來的值正常輸出拿出來
                                                   #stdout=standard output

 ##################Wait usb connection############################# 
  input('please insert USB Device ,then press enter')#執行第二次usb測試，要插入USB裝置
  
#################執行第二次usb裝置連接#######################
  after_result=subprocess.run(#第二次插入usb狀況
    ['powershell',
    '-Command',
    '(Get-PnpDevice -PresentOnly -Class USB).InstanceId'
    ],
    capture_output=True,
    text=True,
    encoding='big5'
  )
  after_lines = after_result.stdout.splitlines()  #把 after_result 裡面的標準輸出 stdout，依照每一行切開，然後存                                                 進after_lines。
  
  after_ids=set(after_lines)
  print('after:',after_ids)
    
  print('starting second USB Test')
  print(after_result.stdout)#現在把抓回來的正常輸出拿出來
  #stdout=standard output
  #start_usb_test()#呼叫並執行函式
  
###########before and after 差集並印出新的 USB 裝置連接###########
  new_ids=after_ids-before_ids
  print(new_ids)
  
  
  if new_ids:        #new_ids 是不是有新的 USB 裝置
    print("New USB device detected")
    for new_usb in new_ids:
      print("New USB device detected:", new_usb)
      command = f'Get-PnpDevice -InstanceId "{new_usb}"'

      device_result = subprocess.run(
              ['powershell','-command',command],
              capture_output=True,
          
              text=True,
              encoding='big5'            
      )
      print(device_result.stdout)

  else:
    print("no New USB")
    
  disk_command = 'Get-Disk | Where-Object {$_.BusType -eq "USB"} | Format-List FriendlyName,BusType,SerialNumber,Size'
                              #使用 PowerShell 指令取得目前所有 USB 磁碟裝置
  disk_result = subprocess.run(
          ['powershell',
          '-Command',
          disk_command
          ],
          capture_output=True,
          text=True,
          encoding='big5'
        )
  print(disk_result.stdout)
  
  disk_lines=disk_result.stdout.splitlines()  #把 disk_result 裡面的標準輸出 stdout，依照每一行切開，然後存進 disk_lines。
  
  print(disk_lines)
  
  for item in disk_lines:
    if'FriendlyName'in item:
      print(item)
      
  for item1 in disk_lines:
      if'Size'in item1:
        #print(item1)
        #print(item1.split(':'))
        
        usb_size=item1.split(':')[1].strip()
       #print(usb_size)
        
        usb_size=int(usb_size)
        print(f'USB Size:{usb_size/(1024**3):.2f}GB')

 ########顯示裝置是什麼槽       
  driveletter_command='(Get-Disk | Where-Object {$_.BusType -eq "USB"} | Get-Partition | Get-Volume).DriveLetter'
  
  driveletter_result=subprocess.run(
    ['powershell',
    '-command',
    driveletter_command
    ],
    capture_output=True,        #把結果抓回來
    text=True,                  #我要文字
    encoding='big5'             #這個文字用 Big5規則解讀
    
  )
  print(f'Drive letter : {driveletter_result.stdout.strip()}:')

  ###############裝置的位置  
  location_command = "(Get-PnpDeviceProperty -InstanceId 'USB\\VID_125F&PID_DD1A\\2572306450170002' -KeyName 'DEVPKEY_Device_LocationInfo').Data"
  
  location_result=subprocess.run(
    ['powershell',
     '-command',
     location_command
     ],

    capture_output=True,
    text=True,
    encoding='big5'

  )
  print(location_result.stdout.strip())
  
#######write test#############
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
    print('Write Test : PASS')
    print(f'Write Elapsed Time: {elapsed_time:.6f} seconds')
    print(f'Write Speed: {write_speed:.2f}MB/s') # 
    
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




  
  
  
  

    
      
    

  
#練習
# def show_name(name):
#   print('name:',name)
  
# show_name("amy")
