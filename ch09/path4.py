import os
pName='c:/data/'
if os.path.exists(pName):
    print(f'{pName}路徑存在, 不必再建立')
else:
   print(f'{pName}路徑不存在')
  