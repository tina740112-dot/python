import subprocess
import time
def start_usb_test():
  ##############第一次確認未插入usb的狀況##########################
  before_result=subprocess.run(#Python 叫外部程式subprocess.run去做事。
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
  time.sleep(3) #等待 3 秒，讓使用者有時間插入 USB 裝置
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
  
  
  if new_ids:                       #new_ids 是不是有新的 USB 裝置
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

##############################抓出 USB 磁碟的磁碟代號 (Drive Letter)##########################
        
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

  #############################顯示 USB 磁碟的磁碟代號 (Drive Letter)##########################
    
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

  print(f'Location Info:{location_result.stdout.strip()}')

  ############################寫入測試並存檔##########################
  #print(open(f'{driveletter_result.stdout.strip()}:\\write_test.txt',"w"))#先測試確定檔案可以寫入
  file=open(f'{driveletter_result.stdout.strip()}:\\write_test.txt',"w")#開啟/建立檔案
  file.write('test write')# 寫資料
  file.close() # 關閉檔案

  try:
    file=open(f'{driveletter_result.stdout.strip()}:\\write_test.txt',"w")#開啟/建立檔案
    file.write('test write')# 寫資料
    file.close() # 關閉檔案
    print('Write test : Pass')
  except IOError:             
    print("Write Test : FAIL")

  ###################讀取測試檔案內容##########################

  file=open(f'{driveletter_result.stdout.strip()}:\\write_test.txt',"r")# 打開 USB 裡的檔案
  read_data=file.read()#把 file 裡面的內容讀出來，存進 read_data。
  file.close() #檔案用完，關掉
  #print(read_data) #把剛才讀到的內容顯示給我看

  try:
    file=open(f'{driveletter_result.stdout.strip()}:\\write_test.txt',"r")# 打開 USB 裡的檔案
    read_data=file.read()#把 file 裡面的內容讀出來，存進 read_data。
    file.close() #檔案用完，關掉
    print("Read Test : PASS")  #讀取成功
  except IOError:
    print("Read Test : FAIL")
##############讀取出來的資料跟寫入的資料進行驗證##########################
  if read_data=='test write':
    print("Data Verify Test : PASS")
  else:
    print("Data Verify Test : FAIL")

#############測試讀取寫入速度##########################
  
  

    
      
    

  
#練習
# def show_name(name):
#   print('name:',name)
  
# show_name("amy")
