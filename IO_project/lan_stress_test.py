import time

def start_lan_stress_test():

    test_minutes_input = int(input("Please enter the test duration in minutes: "))
    minutes_to_seconds = test_minutes_input * 60 #將分鐘轉換為秒
    
    start_now = time.time()
    end_time = start_now + minutes_to_seconds
    
    count = 0
    durations = []
    
    #只要現在的時間還沒超過 end_time，就一直重複執行底下的程式碼」。
    while time.time():
        