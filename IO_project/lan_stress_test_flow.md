# LAN Stress Test 流程圖

```mermaid
flowchart TD
    Start(["開始 start_lan_stress_test()"]) --> Input["詢問使用者：測試幾分鐘<br/>test_minutes_input = int(input(...))"]
    Input --> ToSec["換算成秒<br/>minutes_to_seconds = test_minutes_input * 60"]
    ToSec --> StartNow["記下起點時間<br/>start_now = time.time()"]
    StartNow --> EndTime["算出結束時間<br/>end_time = start_now + minutes_to_seconds"]
    EndTime --> Init["初始化計數器與清單<br/>count = 0 / durations = []"]
    Init --> Check{"現在時間 < end_time ?"}

    Check -- "是，還沒到時間" --> RoundStart["記錄這一輪開始時間<br/>round_start = time.time()"]
    RoundStart --> Work["做一次測試動作<br/>（之後可換成真正的網路測試，目前先用 sleep 模擬）"]
    Work --> RoundEnd["記錄這一輪結束時間<br/>round_end = time.time()"]
    RoundEnd --> Record["算出這一輪花費時間並存入清單<br/>durations.append(round_end - round_start)"]
    Record --> CountUp["count += 1"]
    CountUp --> Check

    Check -- "否，時間到了" --> Stats["從 durations 清單<br/>算出 min / max / avg"]
    Stats --> Report["組合報告內容<br/>(測試時間、總輪數、min/max/avg)"]
    Report --> Save["把報告寫成 txt 檔<br/>stress_test_report_YYYYMMDD_HHMMSS.txt"]
    Save --> End(["結束"])
```

## 文字版流程

1. 問使用者要測試幾分鐘，轉換成秒。
2. 記下開始時間，算出結束時間（`end_time`）。
3. 準備好 `count`（輪數計數器）和 `durations`（每輪花費時間清單）。
4. 進入迴圈，只要現在時間還沒超過 `end_time`：
   1. 記錄這一輪開始時間 `round_start`。
   2. 做一次測試動作（目前先用 `sleep` 模擬，之後可換成真正的網路測試）。
   3. 記錄這一輪結束時間 `round_end`。
   4. 計算這一輪花費時間，存進 `durations`。
   5. `count` 加 1，回到步驟 4 重新檢查時間。
5. 時間到，離開迴圈後：
   1. 用 `durations` 算出最小、最大、平均花費時間。
   2. 組合成報告文字（測試時間、總輪數、min/max/avg）。
   3. 把報告寫成一個 `.txt` 檔案，檔名帶時間戳記。
