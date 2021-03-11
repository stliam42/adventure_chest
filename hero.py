class Hero:
    """ Abstract hero class for adventure chest game.
        Common methods and attributes are defined here."""

    def __init__(self, ac_game):
        self.name = 'unknown hero'
        self.ability_name = 'unknown ability'
        self.is_ability_used = False
        self.upgraded = False
        self.ac_game = ac_game
        self.passive()

    def passive(self):
        """Passive ability"""
        pass

    def ability(self, stage=None):
        """Active ability"""
        pass

    def upgrade_check(self):
        """Checks experience and upgrade your abilities"""
        if self.ac_game.stats.exp >= 5:
            self.upgrade()

    def upgrade(self):
        """Upgrade your abilities when yo have >= 5 exp and change name of hero"""
        self.upgraded = True
        pass

    def ability_check(self, **kwargs) -> bool:
        """Check possibility to use active ability"""
        return False

    def __str__(self):
        return ((f"Ваш герой - \"{self.name}\".\nСпособность \"{self.ability_name}\" ") + 
                ("использована." if self.is_ability_used else "не использована."))

    
class Spellcaster(Hero):
    """
       They say that a battle mage who succumbed to the witchcraft
       rage, can slay a hundred monsters, leaving
       from them only a heap of ashes.
    """

    def __init__(self, ac_game):
        super().__init__(ac_game)
        self.name = "Заклинатель меча"
        self.ability_name = "Мистический клинок"
        self.units = ('Воин', 'Маг')

    def passive(self):
        """Spellcaster can use warriors as mages and vice versa."""
        self.ac_game.units_dict['warrior'] = self.units
        self.ac_game.units_dict['mage'] = self.units

    def ability(self, del_units):
        """Spellcaster may be used as warrior or mage"""
        print("It's working")


    def ability_check(self, usage=None, *args, **params):
        """Spellcaster may be used as warrior or mage.
           If game asks a unit - return True."""

        own_units = list(self.units)

        for del_unit in params['del_units']:
            if del_unit in own_units:
                own_units.remove(del_unit)

        return (True if usage == 'unit' and not self.is_ability_used
                and own_units else False)




    
