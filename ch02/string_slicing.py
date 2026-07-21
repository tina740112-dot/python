flavor="fig pie"
print(flavor[0:3])#fig
print(flavor[3:7])# 空格pie
print(flavor[3:])#  空格pie
print(flavor[:]) #fig pie
print(flavor[:14])#fig pie
print(flavor[13:15])#已超過字串所以空的，但不會報錯

print(flavor[-7:-4])#fig 空格
print(flavor[-7:0])
print(flavor[-7:])
print(flavor[-3:])#pie
#字串切片
