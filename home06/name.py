#建立一個姓名 name 字串串列，及一個同樣長度的年齡 age 整數串列，使用者可以依選擇將年齡由小到大，或由大到小排序，並搭配姓名輸出。
from operator import itemgetter



name=['chang','fa','lee','how','ho']
age=[54,46,50,40,38]
name_age=list(zip(name,age))
#list(zip(name,age))將兩個串列打包成一個串列，裡面每個元素都是一個元組，元組的第一個元素是姓名，第二個元素是年齡。
#list(zip)只要你想把兩個（或多個）串列「一對一綑綁」成一個新串列，起手式直接寫 list(zip(串列1, 串列2))
choice= input('請輸入排序方式(1:由小到大,2:由大到小):')
if choice=='1':
 name_age.sort(key=itemgetter(1))
  #sort 就是專門下指令，預設由小排到大！。
  #itemgetter「項目獲取器」 或 「元素提取器」itemgetter(1)表示以元組的第二個元素（年齡）作為排序的依據
if choice=='2':
  name_age.sort(key=itemgetter(1),reverse=True)
    ####reverse=True表示反向排序，由大排到小
    
for 姓名, 年齡 in name_age:
    print(f"{姓名}:{年齡}", end="   ")
print()  # 最後換行
