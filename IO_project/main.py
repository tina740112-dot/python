import platform#載入platform工具
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
#usb test
try:
  user=int(input('Please select usb option 1/2:'))
  if user==1:
    print('Starting USB Test')
  elif user==2:
    print('Exit')
  else:
    print('Invalid option')
except ValueError:
  print('Invalid option')
    
  
