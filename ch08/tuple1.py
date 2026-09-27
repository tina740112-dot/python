print("將元組轉換成串列")
list1=[10,20,30]
print(tuple(list1), "注意括號已不一樣了")

print("另一種方法:將串列轉換成元組")
tuple1=(10,20,30,20)
print(list(tuple1), )

print('傳回最小值的元素')
print(min(list1))


print('回傳元組的元素個數')
print(len(tuple1))

print('回傳元組中指定元素值的出現次數')
print(tuple1.count(20))


