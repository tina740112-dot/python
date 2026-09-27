import os
pName='c:/data/'
if not os.path.exists(pName):
    os.mkdir(pName)

fName=open('c:/data/file02.txt','w')
fName.close()