""" Module with heroes for AdventureChest game """

from sys import modules
from inspect import getmembers, isclass
from random import choice


def create_hero_list():
    """This function creates list of heroes in this module"""
    available_heroes = [class_ for name, class_ in 
                    getmembers(modules[__name__], isclass) 
                    if issubclass(class_, Hero)]
    available_heroes.remove(Hero)
    available_heroes.remove(UnitHero)
    return available_heroes


def get_random_hero(ac_game):
    """Return random hero"""
    global __avaible_heroes
    return choice(__avaible_heroes)(ac_game)


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
    def unit_mix_passive(hero):
        """Passive, which allows you to use a unit of one type as another."""
        for key, unit in hero.ac_game.units_dict.items():
            if unit in hero.units:
                hero.ac_game.units_dict[key] = hero.units


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

    def improve(self, new_name:str):
        """Improve your abilities when yo have >= 5 exp and change name of hero"""
        print('Ваш герой "{}" становится {}!'.format(self.name, new_name))
        self.improved = True

    def ability_check(self, *args, **kwargs) -> None:
        """Check possibility to use active ability"""
        return None

    def __introduce(self):
        """Introduces a hero"""
        self.ac_game.print_delay('Ваш герой - "{}".'.format(self.name))
        self.ac_game.print_delay(self.passive_info)
        self.ac_game.print_delay(self.ability_info)


    def __reset(self):
        """Reset a hero"""
        self.__init__(self.ac_game)

    def __rep__(self):
        return self.name

    def __str__(self):
        return ((("Ваш герой - \"{}\". Опыт - {} ед.\n") + 
                ("Способность \"{}\" "))
                .format(self.name, self.exp, self.ability_name) + 
                ("использована." if self.is_ability_used 
                 else "не использована."))


class UnitHero(Hero):
    """Class for heroers who may be used as unit and whose passive
       allows to use one type of units as another"""

    def __init__(self, ac_game):
        super().__init__(ac_game)

    def passive(self):
        """UnitHero can use one_tupe as another_type and vice versa."""
        Ability.unit_mix_passive(self)


    def ability(self, del_units=None):
        """UnitHero may be used as one_type or another_type
        improved ability allows reset all dungeon dice"""
        self.is_ability_used = True
        return (self.__improved_ability() if self.improved 
                else Ability.unit_ability(self, del_units))

    def ability_check(self, usage=None, *args, **params):
        """Spellcaster may be used as warrior or mage.
           If game asks a unit - return True."""
        if self.is_ability_used:
            return False
        return (self.__improved_ability_check(usage, args, params) if self.improved 
                else Ability.unit_ability_check(self, usage, args, params)) 

    def __improved_ability(self, *args, **kwargs):
        pass

    def __improved_ability_check(self, *args, **kwargs):
        pass


class Spellcaster(UnitHero):
    """
       They say that a battle mage who succumbed to the witchcraft
       rage, can slay a hundred monsters, leaving
       from them only a heap of ashes.
    """

    def __init__(self, ac_game):
        self.units = ('Воин', 'Маг')
        self.name = "Заклинатель меча"
        self.ability_name = "Мистический клинок"
        self.passive_info = ("Пассивный навык: воинов можно использовать "
                             "как магов, а магов - как воинов.")
        self.ability_info = ('Активная способность - "{}": "{}" может быть '
                             'использован как воин или маг.'
                             .format(self.ability_name, self.name))
        super().__init__(ac_game)


    def __improved_ability(self):
        """Resets all dungeon dice"""
        self.ac_game.print_delay('Вы используете способность {} '
                                 'и сбрасываете все кубики подземелья'
                                 .format(self.ability_name))
        self.ac_game.dungeon.clear()
        self.ac_game.dragon_lair.clear()


    def __improved_ability_check(self, usage, args, params):
        """Improved ability resets dungeon dice.
           Checks availability of dungeon dice."""
        if usage != 'ability':
            return False
        return True if any([self.ac_game.dungeon, self.ac_game.dragon_lair]) else False
            

    def improve(self):
        """Improves your hero and gives him new name and ability"""
        super().improve('"Боевым магом"')
        self.name = "Боевой маг"
        self.ability_name = "Мистическая ярость"
        
        self.ac_game.print_delay('Новая активная способность - "{}":сбросьте все '
                                 'кубики подземелья.\n'.format(self.ability_name))


class Crusader(UnitHero):
    """
       The holy warrior who fights in the name
       your god. She regularly pays tithing and
       a cop of need can count on the divine
       intervention ... Monsters scatter in fear
       away from her shining consecrated sword. And how only
       the light dims, all the chests open, and for each found
       the potion revives a party member.
    """

    def __init__(self, ac_game):
        self.units = ('Воин', 'Клирик')
        self.name = "Крестоносец"
        self.ability_name = "Праведный удар"
        self.passive_info = ("Пассивный навык: воинов можно использовать "
                             "как клириков, а клириков - как воинов.")
        self.ability_info = ('Активная способность - "{}": "{}" может быть '
                             'использован как воин или клирик.'
                             .format(self.ability_name, self.name))
        super().__init__(ac_game)


    def __improved_ability(self):
        """Resets all dungeon dice"""
        self.ac_game.print_delay('Вы используете способность {} и сбрасываете все кубики подземелья'
                                 .format(self.ability_name))
        self.ac_game.dungeon.clear()
        self.ac_game.dragon_lair.clear()


    def __improved_ability_check(self, usage, args, params):
        """Improved ability resets dungeon dice.
           Checks availability of dungeon dice."""
        if usage != 'ability':
            return False
        return True if all((any([self.ac_game.dungeon, self.ac_game.dragon_lair])), 
                           self.ac_game.treasures) else False
            

    def improve(self):
        """Improves your hero and gives him new name and ability"""
        super().improve('"Паладином"')
        self.name = "Паладин"
        self.ability_name = "Божественное вмешательство"
        
        self.ac_game.print_delay('Новая активная способность - "{}":\n'
                                 'сбросьте 1 жетон сокровища,'
                                 'чтобы сбросить всех монстров, '
                                 'открыть все сундуки, выпить все зелья и ' 
                                 'сбросить все кубики из логова дракона.\n'
                                 .format(self.ability_name))


_available_heroes = create_hero_list()