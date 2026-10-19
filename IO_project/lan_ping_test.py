import os
import time
import csv
import subprocess
import re
import platform
from app_paths import get_app_folder

IS_WINDOWS = platform.system() == 'Windows'

def _list_adapters_windows(): #用Get-NetAdapter列出網卡，回傳顯示字串列表（最後一欄是ifIndex）
    result = subprocess.run(
        ['powershell', '-command',
         'Get-NetAdapter | Select-Object Name, InterfaceDescription, status,ifindex | Out-String -Width 200'],
        capture_output=True,
        text=True,
    )
    lines = []
    for item in result.stdout.splitlines():
        if item.strip()=='' or item.strip().startswith('---') or item.strip().startswith('Name'):
            continue
        lines.append(item)
    return lines

def _check_adapter_up_windows(ifindex): #用ifIndex重新查詢該網卡目前是否為Up
    result = subprocess.run(
        ['powershell', '-command',
         f'Get-NetAdapter -InterfaceIndex {ifindex}| Select-Object Name,InterfaceDescription, status,ifindex | Out-String -Width 200'],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    return 'Up' in result.stdout

def _list_adapters_linux(): #用ip指令列出網卡，回傳顯示字串列表（最後一欄是ifindex）
    result = subprocess.run(['ip', '-o', 'link', 'show'], capture_output=True, text=True)
    lines = []
    for item in result.stdout.splitlines():
        match = re.match(r'^(\d+):\s+(\S+?):\s+<([^>]*)>', item)
        if not match:
            continue
        index, name, flags = match.group(1), match.group(2), match.group(3)
        status = 'Up' if 'UP' in flags.split(',') else 'Down' #用FLAGS裡有沒有UP判斷網卡是否啟用
        lines.append(f'{name:<15} Status:{status:<6} {index}')
    return lines

def _check_adapter_up_linux(ifindex): #用ifindex重新查詢該網卡目前是否為Up
    for line in _list_adapters_linux():
        if line.split()[-1] == str(ifindex):
            print(line)
            return 'Up' in line
    return False

def get_lan_adapter():
    lan_list = _list_adapters_windows() if IS_WINDOWS else _list_adapters_linux()

    if not lan_list:
        print('No LAN adapter found')
        return False

    lan_no=0 #網卡編號從0開始

    for item in lan_list:#讓網卡有編號
        lan_no += 1#網卡編號加1
        print(f"{lan_no}: {item}")

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

    #USER選擇的網卡資訊
    Select_lan=lan_list[user_input-1]
    Select_lan_index = int(Select_lan.split()[-1])
    
    
    #印出USER選擇的網卡資訊
    print(Select_lan_index)
    
    #判斷USER選擇的網卡是否啟用
    while True:
        
        if 'Up' in Select_lan:
            print("Selected LAN adapter is up")
            break
        else:
            print("提醒:Selected LAN adapter is down!!!!!!!!!!!!!!!!!!!!")
            print("Please check the LAN connection")
        
    #如果選擇的網卡是關閉狀態，提示用戶選擇操作
        try:
            print("1:Retry\n"
                  "2:Cancel")
            
            User_input_2 = int(input('Please select option: '))
            if User_input_2 == 1:

                is_up = _check_adapter_up_windows(Select_lan_index) if IS_WINDOWS else _check_adapter_up_linux(Select_lan_index)

                if is_up:
                    print("LAN adapter is Up")
                    
                    break#有連線跳出迴圈
                
                else:
                
                    print("Retry Select lan driver") # Add the action for option 1 here
                
                    continue
            
            elif User_input_2 == 2:
                # Add the action for option 2 here
                print('Cancel Lan Test')
            return False
        
        except ValueError:
            print('Please enter a number')
   
        
    
   
            
##############PING TEST
def start_lan_test():
    

    print("======LAN Ping Test======")
    
    target_ip =input('Please enter the  IP address: ')
    
    ping_count = 4
    if IS_WINDOWS:
        ping_command = ['ping', '-n', str(ping_count), target_ip]
        ping_encoding = 'big5' #正確解碼繁體中文Windows的輸出
    else:
        ping_command = ['ping', '-c', str(ping_count), target_ip]
        ping_encoding = 'utf-8'

    ping_test_result=subprocess.run(
        ping_command,
        capture_output=True,
        text=True,
        encoding=ping_encoding
    )
 
    print(ping_test_result.stdout)#印出測試過程
    
    loss_match = re.search(r'(\d+)%', ping_test_result.stdout) #封包遺失率，跨平台的ping輸出都會有這個百分比數字
    lost_percent = int(loss_match.group(1)) if loss_match else 100
    lost_number = round(lost_percent * ping_count / 100)
    
    #判斷已遺失是不是=0
    if lost_number==0:
        ping_status = 'Pass'
        print('Ping Test : Pass ')
        
    else:
        ping_status = 'Fail'
        print('Ping Test : Fail')
        
    test_time=time.strftime('%Y-%m-%d %H:%M:%S')
    
    #儲存測試結果到log，存在程式（或打包後的exe）所在資料夾
    log_file = os.path.join(get_app_folder(), 'lan_test_log_V2.csv')
    file_exists = os.path.exists(log_file)
    
    if not file_exists:
        with open(log_file, mode='a', newline='', encoding='utf-8-sig') as f:
            writer=csv.writer(f)
            writer.writerow(['Test Time', 'Target IP', 'Lost Number', 'Ping Status'])
    with open(log_file,mode='a',newline='',encoding='utf-8-sig') as f:
        writer=csv.writer(f)#建立一個 CSV 寫入工具，讓它負責把資料寫進檔案 f
        writer.writerow([test_time,target_ip,lost_number,ping_status])
        

        
        
    
    
    
    
   
    
    