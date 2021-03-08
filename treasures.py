from random import randint

class Treasures():
    """Treasures class for AC game"""

    def __init__(self, ac_game):
        self.reset()
        self.ac_game = ac_game
        self._combat_treasures = {"Разящий меч", "Талисман", "Жезл силы", 
                                   "Воровские инструменты", "Свиток", "Эликсир"}
        self.__non_combat_treasures = ("Кольцо невидимости", "Эликсир", 
                                       "Приманка для дракона", "Городской портал")
        self.items = {'sword':"Разящий меч"}

        self._treasure_to_unit_dict = {"Разящий меч" : "Воин",
                                       "Талисман" : "Клирик",
                                       "Жезл силы" : "Маг",
                                       "Воровские инструменты" : "Вор",
                                       "Свиток" : "Свиток"}
    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < len(self._treasures):
            result = self._treasures[self.i]
            self.i +=1
            return result
        raise StopIteration


    def __repr__(self):
        return self._treasures
    
    def __str__(self):
        return str(self._treasures)

    def __bool__(self):
        return True if self._treasures else False
    def clear(self):
        self._treasures.clear()

    def get_treasure(self, n=1):
        """Gets i treasures"""
        for _ in range(n):
            self._treasures.append(self._treasures_pull.pop(randint(0, len(self._treasures_pull) - 1)))
            print(f"Получено сокровище - '{self._treasures[-1]}'")
            if "Сундук" in self.ac_game.dungeon:
                self.ac_game.dungeon.remove('Сундук')
            self.ac_game.delay()  
        

    @property
    def is_combat(self):
        """Return True if there are some combat treasures"""
        return True if (self._combat_treasures & set(self._treasures)) else False


    def use_combat(self, del_members):
        """Gets combat treasure, creates temporary unit in a party and returns it"""
        unique_treasures = list(set(self._treasures) & self._combat_treasures)
        
        # Deleting treasures
        for key, value in self._treasure_to_unit_dict.items():
            if key in unique_treasures and value in del_members:
                unique_treasures.remove(key)

        print("Какое сокровище хотите использовать?")

        active_treasure = self.ac_game._get_item(unique_treasures)


        # Returns treasure to the pull and returns member to game
        self._treasures_pull.append(self._treasures.pop(self._treasures.index(active_treasure)))
        self.ac_game.party.insert(0, self._treasure_to_unit_dict[active_treasure])
        return self._treasure_to_unit_dict[active_treasure]

    def count_exp(self) -> int:
        """Count treasures experience"""
        exp = len(self._treasures)
        for treasure in self._treasures:
            if treasure == "Городской портал":
                exp += 1
        exp += self._treasures.count("Драконьи чешуйки")//2 * 2
        return exp

    def reset(self):
        """Reset treasures lists"""
        self._treasures_pull = (
            ["Разящий меч"] * 3 +
            ["Талисман"] * 3 +
            ["Жезл силы"] * 3 +
            ["Воровские инструменты"] * 3 +
            ["Свиток"] * 3 +
            ["Кольцо невидимости"] * 4 +
            ["Драконьи чешуйки"] * 6 +
            ["Эликсир"] * 3 +
            ["Приманка для дракона"] * 4 +
            ["Городской портал"] * 3
            )

        self._treasures = [] 
        """["Разящий меч", "Разящий меч", "Разящий меч",
                                "Талисман", "Талисман", "Талисман",
                                "Жезл силы", "Жезл силы", "Жезл силы"]"""