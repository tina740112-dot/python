dict1 = {'一月':'正月','二月':'花月','三月':'梅月'}
print(dict1)         # {'一月': '正月', '二月': '花月', '三月': '梅月'}
print(dict1['三月'])  # 梅月
dict1['一月'] = '端月' 
print('一月是', dict1['一月']) # 一月是 端月
del dict1['一月']
print(dict1) # {'二月': '花月', '三月': '梅月'}
dict1['一月'] = '正月' 
print(dict1) # {'二月': '花月', '三月': '梅月', '一月': '正月'}
print('1月' in dict1) # False 

del dict1 
#print(dict1) # NameError: name 'dict1' is not defined. Did you mean: 'dict'?