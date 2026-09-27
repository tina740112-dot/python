# 基本 ASCII 轉字元
print(chr(65))   # 輸出: 'A'
print(chr(97))   # 輸出: 'a'
print(chr(48))   # 輸出: '0'
 
# Unicode 轉中文與 Emoji
print(chr(21488))  # 輸出: '台'
print(chr(128522)) # 輸出: '😊'
 
# 快速產生 A ~ Z 英文字母清單
# ASCII 中 A 是 65，Z 是 90
alphabet = [chr(i) for i in range(65, 91)]
print(alphabet)
# ['A', 'B', 'C', ..., 'Z']
 
# 簡單的字母位移（凱撒密碼原理）
# 利用 `ord()` 算出數字後加減，再用 `chr()` 轉回字元：
char = 'C'
shift = 3
# 將 'C' 向後推 3 個字母
new_char = chr(ord(char) + shift)
print(f"'{char}' 向後推 {shift} 位是: '{new_char}'")
# 輸出: 'C' 向後推 3 位是: 'F'