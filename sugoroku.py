import random
def sugoroku(position=0):
  num = random.randint(1, 6)
  position += num
  return position