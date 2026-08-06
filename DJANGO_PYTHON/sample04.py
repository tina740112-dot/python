try:
	height_cm = float(input("請輸入身高（公分）："))
	weight_kg = float(input("請輸入體重（公斤）："))

	if height_cm <= 0 or weight_kg <= 0:
		print("身高和體重必須大於 0。")
	else:
		height_m = height_cm / 100
		bmi = weight_kg / height_m**2
		print(f"您的 BMI 是：{bmi:.2f}")
except ValueError:
	print("請輸入有效的數字。")
