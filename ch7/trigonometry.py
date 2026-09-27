import math
# 案例 1：已知角度與斜邊，計算直角三角形的對邊高度 (sin)
# 已知角度為 30 度，斜邊長為 10，求對邊高度
angle_degrees = 30
hypotenuse = 10.0
# 1. 將角度轉為弧度
radians = angle_degrees * (math.pi / 180) 
# 或使用 math.radians(30)
# 2. 計算對邊高度 = 斜邊 * sin(角度)  
height = hypotenuse * math.sin(radians)
print(f"30 度角、斜邊長 10 時的高度為：{height:.2f}") # 輸出：5.00
# 30 度角、斜邊長 10 時的高度為：5.00
# 案例 2：利用反切函數 (atan) 反推角度
# 已知對邊為 1，鄰邊為 1，求對應的角度
tan_value = 1.0
# 1. 計算反切函數取得弧度
rad_result = math.atan(tan_value)
# 取得弧度 (約 0.7854，即 π/4)
# 2. 將弧度轉為角度
deg_result = rad_result * (180 / math.pi) 
# 轉回角度
print(f"tan 答案為 1 時的角度為：{deg_result:.1f} 度")
# tan 答案為 1 時的角度為：45.0 度