class Animal:
  def __init__(self, name, age):
    self.name = name
    self.age= age
    
  def sing(self):
    print(self.name+str(self.age)+"歲，很會唱歌")
    
  def grow(self, year):
    self.age=self.age+year
    
#bird = Animal("鸚鵡",1)
#bird.grow(1)
#bird.sing()
Animal("鸚鵡", 1).grow(1)
Animal("鸚鵡", 1).sing()