import subprocess
def start_usb_test():
  before_result=subprocess.run(
    ['powershell','-Command','get-PnpDevice -PresentOnly -Class USB'],
    #取得 Windows 的 PnP 裝置
    # -PresentOnly 只顯示目前存在的裝置
    # -Class USB 只顯示 USB 類別的裝置
    capture_output=True,
    #capture(抓取) output(輸出)PowerShell 的輸出抓回 Python,
    # True ：要!!開啟這個功能。
    text=True,#抓回來的東西，我要用「文字」處理。
    #PowerShell 的輸出被 Python 抓回來之後，可以用不同形式處理。在這裡我們用str輸出。
    encoding='big5'#指定抓回來的文字編碼為 big5,正確解碼中文字
    )
####Wait usb connection

  print('starting USB Test')
  print(before_result.stdout)#現在把抓回來的正常輸出拿出來
  #stdout=standard output
  input('please insert USB Device ,then press enter')

#start_usb_test()#呼叫並執行函式


#練習
# def show_name(name):
#   print('name:',name)
  
# show_name("amy")
