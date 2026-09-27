import random as R                  # 匯入 Python 隨機模組，並將別名設為 R 以方便呼叫
 
max = 35                            # 設定亂數範圍的「最大值」（包含 35）
min = 18                            # 設定亂數範圍的「最小值」（包含 18）
num = 6                             # 設定預計要採集的不重複亂數「總數量」
 
arr = [0 for x in range(num)]       # 使用串列生成式建立長度為 6 的串列，預設填入 0 (即 [0, 0, 0, 0, 0, 0])
# arr = R.sample(range(min, max+1), num)  # (補充: Python 精簡寫法，可直接不重複抽樣取代底下整個 while 迴圈)
 
n = 0                               # 初始化「串列索引值」與「成功存入的亂數計數器」（從第 0 個位置開始填）
while (n < num):                    # 當已成功的亂數數量 (n) 還沒達到預期總數 (num) 時，繼續執行迴圈
    isRepeat = False                # 每次產生新亂數前，先假設（預設）這個亂數「沒有重複」
    
    rnd = R.randint(min, max)       # 隨機產生一個介於 min(18) 到 max(35) 之間的整數（包含兩端點）
    
    for v in arr:                   # 逐一取出目前 arr 串列中的每一個元素 v 來比對
        if rnd == v:                # 如果新產生的亂數 rnd 等於串列中已存在的元素 v
            isRepeat = True         # 代表數值重複了，將標記改為 True，並終止無謂的比對
            break                   # (補充優化: 發現重複即可立即跳出 for 迴圈，節省效能)
            
    if not isRepeat:                # 如果 isRepeat 仍為 False (即亂數確實「沒有重複」)
        arr[n] = rnd                # 將這個合格的亂數放入串列 arr 的第 n 個位置
        n += 1                      # 成功存入一個亂數，將索引計數器 n 加 1，準備填寫下一個位置
 
for i in range(num):                # 使用 for 迴圈從 i = 0 到 i = 5 走訪串列
    print(f'第 {i+1} 個亂數 : {arr[i]}') # 透過 f-string 格式化輸出，將序號 (i+1) 與對應位置的亂數 (arr[i]) 印出