#基本英文字母與數字的Unicode編碼
#常用於加密解密（如凱撒密碼）、產生連續英文字母選單、或判斷字元範圍。
#ord(s)：輸入單一字元，傳回其對應的 Unicode 編碼數字。
print(ord('A'))  # 輸出：65
print(ord('a'))  # 輸出：97
print(ord('0'))  # 輸出：48
# 中文字元與 Emoji(emoji) 笑臉去網路複製貼上就可以使用 ord() 函式取得。
print(ord('台')) # 輸出: 21488 
print(ord('😊')) # 輸出: 128522