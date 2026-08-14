x=0
while x<5:
  x+=1
  if x==3:
    continue
  if x==4:
    break
print(x,end='')
#########################
i=10
p=20
result=(i>15)or(p==20)
print(result)
#########################
i=1
total=0
while i<=3:
  total+=i
  i+=1
print(total)
############################
data="apple,banana,orange".split(',')
print(data)
#######################################
def petStore(category, species, breed="Unknown"):
    print(category, species, breed)

petStore(breed="Maltese", species="Canine", category="dog")
#############################
int("hello")