lst = [0 for x in range(5)]
print('請依序輸入5個整數...')
for i in range(5):
  print(f'input{i+1}個元素內容:',end = '')#接收使用者在鍵盤輸入的文字，並將他轉成數字
  lst[i]=eval(input())#出最大值(演算法核心)
max = lst[0]
for item in lst:
  if max < item:
     max = item
print()
print(f'max{max}')