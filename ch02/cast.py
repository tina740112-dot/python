i1=10
f1=float(i1)#使用float() change to float
print(i1,f1,type(f1))
f2=1234.5678
i2=int(f2)#use int() float change to int(整數)
print(f2,i2,type(i2))
i3=round(f2)#use rount()float change to int(四捨五入)
print(f2,i3,type(i3))#1234.5678 1235('int')
s=str(i2)#use str() int change to str
print(s,type(s))#1234<class 'str')
b=bool(f1)#use bool() float change to Bool
print(b,type(b))#true <class 'bool'>