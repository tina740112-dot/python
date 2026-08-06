from math_operation import test,mul,add,minus,divide,operation1
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
