class Ability:
    """Class for common hero abilities"""

    @staticmethod
    def unit_ability(hero, del_units:tuple) -> str:
        """Ability which allows you to use hero as unit.
           Returns unit"""

        units = list(hero.units)
        for del_unit in del_units:
            if del_unit in units:
                units.remove(del_unit)

        # Choosing a unit
        hero.ac_game.print_delay('{} может быть использован как "{}" или "{}".\n'
                                 .format(hero.name, hero.units[0], hero.units[1]))
        hero.ac_game.print_delay("Каким сопартийцем хотите воспользоваться?")

        unit = hero.ac_game._get_item(units)
        hero.ac_game.party.insert(0, unit)

        return unit


    @staticmethod
    def unit_mix_passive(hero, *units_type):
        """Passive, which allows you to use a unit of one type as another."""
        for unit_type in units_type:
            hero.ac_game.units_dict[unit_type] = hero.units


    @staticmethod
    def unit_ability_check(hero, usage, args, params):
        """Checks if the hero can be used as a unit or not"""
        if usage != 'unit':
            return False

        own_units = list(hero.units)

        # Try to delete forbidden units
        try:
            for del_unit in params['del_units']:
                if del_unit in own_units:
                    own_units.remove(del_unit)
        except:
            pass

        return True if own_units else False

        
class Hero:
    """ Abstract hero class for adventure chest game.
        Common methods and attributes are defined here."""

    def __init__(self, ac_game):
        #self.name: str = 'unknown hero'
        #self.ability_name: str = 'unknown ability'
        self.exp: int = 0
        self.is_ability_used: bool = False
        self.improved: bool = False
        self.ac_game = ac_game
        self.passive()
        self.__introduce()

    def passive(self):
        """Passive ability"""
        pass

    def ability(self, usage=None):
        """Active ability"""
        pass

    def get_exp(self, n:int=1):
        """Get exp and check improve"""
        self.exp += n
        self.__improve_check()

    def __improve_check(self):
        """Checks experience and improve your abilities"""
        if self.exp >= 5 and not self.improved:
            self.improve()

    def improve(self):
        """improve your abilities when yo have >= 5 exp and change name of hero"""
        print('Ваш герой "{}" становится мастером!'.format(self.name))
        self.improved = True

    def ability_check(self, *args, **kwargs) -> None:
        """Check possibility to use active ability"""
        return None

    def __introduce(self):
        """Introduces a hero"""
        self.ac_game.print_delay('Ваш герой - "{}".'.format(self.name))

    def __str__(self):
        return ((f"Ваш герой - \"{self.name}\". Опыт - {self.exp} ед.\nСпособность \"{self.ability_name}\" ") + 
                ("использована." if self.is_ability_used else "не использована."))



class Spellcaster(Hero):
    """
       They say that a battle mage who succumbed to the witchcraft
       rage, can slay a hundred monsters, leaving
       from them only a heap of ashes.
    """

    def __init__(self, ac_game):
        self.units = ('Воин', 'Маг')
        self.name = "Заклинатель меча"
        self.ability_name = "Мистический клинок"
        super().__init__(ac_game)


    def passive(self):
        """Spellcaster can use warriors as mages and vice versa."""
        Ability.unit_mix_passive(self, 'warrior', 'mage')


    def ability(self, del_units=None):
        """Spellcaster may be used as warrior or mage
        improved ability allows reset all dungeon dice"""
        self.is_ability_used = True
        return self.__improved_ability() if self.improved else Ability.unit_ability(self, del_units) # FIXME


    def __improved_ability(self):
        """Resets all dungeon dice"""
        self.ac_game.print_delay('Вы используете способность {} и сбрасываете все кубики подземелья'
                                 .format(self.ability_name))
        self.ac_game.dungeon.clear()
        self.ac_game.dragon_lair.clear()


    def ability_check(self, usage=None, *args, **params):
        """Spellcaster may be used as warrior or mage.
           If game asks a unit - return True."""
        if self.is_ability_used:
            return False
        return (self.__improved_ability_check(usage, args, params) if self.improved 
                else Ability.unit_ability_check(self, usage, args, params))      
        

    def __improved_ability_check(self, usage, args, params):
        """Improved ability resets dungeon dice.
           Checks availability of dungeon dice."""
        if usage != 'ability':
            return False
        return True if any([self.ac_game.dungeon, self.ac_game.dragon_lair]) else False
            

    def improve(self):
        """Improves your hero and gives him new name and ability"""
        super().improve()
        self.name = "Боевой маг"
        self.ability_name = "Мистическая ярость"
        
        self.ac_game.print_delay('Новая активная способность - "{}": сбросьте все кубики подземелья.\n'
                                 .format(self.ability_name))

    def __introduce(self):
        """Introduces your hero: describes passive and active abilities"""
        self.ac_game.print_delay("Пассивный навык: воинов можно использовать как магов, а магов - как воинов.")
        self.ac_game.print_delay('Активная способность - "{}": "{}" может быть использован как воин или маг.'
                                 .format(self.ability_name, self.name))