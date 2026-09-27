# 初始化原始串列
lst1 = [10, 20, 30, 40, 50]
print(f"0. 初始狀態: {lst1}\n" + "-" * 40)
 
# 1. append(value) - 附加到最後面
lst1.append(66)
print(f"1. append(66) 後  : {lst1}")  
 
# 2. insert(index, value) - 插入指定位置 (索引 2)
lst1.insert(2, 77)
print(f"2. insert(2, 77) 後: {lst1}")  
# 3. count(value) 與 index(value) - 統計與尋找位置
cnt = lst1.count(30)
idx = lst1.index(30)
print(f"3. 數字 30 出現 {cnt} 次，地位於索引: {idx}") 
 
# 4. remove(value) - 刪除第一個指定的值 (刪除 20)
lst1.remove(20)
print(f"4. remove(20) 後  : {lst1}")
 
# 5. pop(index) - 刪除指定位置元素並回傳 (刪除索引 3 的元素)
removed_val = lst1.pop(3)
print(f"5. pop(3) 移除了 [{removed_val}]，剩餘: {lst1}") 
 
# 6. pop() - 預設刪除最後一個元素
lst1.pop()
print(f"6. pop() 後       : {lst1}")
 
print("\n" + "=" * 40 + "\n[測試 del 切片與 clear 方法]\n") 
 
# 7. del 刪除操作 (使用新串列示範)
lst2 = [11, 22, 33, 44, 55, 66, 77]
print(f"原始 lst2: {lst2}")
del lst2[1:5:2]  # 刪除索引 1 到 4，步長為 2 的元素 (刪除索引 1 的 22 與 索引 3 的 44)
print(f"del lst2[1:5:2] 後: {lst2}")  # [11, 33, 55, 66, 77]
 
# 8. clear() - 清空整個串列
lst2.clear()
print(f"lst2.clear() 後    : {lst2}")  # []