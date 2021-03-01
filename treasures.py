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

    def get_treasure(self, i):
        """Gets i treasures"""
        for _ in range(i):
            self._treasures.append(self._treasures_list.pop(randint(0, len(self._treasures_list) - 1)))

    def reset(self):
        """Reset treasures lists"""
        self._treasures_list = [ "Разящий меч", "Разящий меч", "Разящий меч",
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