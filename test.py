from treasures import Treasures
from adventure_chest import AdventureChest
tr = Treasures(AdventureChest())
tr.get_treasure(10)
exp = tr.count_exp()

print(exp)