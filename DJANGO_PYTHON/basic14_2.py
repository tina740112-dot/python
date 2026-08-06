for x in range(2):#2=0,1
  for y in range(4):#4=0,1,2,4
    print(f'x={x},y={y}')


##################
#九九乘法
for x in range(1,10):#x=外迴圈
  for y in range(1,10):
    print(f'{x}*{y}={x*y:2d}',end=' ')
  print()
    