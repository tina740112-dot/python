import subprocess
def start_usb_test():
  result=subprocess.run(
    ['powershell','-Command','get-date']
    capture_output=true,
    text=true
    )
print('starting USB Test')

#start_usb_test()#呼叫函式


