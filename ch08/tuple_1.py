tuple1=('東','西','南')
print(tuple1)
east,west,south=tuple1
print(south)
tuple2=tuple1+('北',)
print(tuple2)
tuple1,tuple2=tuple2, tuple1
print(tuple1)
print(tuple2)
print(len(tuple1))
del(tuple2)
print(tuple2,'ERROR')