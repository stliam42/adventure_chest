from random import randint

class Treasures():
    """Treasures class for AC game"""

    def __init__(self, ac_game):
        self.reset()
        self.ac_game = ac_game

    def __repr__(self):
        return str(self._treasures)
    
    def __bool__(self):
        return True if self._treasures else False

    def get_treasure(self, n=1):
        """Gets i treasures"""
        for _ in range(n):
            self._treasures.append(self._treasures_pull.pop(randint(0, len(self._treasures_pull) - 1)))
            print(f'Получено сокровище - {self._treasures[-1]}')
            self.ac_game.dungeon.remove('Сундук')
            self.ac_game.delay()

    def use(self, type='all'):
        """Treasures using"""
        if type == 'combat':
            removed_treasures = ("Кольцо невидимости", "Драконьи чешуйки", 
                                 "Эликсир", "Приманка для дракона", "Городской портал")
        elif type == 'non-combat':
            removed_treasures = ("Разящий меч", "Талисман", "Жезл силы", 
                                 "Воровские инструменты", "Свиток", "Эликсир")
        else:
            removed_treasures = ()
        print("Какое сокровище вы хотите использовать:")
        treasure = self.ac_game._get_item(self._treasures, True, removed_treasures)
        if not treasure:
            return
        if treasure == "Разящий меч":
            self._sword()

    def _sword(self):
        """You can use sword like a warrior"""
        self._treasures_pull.append(self._treasures.pop(self._treasures.index(treasure)))

    def reset(self):
        """Reset treasures lists"""
        self._treasures_pull = [ "Разящий меч", "Разящий меч", "Разящий меч",
                                "Талисман", "Талисман", "Талисман",
                                "Жезл силы", "Жезл силы", "Жезл силы",
                                "Воровские инструменты", "Воровские инструменты", "Воровские инструменты",
                                "Свиток", "Свиток", "Свиток",
                                "Кольцо невидимости", "Кольцо невидимости", "Кольцо невидимости", "Кольцо невидимости",
                                "Драконьи чешуйки", "Драконьи чешуйки", "Драконьи чешуйки",
                                "Драконьи чешуйки", "Драконьи чешуйки", "Драконьи чешуйки",
                                "Эликсир", "Эликсир", "Эликсир",
                                "Приманка для дракона", "Приманка для дракона", 
                                "Приманка для дракона", "Приманка для дракона",
                                "Городской портал", "Городской портал", "Городской портал", "Городской портал"
                                ]
        self._treasures = []