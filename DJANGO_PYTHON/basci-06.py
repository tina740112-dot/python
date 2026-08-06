print(".......1.......")
# 建立tuple
tuple_data = ('abcd', 786, 2.23, 'John', 70.2, 786)
print(tuple_data)
#取得元素
print(tuple_data[0]) #第一個元素
print(tuple_data[2]) #第一個元素
print(tuple_data[1:3]) #輸出第二個至第三個元素
print(tuple_data[2:]) #輸出第二個至未的所有元素

# tuple_data[2] = "new number" #TypeError
# 常數

#走訪
print(".......5.......")
for element in tuple_data:
    print(element)