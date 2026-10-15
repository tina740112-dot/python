import time

def start_lan_stress_test():

    test_minutes_input = int(input("Please enter the test duration in minutes: "))
    minutes_to_seconds = test_minutes_input * 60 #將分鐘轉換為秒
    
    start_now = time.time()
    end_time = start_now + minutes_to_seconds
    
    #取得現在時間，存到變數
    rount_start = time.time()
    
    count = 0
    durations = []
    
    #只要現在時間小於 end_time，就繼續跑
    while time.time() < end_time:
        