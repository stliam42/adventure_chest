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
        

    def _member_giver(self, treasure):
        """Returns treasure to the pull and returns member to game"""
        dictionary = {"Разящий меч" : "Воин",
                      "Талисман" : "Клирик",
                      "Жезл силы" : "Маг",
                      "Воровские инструменты" : "Вор",
                      "Свиток" : "Свиток"}

        self._treasures_pull.append(self._treasures.pop(self._treasures.index(treasure)))
        self.ac_game.party.insert(0, dictionary[treasure])
        return dictionary[treasure]


    @property
    def is_combat(self):
        """Return True if there are some combat treasures"""
        return True if (self.__combat_treasures & set(self._treasures)) else False

    def use_combat(self, scroll=True):
        """Gets combat treasure, creates temporary unit in a party and returns it"""
        unique_treasures = list(set(self._treasures) & self.__combat_treasures)
        if scroll and "Свиток" in unique_treasures:
            unique_treasures.remove("Свиток")

        print("Какое сокровище хотите использовать?")

        active_treasure = self.ac_game._get_item(unique_treasures)
        
        return self._member_giver(active_treasure)

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