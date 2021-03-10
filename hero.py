class Hero:
    """ Abstract hero class for adventure chest game.
        Common methods and attributes are defined here."""

    def __init__(self):
        self.name = 'unknown hero'
        self.is_ability_used = False

    def passive(self):
        """Passive ability"""
        pass

    def ability(self):
        """Active ability"""
        pass

    def upgrade(self):
        """Upgrade your abilities when yo have >= 5 exp and change name of hero"""
        pass

    def ability_check(self) -> bool:
        """Check possibility to use active ability"""
        pass

class Spellcaster(Hero):
    """
       They say that a battle mage who succumbed to the witchcraft
       rage, can slay a hundred monsters, leaving
       from them only a heap of ashes.
    """

    def __init__(self, ac_game):
        super().__init__(self)
        self.name = "Заклинатель меча"
        self.ac_game = ac_game

    def passive(self):
        """Spellcaster can use warriors as mages and vice versa."""




    
