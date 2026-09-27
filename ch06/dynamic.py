lst=[]
count = eval(input('請輸入lst串列的元素數量:'))
print('請依序填入各元素的內容...')
      #會產生一個從0開始，長度count的數字序列
for i in range(count):
 print(f'輸入第{+1}元素內容:',end="")
 num=eval(input())
 lst.append(num)
 
print('lst串列的元素內容')
for x in lst:
  print(x, end = ' ')