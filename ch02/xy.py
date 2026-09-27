x=8
y=3
print(2 + 3 * 4 ** 2 // 5)
print(0 and 3, 2 or 3, not 0)
print(5 & 3, 5 | 3, 20 >> 2)
print(int('12') * 4, '12' * 4)

s = 'Python程式設計'
print(len(s))
print(s[3])
print(s[2])
print(s[6:2:-1])

身高=float(input('請輸入身高:'))
体重=float(input('請輸入体重:'))
bmi=体重/(身高**2)
print(f'您的bmi值為:{bmi:.2f}')

用電度數=float(input('請輸入用電度數:'))
if 用電度數<=120:
    電費=用電度數*1.63
    print(f'用電: {用電度數}，電費為: {電費} 元')
elif 用電度數<=330:
    電費=用電度數*2.10
    print(f'用電: {用電度數}，電費為: {電費} 元')
elif 用電度數<=500:
    電費=用電度數*2.89
    print(f'用電: {用電度數}，電費為: {電費} 元')
else:
    電費=用電度數*4.80
    print(f'用電: {用電度數}，電費為: {電費} 元')
S=