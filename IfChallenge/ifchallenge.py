name = input('What is your name? ')

age = int(input('How old are you, {0} '.format(name)))

if 31 > age > 17:
    print('Enjoy your holiday, {0}'.format(name))
else:
    print('Sorry, no entry ' + name)
