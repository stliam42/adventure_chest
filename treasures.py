from random import randint

class Treasures():
    """Treasures class for AC game"""

    def __init__(self, ac_game):
        self.reset()
        self.ac_game = ac_game
        self.__combat_treasures = {"Разящий меч", "Талисман", "Жезл силы", 
                                   "Воровские инструменты", "Свиток", "Эликсир"}
        self.__non_combat_treasures = ("Кольцо невидимости", "Эликсир", 
                                       "Приманка для дракона", "Городской портал")
        self.items = {'sword':"Разящий меч"}

    def __repr__(self):
        return self._treasures
    
    def __str__(self):
        return str(self._treasures)

    def __bool__(self):
        return True if self._treasures else False


    def get_treasure(self, n=1):
        """Gets i treasures"""
        for _ in range(n):
            self._treasures.append(self._treasures_pull.pop(randint(0, len(self._treasures_pull) - 1)))
            print(f"Получено сокровище - '{self._treasures[-1]}'")
            self.ac_game.dungeon.remove('Сундук')
            self.ac_game.delay()  

    def _sword(self):
        """You can use sword like a warrior"""
        self._treasures_pull.append(self._treasures.pop(self._treasures.index("Разящий меч")))
        self.ac_game.party.insert(0, "Воин")
        return "Воин"

    @property
    def is_combat(self):
        """Return True if there are some combat treasures"""
        return True if (self.__combat_treasures & set(self._treasures)) else False

    def use_combat(self, scroll=True):
        """Gets combat treasure, creates temporary unit in a party and returns it"""
        unique_treasures = list(set(self._treasures) & self.__combat_treasures)
        if scroll and "Свиток" in unique_treasures:
            unique_treasures.remove("Свиток")

        print("Какое сокровище использовать?")

        active_treasure = self.ac_game._get_item(unique_treasures)
        
        if active_treasure == self.items['sword']:
            return self._sword()

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

        self._treasures = ["Разящий меч", "Разящий меч", "Разящий меч",
                                "Талисман", "Талисман", "Талисман",
                                "Жезл силы", "Жезл силы", "Жезл силы"]