no = [1,2,3,4]                                           # 編號
score = [[87,64,88],[93,72,86],[80,88,89],[79,91,90]]    # 成績   
print('編號   語文   數理   智力   總分')
print('================================') 
# 迴圈跑 len(no)=4 次， i =0, 1, 2, 3
for i in range(len(no)):
    # 印出 編號 1, 2, 3, 4 (2 位數字)
    print(f'{no[i]:2d}', end = '    ')
    hSum = 0
    # j = 0, 1, 2, 3
    # 計算每一 row 加總成績 for 每一編號學生
    for j in range(len(score[i])):
        print(f'{score[i][j]:3d}', end = '    ')
        hSum += score[i][j]
    print(f'{hSum:3d}')
 
print('平均', end = '   ')
# j = 0, 1, 2
for j in range(3):
    vSum = 0
    # i = 0, 1, 2    j = 0
    # i = 0, 1, 2    j = 1
    # i = 0, 1, 2    j = 2     
    for i in range(len(no)):
        vSum += score[i][j]
    # 平均 = ([0][0] + [1][0] + [2][0]) / 3 
    # 平均 = ([0][1] + [1][1] + [2][1]) / 3 
    # 平均 = ([0][2] + [1][2] + [2][2]) / 3 
    # 平均 = ([0][3] + [1][3] + [2][3]) / 3     
    print(f'{vSum/len(no):4.1f}', end = '   ')