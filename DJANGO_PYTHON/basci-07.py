# 建立
print("..........1..........")
dict_data = {"name":"John","code":6734,"dept":"sales"}
# 無順序性
print(dict_data)

#再新增
print("..........2..........")
print(dict_data)
dict_data["one"] = "This is one"
print(dict_data)

dict_data2 = {}
dict_data2["one"]="one"
dict_data2[2]="two"
print(dict_data2)

#修改
print("..........3..........")
print(dict_data)
dict_data['code'] = 8888
print(dict_data)

#取值
print("..........4..........")
print(dict_data['code'])
print(dict_data['dept'])
print(dict_data['name'])

#刪除
print("..........5..........")
print(dict_data)
del dict_data["dept"]
print(dict_data)

#走訪
print("..........6..........")
#取key，透過key，再產生value
print(dict_data)
for key in dict_data:
    # print(key)
    print(f"{key}=>{dict_data[key]}")

print("..........7..........")
#利用items()，取得key and value
for k, v in dict_data.items():
    # print(k)
    # print(v)
    # print("...")
    print(f"{k}=>{v}")

print("..........8..........")
# print(dict_data["sample"]) #KeyError
# 方法一:try excpet
# 方法二:透過get()方法
print(dict_data.get("sample")) #預設None
print(dict_data.get("sample","N")) #預設None
print(dict_data.get("name","N")) #預設None