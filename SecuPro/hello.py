print("Hello world")
#주석주석주석

age = 20
name = 'Swaroop'

print('{0} was {1} years old when he wrote this book'.format(name,age))
print('Why is {0} playing with that Python?'.format(name))

name = name + ' is ' + str(age) + ' years old'
print(name)

print('{name} wrote {book}'.format(name = 'Swaroop',book = 'A Byte of Python'))

for i in range(5):
    print(i)

fruits = ['banana', 'apple', 'mamgo']
for fruit in fruits:
    print('Current fruit : ', fruit)


for index in range(len(fruits)):
    print('Current fruit : ', fruits[index])


numbers = [12, 34, 55, 40, 55, 75, 37, 21 ,23 , 41 ,13]

for i in numbers:
  if(i % 2 == 0):
    print('is even')
else:
    print('is odd')