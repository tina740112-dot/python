import os
fName ='c:/data/stu.txt'
if os.path.isfile(fName):
  fr=open(fName,'r',encodind='utf-8') as fr:
  str1=fr.readline()
    
  print(str1,end='')
  str2=fr.readline(7)
  print(str2)
  
else:
  print(f'{fName}檔案不存在')
  
