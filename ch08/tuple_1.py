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
#print(tuple2) # tuple2 已被刪除
list1 = list(tuple1)
list1.append('東北')
print(list1) # ['東', '南', '西', '北', '東北']
tuple1 = tuple(list1) 
print(tuple1) # ('東', '南', '西', '北', '東北')
print(tuple1[0]) # 東
print('東北' in tuple1) # True
for t in tuple1:
	print(t, end=',')  # 東,南,西,北,東北,