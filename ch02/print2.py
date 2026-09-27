print('%c%s sir'%('張','無際'))
wt,price=3, 20.5
print('%s%d公斤,共%f元'%('香蕉',wt,wt*price))
print(bool(''))
print(bool(0 or 3))
print(bool(3 and 'a'))

x=25.6
h=10.84
area=(x*h)/2
print("三角形面積", round(area, 2))
x=25.6
h=10.84
三角形面積=(x*h)/2

x=10
y=4
print('相加',x+y)

攝氏度數=128
華氏度數=(攝氏度數 *9/5+32)
print("攝氏%04d度  =  華氏%08.3f度" % (攝氏度數, 華氏度數))

lst = [10, 20, 30, 40, 50]
lst.remove(30)
x = lst.pop()
print(lst, x)

print(lst.index(40), lst.count(20))
del lst[1:3]
print(lst)                      

print(lst + [7, 8], lst * 2) 


def stat(lst):
   #return max(lst), min(lst), sum(lst)/len(lst)
   return (f'最高= {max(lst)}, 最低= {min(lst)}, 平均= {sum(lst)/len(lst)} ')
 
print(stat([72, 98, 86, 76, 63]))

def power(base, exp=2):
    return base ** exp
print(power(5))
print(power(5, 3))
print(power(2, 10))





def f(n, lst):
    n = n * 2
    lst.append(99)
    v = 10
    global g
    g = g + 1
    print('函式內 :', n, lst, v, g)

g = 100
n = 5
data = [1, 2]
v = 0

f(n, data)
print('函式外 :', n, data, v, g)

t1 = (25)
t2 = (25,)
t3 = 25,
print(type(t1), type(t2), type(t3))


t4 = ('東', '南', '西')
a, b, c = t4
print(b)

t5 = t4 + ('北',)
print(t5, len(t5))  
print(sum((10, 20, 30), 40)) 
lst = list(t5)
lst.append('東北')
print(tuple(lst))   
#t4[0] = '中'
print(t4)

stock = {'A001': ['汽水', 25, 10],
         'A003': ['冰棒', 20, 5],
         'A006': ['口香糖', 8, 30]}
stock['A007'] = ['布丁', 18, 12]
#print(stock.get('A999','查無貨號'))
print(stock)
print(stock.get('A003'))
stock.pop('A006')
print(stock)
stock['A001'] = ['汽水', 25, 8]
print(stock)

