# 0 input ,0 output
def test():
   print('hello,world')
# 2 input,1 output
def mul(x,y):
   return x*y

def add(x,y):
    return x+y

def minus(x,y):
    return x-y

def divide(x,y):
    if y==0:
        return '除數不能為零'
    else:
        return x/y
      
#2 input,4 output
def operation1(x,y):
    mul=x*y
    add=x+y
    minus=x-y
    divide=x/y
    return[mul,add,minus,divide]
print('另一種表示法 ') 
def operation2(x,y):
    mul=x*y
    add=x+y
    minus=x-y
    divide=x/y
    return[mul,add,minus,divide]
#################
test()
test()
num1=mul(3,4)
num2=add(5,6)
num3=minus(10, 2)
num4=divide(2, 3)
print(f'num1={num1},num2={num2},num3={num3},num4={num4}')

list_num= operation1(2,3)
for data in list_num:
    print(f'data={data}')
print('--------------------')
mul,add,minus,divide=operation2(2,3)
print(f'mul={mul},add={add},minus={minus},divide={divide}')