a=[4,-15,20,13,-11]
print('排 序 前 :',end='')
for i in range(5):
    print(f' a[{i:d}]={a[i]:3d}',end=' ')
print()
  
for loop in range(1,5):
    for index in range(0, (5-loop)):
      if a[index]>a[index+1] :
        temp = a[index]
        a[index]=a[index+1]
        a[index+1]=temp

    print(f'第{loop}次排列:',end = '')
    for j in range(5):
        print(f' a[{j:d}]={a[j]:3d}',end=' ')    
    print()    