ch = input("請輸入國文成績:")
print(ch)
print(type(ch))
#string
math = input("請輸入數學成績:")
eng = input("請輸入英文成績:")
sum = int(ch)+int(math)+int(eng)
avg = sum / 3
# avg = float(sum) / 3
print(f"sum={sum}")
print(f"成績總分:{sum}，平均成績:{avg:.3f}")
