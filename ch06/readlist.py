lst = [[4,8,5,9],[13,16,19,15],[28,25,29,24]]
 
print('lst =', end = ' ')
print(lst)
for i in range(len(lst)):
    print()
    for j in range(len(lst[i])):
        print(f'lst[{i}][{j}]={lst[i][j]:2d}', end = '   ')