#已幫你在檔案中加上詳細註解：


# 匯入 math 模組，提供數學常數與函數，例如 π、e、log、ceil
import math

# 使用 print() 顯示圓周率 π 的值
print(f'圓周率π:{math.pi}')  # 輸出圓周率 π，約為 3.14159

# 使用 print() 顯示自然對數底 e 的值
print(f'自然對數e:{math.e}')  # 輸出自然對數底 e，約為 2.71828

# 這一行是註解，說明我們接下來要解決的問題：
# 如果要儲存 1000 種不同狀態，至少需要多少個位元
# 這裡先設定要儲存的狀態數量為 1000
states = 1000

# 這一行是計算公式：ceil(log2(states))
# 其中 log2(states) 表示以 2 為底計算 states 的對數
# math.ceil(...) 會將結果向上取整，確保位元數足夠
bits_needed = math.ceil(math.log(states, 2))

# 使用 print() 輸出計算結果，顯示需要多少個位元
print(f"儲存 {states} 種狀態需要 {bits_needed} 個位元")  # 顯示結果，例如 1000 種狀態需要 10 個位元
import math
print(f'圓周率π:{math.pi}') # 圓周率π:3.14159
print(f'自然對數e:{math.e}') # 自然對數底e:2.71828
# 欲儲存 1000 種狀態，至少需要多少個位元 (Bits)？
states=1000
# 計算公式：ceil(log2(states))，其中 log2 為以 2 為底的對數
bits_needed = math.ceil(math.log(states, 2))
print(f"儲存 {states} 種狀態需要 {bits_needed} 個位元")
# 儲存 1000 種狀態需要 10 個位元