g1=['lin2','wang1','chang3','zhao6','wang1','li4','chang3','chan5']
g2=['chang10','zhao6','liuchang','lio8','ko7','chang3','wang1','li4','lu9','ko7','tsaibai']
s1=set(g1)
print(f'hot music people: {len(g1)}   exact count:{len(s1)} ')
s2=set(g2)
print(f'popular music people:{len(g2)}  exact people count:{len(s2)}')
s3=s1.intersection(s2)
print(f'double in people:{s3}')
s4=s1.union(s2)
print(f'all people:{len(s4)}')

  


