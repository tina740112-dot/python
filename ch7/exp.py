import math
principal = 10000 # 本金 10,000
rate = 0.05 # 年利率 5%
years = 3 # 3 年
# 計算連續複利公式：A = P * e^(r*t)
amount = principal * math.exp(rate * years)
print(f"連續複利後的總金額：{amount:.2f}")
# 連續複利後的總金額：11618.34                                                                                                                                                                                                                                                                                                                      
