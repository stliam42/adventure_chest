treasure = ['sword', 'shield', 'gun']

gear = ['sword']+['gun'] * 3 + ['gun'] * 4

print(gear)

from treasures import Treasures

t = Treasures(1)
print(t._treasures_pull, len(t._treasures_pull))
