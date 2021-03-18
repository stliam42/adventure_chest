from random import choice


class Group:
    """Parental class for groups in AdventureChest"""

    def __str__(self):
        return str(self.group)

    def __repr__(self):
        return self.group

    def __len__(self):
        return len(self.group)

    def __bool__(self):
        return True if self.group else False

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < len(self.group):
            result = self.group[self.i]
            self.i +=1
            return result
        raise StopIteration


    def add_unit(self, units:list=None, n:int=1):
        """Adds n unit to the group"""
        if units:
            self.group.extend(units)
        else:
            self.group += [choice(self.units) for unit in range(n)]


    def delete_unit(self, unit:str, all=False):
        """Kills unit in a group. If parametr 'all' is True:
           kills all units of this type"""
        if all:
            while unit in self.group:
                self.group.remove(unit)
        else:
            self.group.remove(unit)
    

    def insert(self, unit:str):
        """Inserts a unit to the 0-index"""
        self.group.insert(0, unit)

    def clear(self):
        """Clear a group"""
        self.group.clear()

    def count(self, unit:str):
        """Counts a unit in a group"""
        return self.group.count(unit)

    def pop(self, index:int=-1):
        """Pop the last unit or [index] unit and return it"""
        return self.group.pop(index)

    def index(self, unit:str):
        """Returns first index of unit"""
        return self.group.index(unit)




class Party(Group):
    """Class for AdventureChest party"""

    def __init__(self):
        self.group = []
        self.units = ["Воин", "Маг", "Вор", "Свиток", "Страж", "Клирик"]


class Dungeon(Group):
    """Class for AdventureChest dungeon"""
    
    def __init__(self):
        self.group = []
        self.units = ["Гоблин", "Скелет", "Слизень", "Зелье", "Сундук", "Дракон"]

    def is_monsters(self):
        """Returns True if there are monsters in a dungeon"""
        return True if ("Гоблин" in self.group or 
                        "Скелет" in self.group or 
                        "Слизень" in self.group) else False

    def is_reward(self):
        """Returns true if there are chests of potions in a dungeon"""
        return True if ("Сундук" in self.group or 
                        "Зелье" in self.group) else False

    def move_dragons(self) -> list:
        """Removes all dragons and return it"""
        dragons = []
        while "Дракон" in self.group:
            dragons.append(self.group.pop(self.group.index('Дракон')))

        return dragons


