import subprocess
def start_usb_test():
  result=subprocess.run(
    ['powershell','-Command','get-date'],
    capture_output=True,
    #capture(抓取) output(輸出)PowerShell 的輸出抓回 Python,True 就是：要!!開啟這個功能。
    text=True#抓回來的東西，我要用「文字」處理。
    #PowerShell 的輸出被 Python 抓回來之後，可以用不同形式處理。在這裡我們用str輸出。
    )
  print('starting USB Test')
  print(result.stdout)
#start_usb_test()#呼叫並執行函式


#練習
# def show_name(name):
#   print('name:',name)
  
# show_name("amy")
