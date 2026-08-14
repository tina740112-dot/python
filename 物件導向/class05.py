class Animal:
  
  def fly(self):
      print(self.name+" fly")
    
class Bird(Animal):
  def __init__(self, name):
      self.name='pink'+name
  def sing(self):
      print(self.name+' sing')
    
pigeon=Animal('白鴿')
pigeon.fly()

parrot=Bird('鸚鵡')
parrot.fly()
parrot.sing()