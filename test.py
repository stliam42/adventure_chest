from treasures import Treasures
from adventure_chest import AdventureChest

tr = Treasures(3)
exp = tr.count_exp()
print(tr._treasures)

print(tr.is_combat(("Вор", "Свиток")))