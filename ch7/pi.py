# 案例：計算圓形面積與斜邊長
import math
radius=5.0
circle_area=math.pi*(radius**2)
print(f'半徑為{radius}的圓面積是:{circle_area:.2f}')
# 畢氏定理：計算直角三角形斜邊 (a=3, b=4)
a,b=3.0,4.0
c=math.sqrt(a**2+b**2)
print(f'斜邊長c:{c}')