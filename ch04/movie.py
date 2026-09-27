age=int(input('請輸入年齡(正整數):'))
rating='普遍級'
if age >=18:
  rating="限制級"
elif age >=12:
  rating='輔導級'
elif age >=6:
  rating='保護級'
else:
  rating='普遍級'
print(f'年齡{age}最高可看{rating}電影')