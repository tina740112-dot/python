import os
fName ='c:/data/stu.txt'
if os.path.isfile(fName):
  fr=open(fName,'r')
  str1=fr.read(7)
  print(str1)
  print(fr.read())
  fr.close()
else:
  print(f'{fName}檔案不存在')
  
  