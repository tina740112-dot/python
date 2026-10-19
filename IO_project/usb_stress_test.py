import subprocess
from datetime import datetime

def start_usb_stress_test():
    user_input_test_time=int(input('please enter thoe test time(minutes):'))
    print(f'usb stress test time:{user_input_test_time} minutes')