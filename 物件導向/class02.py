class Animal:
  def __init__(self, name):
    self.name = name
    print(f'【誕生】{self.name}建立好了!')
  def sing(self):
    print(self.name+"正在唱歌")
  def __del__(self):
    print(f'【銷毀】{self.name}記憶体已釋放!')
bird = Animal("鸚鵡")
print(bird.name)
bird.sing()
print('stanby delete bird')
del bird
print('finish')
  