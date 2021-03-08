class Stats():
    """Settings class for AC game"""

    def __init__(self):
        """Initialize game statistics"""
        # Dungeon
        self.dungeon_level = 1
        self.dungeon_trip = 1
        self.dragon_awake = False

        # Hero
        self.exp = 0
        self.ability_used = False
        