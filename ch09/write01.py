import os
pName ='c=/data/'
if not os.path.exists(pName):
    os.mkdir(pName)
fw=open('c:/data/file01.txt','w')
fw.write('王一心,85,90\n')
fw.write('王二心,75,87\n')  
fw.write('王三心,92,71')
fw.close()
fw.flush()

with open ('c:/data/stu.txt','w',encoding='utf-8')  as fr:
  fr.write('王一心,85,90\n')
  fr.write('王二心,75,87\n')
  fr.write('王三心,92,71') 