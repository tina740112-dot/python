from 物件導向.class04 import animal


class Animal:
  
  def __init__(self, name):
      self.name = name
     
  def fly(self):
      print(self.name + " fly")
class bird(animal):
  def __init__(self, name,age):
    super().__init__(name)
   