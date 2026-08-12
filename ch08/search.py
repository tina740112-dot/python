datas = {'A001':['汽水',25],
         'A005':['公司面',10],
         'A006':['口香糖',8],
         'A003':['冰棒',20]
         }
num=input('請輸入貨號:')
if num not in datas:
   print(f'貨號:{num}不存在')
   name=input('input name:')
   money=int(input('input money:'))
   datas[num]=[name,money]
   data1=datas.get(num)
   print(f'貨號:{num}品名:{data1[0]}價格:{data1[1]}')
         