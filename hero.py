class Hero:
    """ Abstract hero class for adventure chest game.
        Common methods and attributes are defined here."""

    def __init__(self, ac_game):
        self.name = 'unknown hero'
        self.ability_name = 'unknown ability'
        self.is_ability_used = False
        self.upgraded = False
        self.ac_game = ac_game

    def passive(self):
        """Passive ability"""
        pass

    def ability(self):
        """Active ability"""
        pass

    def upgrade_check(self):
        if self.ac_game.stats.exp >= 5:
            self.upgrade()

    def upgrade(self):
        """Upgrade your abilities when yo have >= 5 exp and change name of hero"""
        self.upgraded = True
        pass

    def ability_check(self) -> bool:
        """Check possibility to use active ability"""
        return True

    def __str__(self):
        return self.name

    
class Spellcaster(Hero):
    """
       They say that a battle mage who succumbed to the witchcraft
       rage, can slay a hundred monsters, leaving
       from them only a heap of ashes.
    """

    def __init__(self, ac_game):
        super().__init__(self)
        self.name = "Заклинатель меча"
        self.ability_name = "Мистический клинок"


    def passive(self):
        """Spellcaster can use warriors as mages and vice versa."""
        self.ac_game.unit_dict['warrior'] = ('Воин','Маг')
        self.ac_game.unit_dict['mage'] = ('Воин','Маг')



    
