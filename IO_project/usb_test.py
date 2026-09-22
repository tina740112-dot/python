import subprocess
def start_usb_test():
  ##############第一次確認未插入usb的狀況##########################
  before_result=subprocess.run(
    ['powershell',
    '-Command',
    '(Get-PnpDevice -PresentOnly -Class USB ).InstanceId'
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
  
  #for item in before_lines:
    #if 'InstanceId' in item:
    #  print(item)
    

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
  print('starting second USB Test')
  print(after_result.stdout)#現在把抓回來的正常輸出拿出來
  #stdout=standard output
  #start_usb_test()#呼叫並執行函式


#練習
# def show_name(name):
#   print('name:',name)
  
# show_name("amy")
