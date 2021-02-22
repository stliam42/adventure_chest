from random import choice

class Die():
    """Standart die class"""

    def __init__(self):
        self.sides = []

    def roll(self, num_rolls):
        """Doing several (num_rolls) rolls"""
        rolls = [choice(self.sides) for roll in range(num_rolls)]
        return rolls

class White_die(Die):
    """White die class"""

    def __init__(self):
        self.sides = ["Воин", "Маг", "Вор", "Свиток", "Страж", "Клирик"]

class Black_die(Die):
    """Black die class"""

    def __init__(self):
        self.sides = ["Гоблин", "Слизень", "Сундук", "Зелье", "Дракон", "Скелет"]