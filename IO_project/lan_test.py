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
    
    lost_number=int(lost_text)
    
    #判斷已遺失是不是=0
    if lost_number==0:
        ping_status = 'Pass'
        print('Ping Test : Pass ')
        
    else:
        ping_status = 'Fail'
        print('Ping Test : Fail')
        
    test_time=time.strftime('%Y-%m-%d %H:%M:%S')
          
    with open('lan_test_log.csv',mode='a',newline='',encoding='utf-8-sig') as f:
        writer=csv.writer(f)#建立一個 CSV 寫入工具，讓它負責把資料寫進檔案 f
        writer.writerow([test_time,target_ip,lost_number,ping_status])
        
    os.path.exists('lan_test_log.csv')
        
        
    
    
    
    
   
    
    