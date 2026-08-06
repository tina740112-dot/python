# 2 input ,1 output
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