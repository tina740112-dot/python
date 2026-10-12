import platform#載入platform工具
##呼叫usb_test 進來
from usb_test import start_usb_test #從 usb_test.py 匯入 start_usb_test 函式
from lan_test import start_lan_test #從 lan_test.py 匯入 start_lan_test 函式



print("===Peripheral Test Tool===")
#platform.system()platform的system確認作業系統
os_name=platform.system()#取得作業系統名稱並存入 os_name
print(os_name)

if os_name =="Windows":
  print('Windows System Detected')
elif os_name=='Linux':
  print('Linux System Detected')
else:
  print('Unsupported System')
################ test list#######################
try:
  print('1:USB Test\n'
        '2:LAN Test')
  user=int(input('Please select option 1/2:'))
  if user==1:
    #print('Starting USB Test')
    start_usb_test()#呼叫usb_test
  elif user==2:
    start_lan_test()#呼叫lan_test
  else:
    print('Invalid option')
except ValueError:
  print('Invalid option')
  







  
