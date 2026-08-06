print(".......1.......")
# 建立list
list_data = ['abcd', 786, 2.23, 'John', 70.2, 786]
print(list_data)
#取得元素
print(list_data[0]) #第一個元素
print(list_data[2]) #第一個元素
print(list_data[1:3]) #輸出第二個至第三個元素
print(list_data[2:]) #輸出第二個至未的所有元素

# update
print(".......2.......")
print(list_data)
list_data[2] = "new number"
print(list_data)

#delete
print(".......3.......")
print(list_data)
del list_data[2]
print(list_data)

#append
print(".......4.......")
print(list_data)
list_data.append("cccc")
print(list_data)

#走訪
print(".......5.......")
for element in list_data:
    print(element)