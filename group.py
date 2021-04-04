from random import choice


class Group(list):
    """Parental class for groups in AdventureChest"""

    def add_unit(self, n:int=1, units:list=None):
        """Adds n unit to the group"""
        if units:
            self.extend(units)
        else:
            self += [choice(self.units) for unit in range(n)]


    def kill_unit(self, unit:str, all=False):
        """Kills unit in a group. If parametr 'all' is True:
           kills all units of this type"""
        if all:
            while unit in self:
                self.remove(unit)
        else:
            self.remove(unit)


class Party(Group):
    """Class for AdventureChest party"""

    def __init__(self):
        self.units = ["Воин", "Маг", "Вор", "Свиток", "Страж", "Клирик"]
        super().__init__()


class Dungeon(Group):
    """Class for AdventureChest dungeon"""
    
    def __init__(self):
        self.units = ["Гоблин", "Скелет", "Слизень", "Зелье", "Сундук", "Дракон"]
        super().__init__()

    def is_monsters(self):
        """Returns True if there are monsters in a dungeon"""
        return True if ("Гоблин" in self or 
                        "Скелет" in self or 
                        "Слизень" in self) else False

    def count_monsters(self) -> int:
        """Count monsters in the dungeon and return the number"""
        counter = 0
        for item in self:
            if item == 'Гоблин' or item == 'Скелет' or item == 'Слизень':
                counter += 1
        return counter
    
    def is_reward(self):
        """Returns true if there are chests of potions in a dungeon"""
        return True if ("Сундук" in self or 
                        "Зелье" in self) else False

    def move_dragons(self) -> list:
        """Removes all dragons and return it"""
        dragons = []
        while "Дракон" in self:
            dragons.append(self.pop(self.index('Дракон')))

        return dragons


class DragonLair(Group):
    """Dragon lair class for AdventureChest game"""

    @property
    def is_awake(self):
        """ Return True is Dragon lair has 3 dice or more"""
        return True if len(self) >= 3 else False


if __name__ == "main":
    main()