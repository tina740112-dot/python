import math
items = 23 
capacity_per_box = 10 
boxes_needed = math.ceil(items / capacity_per_box) 
print(f"需要箱數：{boxes_needed}") 
# 需要箱數：3       (無條件進位)
