from random import choice


class Group(list):
    """Parental class for groups in AdventureChest"""

    def add_unit(self, units:list=None, n:int=1):
        """Adds n unit to the group"""
        if units:
            self.extend(units)
        else:
            self += [choice(self.units) for unit in range(n)]


    def del_unit(self, unit:str, all=False):
        """Kills unit in a group. If parametr 'all' is True:
           kills all units of this type"""
        if all:
            while unit in self.group:
                self.group.remove(unit)
        else:
            self.group.remove(unit)


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


