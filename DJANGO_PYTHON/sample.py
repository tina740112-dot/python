# 輸入身高與體重
height = float(input("請輸入身高（公分）："))
weight = float(input("請輸入體重（公斤）："))

# 將身高由公分轉換成公尺
height_m = height / 100

# 計算 BMI
bmi = weight / (height_m ** 2)

# 顯示結果
print(f"您的 BMI 是：{bmi:.2f}")

# 判斷 BMI 範圍
if bmi < 18.5:
    print("體重過輕")
elif bmi < 24:
    print("正常範圍")
elif bmi < 27:
    print("過重")
elif bmi < 30:
    print("輕度肥胖")
elif bmi < 35:
    print("中度肥胖")
else:
    print("重度肥胖")