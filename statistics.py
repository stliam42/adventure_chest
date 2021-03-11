class Stats():
    """Settings class for AC game"""

    def __init__(self):
        """Initialize game statistics"""
        self.reset()

    def reset(self):
        """Reset statistics"""

        # Dungeon
        self.dungeon_level = 1
        self.dungeon_trip = 1
        self.dragon_awake = False

