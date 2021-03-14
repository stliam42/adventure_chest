class Settings():
    """Settings for AC game"""

    def __init__(self):
        # Delay for printing messages
        self.time_delay = 0.1
        # Dice
        self.white_dice = 7
        self.black_dice = 7
        # Dungeon
        self.max_dungeon_level = 10
        self.max_dungeon_trip = 3
        self.dragon_slayers_number = 3 # Number of units who will slay a dragon

        # Hero
        self.random_hero = False
