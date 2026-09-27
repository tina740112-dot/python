class Animal:
  def __init__(self, name, age):
    self.name = name
    self.age= age
    
  def sing(self):
    print(self.name+str(self.age)+"歲，很會唱歌")
    
  def grow(self, year):
    self.age=self.age+year
    
bird = Animal("鸚鵡",1)


bird.grow(1)
bird.sing()
  