#宣告
def f1(x):#x為區域變數
  return x**2+x+1

def f2(x,y):#x,y為區域變數
  return x**2+y**2+1

def f3(begin,end):#begin,end為區域變數
  total=0
  for x in range(begin,end+1):
    total+=x#total=total+x
  return total
#####################
#使用
num1=f1(2)
print(f'num1={num1}')

num2= f2(2,3)
print(f'num2={num2}')

num3=f3(1,3)
print(f'num3={num3}')
