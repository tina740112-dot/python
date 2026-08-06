n1=34
n2=100
n3=-67

print(f'三個整數分別為{n1},{n2},{n3}')
if(n1>n2):
  if(n1>n3):
    max=n1
  else:
    max=n3
else:
  if(n2>n3):
    max=n2
  else:
    max=n3
    