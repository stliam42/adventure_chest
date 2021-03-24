""" Module with heroes for AdventureChest game """

from sys import modules
from inspect import getmembers, isclass
from random import choice


def __create_heroes_list():
    """This function creates list of heroes in this module"""
    available_heroes = [class_ for name, class_ in 
                    getmembers(modules[__name__], isclass) 
                    if issubclass(class_, Hero)]
    available_heroes.remove(Hero)
    available_heroes.remove(UnitHero)
    return available_heroes


def get_random_hero(ac_game):
    """Return random hero"""
    
    return choice(__create_heroes_list())(ac_game)
        

class Hero:
    """ Abstract hero class for adventure chest game.
        Common methods and attributes are defined here."""

    def __init__(self, ac_game):
        #self.name: str = 'unknown hero'
        #self.ability_name: str = 'unknown ability'
        self.exp: int = 0
        self.is_ability_used: bool = False
        self.is_passive_used: bool = False
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

    def reset_abilities(self):
        """Reset used abilities"""
        self.is_ability_used = False
        self.is_passive_used = False

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
        """UnitHero can use one_type as another_type and vice versa."""
        for key, unit in self.ac_game.units_dict.items():
            if unit in self.units:
                self.ac_game.units_dict[key] = self.units
        self.is_passive_used = True

    def ability(self, del_units=None):
        """UnitHero may be used as one_type or another_type
        improved ability allows reset all dungeon dice"""
        self.is_ability_used = True

        if self.improved:
            return self._improved_ability() 
        else:
            units = list(self.units)
            for del_unit in del_units:
                if del_unit in units:
                    units.remove(del_unit)

            # Choosing a unit
            self.ac_game.print_delay('{} может быть использован как "{}" или "{}".\n'
                                     .format(self.name, self.units[0], self.units[1]))
            self.ac_game.print_delay("Каким сопартийцем хотите воспользоваться?")

            unit = self.ac_game._get_item(units)
            self.ac_game.party.insert(0, unit)

            return unit

    def ability_check(self, usage=None, *args, **params):
        """Spellcaster may be used as warrior or mage.
           If game asks a unit - return True."""
        
        if self.is_ability_used:
            return False
        elif self.improved:
            return self._improved_ability_check(usage, args, params)
        else:
            # Checks if the hero can be used as a unit or not
            if usage != 'unit':
                return False

            own_units = list(self.units)

            # Try to delete forbidden units
            try:
                for del_unit in params['del_units']:
                    if del_unit in own_units:
                        own_units.remove(del_unit)
            except:
                pass

            return True if own_units else False

    def _improved_ability(self, *args, **kwargs):
        pass

    def _improved_ability_check(self, *args, **kwargs):
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

    def _improved_ability(self):
        """Resets all dungeon dice"""
        self.ac_game.print_delay('Вы используете способность {} '
                                 'и сбрасываете все кубики подземелья'
                                 .format(self.ability_name))
        self.ac_game.dungeon.clear()
        self.ac_game.dragon_lair.clear()

    def _improved_ability_check(self, usage, args, params):
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

    def _improved_ability(self):
        """Resets all dungeon dice"""
        self.ac_game.print_delay('Вы используете способность "{}".\n'
                                 .format(self.ability_name))
        self.ac_game.print_delay('Выберите сокровище, которое хотите сбросить, '
                                 'чтобы зачистить подземелье:')
        self.ac_game.treasures.discard(self.ac_game._get_item(self.ac_game.treasures))
        self.ac_game.print_delay('Сундуки:')
        self.ac_game._chest('Вор')
        self.ac_game.print_delay('Зелья:')
        self.ac_game._potion()
        self.ac_game.dungeon.clear()
        self.ac_game.dragon_lair.clear()

    def _improved_ability_check(self, usage, args, params):
        """Improved ability resets dungeon dice.
           Checks availability of dungeon dice."""
        if usage != 'ability':
            return False
        return True if all(((any([self.ac_game.dungeon, self.ac_game.dragon_lair])), 
                           self.ac_game.treasures)) else False
            
    def improve(self):
        """Improves your hero and gives him new name and ability"""
        super().improve('"Паладином"')
        self.name = "Паладин"
        self.ability_name = "Божественное вмешательство"
        
        self.ac_game.print_delay('Новая активная способность - "{}":\n'
                                 'сбросьте 1 жетон сокровища, '
                                 'чтобы сбросить всех монстров, '
                                 'открыть все сундуки, выпить все зелья и ' 
                                 'сбросить все кубики из логова дракона.\n'
                                 .format(self.ability_name))


class Knight(Hero):
    """
        The valiant knight is ignorant of magic, but in possession
        with a sword he has no equal! Passing the test of fire
        dragon slayer has studied all the weaknesses of his main
        enemy. And to defeat the beast, he needs support
        of only two different party members!
    """

    def __init__(self, ac_game):
        self.name = "Рыцарь"
        self.ability_name = "Боевой клич"
        self.passive_info = ("Пассивный навык: когда вы формируете партию, "
                             "все свитки становятся стражами.")
        self.ability_info = ('Активная способность - "{}": превращает всех монстров '
                             'в подземелье в драконов.'
                             .format(self.ability_name))
        super().__init__(ac_game)

    def passive(self):
        """ Replace all scrolls with guadrians when you form a party."""
        scroll_counter = 0
        while "Свиток" in self.ac_game.party:
            self.ac_game.party[self.ac_game.party.index("Свиток")] = "Страж"
            scroll_counter += 1
        if scroll_counter:
            self.ac_game.print_delay("При формировании партии {} {}."
                                     .format(scroll_counter,
                ('свиток был заменён стражем' if scroll_counter == 1 
                    else 'свитка были заменёны стражами')))
            print('')
        self.is_passive_used = True
        
    def ability(self):
        """ Transfom monsters into dragons and move it to lair"""
        self.ac_game.print_delay('Вы используете способность "{}".'
                                 .format(self.ability_name))
        self.ac_game.print_delay("Все монстры были превращены в драконов.\n")

        for monster in self.ac_game.dungeon:
            if any((monster == "Гоблин", monster == "Скелет", monster == "Слизень")):
                self.ac_game.dungeon[self.ac_game.dungeon.index(monster)] = "Дракон"

        self.is_ability_used = True

    def ability_check(self, usage, *args, **kwargs):
        """ Check monsters in a dungeon"""
        if usage != 'ability':
            return False
        return (True if any(("Гоблин" in self.ac_game.dungeon, 
                           "Скелет" in self.ac_game.dungeon, 
                           "Слизень" in self.ac_game.dungeon))
                else False)

    def improve(self):
        """Improves your hero and gives him new name and ability"""
        super().improve('"Убийцей драконов"')
        self.name = "Убийца драконов"
        
        self.ac_game.print_delay('Новый пассивный навык - чтобы победить '
                                 'дракона требуется 2 сопартийца, вместо 3.')
        self.ac_game.settings.dragon_slayers_number = 2
