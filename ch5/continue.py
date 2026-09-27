#-*- coding:utf-8 -*-
s=input("請輸入字串: ")
for ch in s :
  if(ch>'9' or ch <'0'):
     continue
  print(ch,end='')
print()#換行，不寫也沒關係