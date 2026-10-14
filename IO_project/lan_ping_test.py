import os
import time
import csv
import subprocess

def get_lan_adapter():
    get_lan_adapter_result=subprocess.run(['powershell', '-command', 'Get-NetAdapter | Select-Object Name, InterfaceDescription'],
                   capture_output=True,
                   text=True,
                   )
    
    get_lan_adapter_list=get_lan_adapter_result.stdout.splitlines()
    
   # print(get_lan_adapter_list)
   
    lan_no=0 #網卡編號從0開始
    
    lan_list=[]#將網卡資訊'存'入列表
    
    for index, item in enumerate(get_lan_adapter_list, start=1):#讓網卡有編號
        
        if item.strip()==''or item.strip().startswith('---')or item.strip().startswith('Name'):#如果這一行去掉空白後，什麼都沒有或者是---標題行
            
            continue#就跳過這一行
        
        lan_no += 1#網卡編號加1
        
        print(f"{lan_no}: {item}")
        
        lan_list.append(item)#將網卡資訊'加'入列表
        
        
            
    
    print('--'*30)
    
    while True:#USER防呆迴圈
        
        try:
        
            user_input = int(input('Please select the LAN adapter: '))
        
            if user_input > len(lan_list) or user_input <= 0 : #USER防呆
                
                print('Invalid LAN adapter number')
                
                continue #輸入錯誤 → 執行 continue，重新輸入。
            break #輸入正確 → 跳過 if，執行 break，離開迴圈。
            
        except ValueError:
            
            print('Please enter a number')
            
            
            
        
    Select_lan=lan_list[user_input-1]
    
    print(Select_lan)
            

def start_lan_test():

    print("======LAN Ping Test======")
    
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
    
    #儲存測試結果到log
    file_exists = os.path.exists('lan_test_log_V2.csv')
    
    if not file_exists:
        with open('lan_test_log_V2.csv', mode='a', newline='', encoding='utf-8-sig') as f:
            writer=csv.writer(f)
            writer.writerow(['Test Time', 'Target IP', 'Lost Number', 'Ping Status'])
    with open('lan_test_log_V2.csv',mode='a',newline='',encoding='utf-8-sig') as f:
        writer=csv.writer(f)#建立一個 CSV 寫入工具，讓它負責把資料寫進檔案 f
        writer.writerow([test_time,target_ip,lost_number,ping_status])
        

        
        
    
    
    
    
   
    
    