import os
import time
import csv
import subprocess

def start_lan_test():
    
    print("===LAN Test===")
    
    target_ip =input('Please enter the  IP address: ')
    
    ping_test_result=subprocess.run([
    'ping', '-n', '4', f'{target_ip}'],
    capture_output=True,
    text=True,
    encoding='big5'
    
    )
 
    print(ping_test_result.stdout)#印出測試過程
    
    text=ping_test_result.stdout
    lost_text=text.split('已遺失 = ')[1].strip()[0]#將text分割成list，取列表的[1]=0
    print(lost_text)
    lost_number=int(lost_text)
    
    #判斷已遺失是不是=0
    if lost_number==0:
        print('Ping Test : Pass ')
        
    else:
        print('Ping Test : Fail')
        
        
    
    
    
    
   
    
    