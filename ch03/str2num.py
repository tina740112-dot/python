s1,s2='123','12.34'
print(int(s1),type(int(s1)))
print(float(s2),type(float(s2)))
print(float(s1),type(float(s2)))
#123<class'int'>12.34<class'float'>
print(eval(s1),type(eval(s1)),eval(s2),type(eval(s2)))
print(eval('s1+s2'),type(eval('s1+s2')))#12312.34<class 'str'>
eval('print(s1+s2)') #12312.34
eval('print(2+3)')