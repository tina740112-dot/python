import platform#載入platform工具
##呼叫usb_test 進來
from usb_test import start_usb_test #從 usb_test.py 匯入 start_usb_test 函式
from lan_ping_test import start_lan_test #從 lan_test.py 匯入 start_lan_test 函式
from lan_ping_test import get_lan_adapter #從 lan_test.py 匯入 get_lan_adapter 函式
from lan_stress_test import start_lan_stress_test #從 lan_stress_test.py 匯入 start_lan_stress_test 函式
from system_info_test import start_system_info_test #從 system_info_test.py 匯入 start_system_info_test 函式



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
while True:
      try:
        print('1:USB Test\n'
              '2:LAN Ping Test\n'
              '3:LAN Stress Test\n'
              '4:System Hardware Overview')
 
        user=int(input('Please select option 1/2/3/4:'))
        print('**'*30)#空行分隔選單與輸入提示
        
        if user==1:
          print('USB Test Selected')
          start_usb_test()#呼叫usb_test
          
        elif user==2:
          print('LAN Ping Test Selected\n')
          lan_result = get_lan_adapter()#使用者取消，不執行 Ping
          if lan_result is not False:#繼續執行 Ping
            start_lan_test()#呼叫lan_test
          
        elif user==3:
          start_lan_stress_test()# 呼叫 LAN Stress Test 函式（假設函式名稱為 start_lan_stress_test）
          
        elif user==4:
          start_system_info_test()# 呼叫 System Hardware Overview 函式
          
        else:
          print('Invalid option')
          
      except ValueError:
        print('Invalid option')
      

  







  
