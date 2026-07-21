import decimal#add decimal module
d1=decimal.Decimal.from_float(123.4567)#123.4567轉乘decimal型別
d2=decimal.Decimal.from_float(34.5678)#34.5678轉乘decimal型別
print(d1+d2)

print(decimal.getcontext())#取出目前Decimal資料型別運算設定
print(decimal.getcontext().prec)
print(decimal.getcontext().rounding)
print(d1+d2)
decimal.getcontext().prec=8
print(d1+d2)
