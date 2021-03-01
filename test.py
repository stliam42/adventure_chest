from treasures import Treasures

tr = Treasures(1)

if not tr:
    print(0)

tr.get_treasure(2)

if tr:
    print(1)