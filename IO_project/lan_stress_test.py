import time #載入時間工具，用來計算測試起訖時間
from datetime import datetime #載入datetime，用來產生報告時間戳記
import subprocess #載入subprocess，用來呼叫外部指令(iperf3)
import json #載入json，用來解析iperf3的JSON輸出
import os
import matplotlib.pyplot as plt #載入matplotlib，用來即時畫出頻寬折線圖
from app_paths import get_app_folder

def _run_iperf_round(ip, round_seconds): #對單一IP跑一輪iperf3，回傳Mbps，失敗回傳None
    iperf_result = subprocess.run( #呼叫系統的iperf3指令
        ['iperf3', '-c', ip, '-t', str(round_seconds), '-J'], #對目標IP做round_seconds秒的頻寬測試，輸出JSON
        capture_output=True, #把iperf3的輸出抓回Python
        text=True #輸出用文字(字串)處理
    )
    try:
        result_json = json.loads(iperf_result.stdout) #把JSON文字轉成Python字典
        bits_per_second = result_json['end']['sum_received']['bits_per_second'] #取出這輪收到資料的平均位元率
        return bits_per_second / 1_000_000 #換算成Mbps(百萬位元/秒)比較好讀
    except (json.JSONDecodeError, KeyError): #iperf3 失敗或連不上時，輸出不是預期的JSON
        return None

def start_lan_stress_test(): #定義LAN壓力測試函式，main.py會呼叫它

    ip1 = input("Please enter the first IP address to test: ") #問使用者第一個要測試的目標IP
    ip2 = input("Please enter the second IP address to test: ") #問使用者第二個要測試的目標IP

    test_minutes_input = int(input("Please enter the test duration in minutes: ")) #問使用者要測幾分鐘
    print('testing') #提示使用者測試已經開始，避免看起來像當機
    minutes_to_seconds = test_minutes_input * 60 #將分鐘轉換為秒

    round_seconds = 5 #每一輪 iperf3 測試要跑幾秒

    start_now = time.time() #記下測試開始的時間點
    end_time = start_now + minutes_to_seconds #算出測試應該結束的時間點

    fail_count = {ip1: 0, ip2: 0} #分別記錄兩個IP測試失敗的次數
    count = 0 #記錄整段測試總共跑了幾輪，用來驗證測試有沒有持續穩定跑完整段時間
    bitrates = {ip1: [], ip2: []} #每一輪量到的頻寬(Mbps)，失敗該輪記None以維持輪次對齊

    plt.ion() #開啟互動模式，讓圖表可以在迴圈中即時更新
    fig, ax = plt.subplots()
    line1, = ax.plot([], [], marker='o', label=ip1)
    line2, = ax.plot([], [], marker='o', label=ip2)
    ax.set_xlabel('Round')
    ax.set_ylabel('Bitrate (Mbps)')
    ax.set_title('LAN Stress Test - Live Throughput')
    ax.legend()

    #只要現在時間小於 end_time，就繼續跑
    while time.time() < end_time:
        for ip in (ip1, ip2): #每一輪依序測試兩個IP
            mbps = _run_iperf_round(ip, round_seconds)
            if mbps is None:
                fail_count[ip] += 1 #視為這輪測試失敗
                bitrates[ip].append(None)
            else:
                bitrates[ip].append(mbps) #把這輪的頻寬記進清單

        count += 1 #每跑完一輪就加1，最後count就是總輪數

        x = list(range(1, count + 1)) #目前跑過的輪次編號
        y1 = [v if v is not None else float('nan') for v in bitrates[ip1]] #失敗輪次用nan讓圖上出現斷點
        y2 = [v if v is not None else float('nan') for v in bitrates[ip2]]
        line1.set_data(x, y1)
        line2.set_data(x, y2)
        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(0.01) #讓圖表視窗有機會刷新畫面

    successful_rounds = [v for v in bitrates[ip1] + bitrates[ip2] if v is not None]
    if not successful_rounds: #每一輪都失敗，沒有資料可以統計
        print("All rounds failed. No data to report.") #告知使用者沒有任何成功的測試結果
        plt.ioff()
        plt.close(fig)
        return #提早結束函式，不產生報告

    now_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S") #取得現在時間，格式化成報告用的時間戳記

    def _stats_block(ip): #組出單一IP的統計區塊文字
        data = [v for v in bitrates[ip] if v is not None]
        if not data:
            return f"    target ip:{ip}\n    all rounds failed (fail count:{fail_count[ip]})\n"
        return (
            f"    target ip:{ip}\n"
            f"    min bitrate:{min(data):.2f} Mbps\n"
            f"    max bitrate:{max(data):.2f} Mbps\n"
            f"    avg bitrate:{sum(data)/len(data):.2f} Mbps\n"
            f"    fail count:{fail_count[ip]}\n"
        )

    LAN_stress_test=(
        f"LAN stress test report (iperf3 throughput):\n"
        f"    test time:{now_time}\n"
        f"    total rounds:{count}\n\n"
        f"{_stats_block(ip1)}\n"
        f"{_stats_block(ip2)}"
    )
    print(LAN_stress_test) #把報告印到畫面上

    report_filename = f"stress_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt" #組出帶時間戳記的報告檔名
    chart_filename = f"stress_test_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png" #組出帶時間戳記的圖表檔名
    report_path = os.path.join(get_app_folder(), report_filename) #存在程式（或打包後的exe）所在資料夾
    chart_path = os.path.join(get_app_folder(), chart_filename)

    with open(report_path,mode='a',encoding='utf-8') as f: #開啟檔案準備寫入
        f.write(LAN_stress_test) #把報告文字寫進檔案

    fig.savefig(chart_path) #把最終折線圖存成圖片方便事後查看
    plt.ioff()
    plt.show() #顯示最終圖表，使用者關閉視窗後才繼續
