x = True
y = False

def go(x, y):
    if not x and not y:
        return False
    else:
        return True

if go(x,y):
    print('yes')
else:
    print('no')
