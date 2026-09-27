import os
pName='c:/data/'
if os.path.isdir(pName):
  print(f'{pName}路徑為資料夾')
else:
  print(f'{pName}路徑不是資料夾')

fName='c:/Windows/system.ini'
if os.path.isfile(fName):
  print(f'{fName}路徑為檔案')
else:
  print(f'{fName}檔案路徑不存在')
  