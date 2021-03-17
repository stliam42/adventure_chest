from time import sleep
import sys

from group import Party, Dungeon
from stats import Stats
from settings import Settings
from treasures import Treasures
from exceptions import Defeat, Leave
import hero 


class AdventureChest():
    """Adventure Chest game class"""

    def __init__(self):
        """Inintialization parametrs"""

        # Game stats
        self.stats = Stats()

        # Game settings
        self.settings = Settings()
        #self.__request_settings()      #FIXME


        # Treasures
        self.treasures = Treasures(self)

        # Units dictionary for heroes abilities
        self.units_dict = {"warrior" : ("Воин"), 
                           "cleric" : ("Клирик"), 
                           "mage" : ("Маг"), 
                           "thief": ("Вор"), 
                           "guardian" : ("Страж"),
                           "scroll" : ("Свиток"),
                           "monster" : ("Гоблин", "Скелет", "Слизень")
                           }

        # Hero
        self.hero = hero.Crusader(self)
        self.hero.get_exp(5)

        # Player's party, monters, cemetery and dragon lists
        self._reset_dungeon()

        # Print the settings of current dungeon
        self._print_dungeon_settings()

        # Applies hero's passive
        self.hero.passive()


    #def __request_settings(self):
    #    while True:
    #        try:
    #            print("1 - Пользовательские настройки, 2 - Использовать стандартные.")
    #            answer = int(input("Ваш выбор: "))
    #        except:
    #            self.print_delay("Некорректный ввод")
    #        else:
    #            if answer > 2:
    #                raise ValueError
    #            elif answer == 1:
    #                white_dice = int(input("Введите количество кубиков партии: "))
    #                self.settings.white_dice = 
    #            else:
    #                break


    def _reset_dungeon(self):
        """Reset dungeon"""
        self.party = Party()
        self.party.add_unit(n=self.settings.white_dice)
        self.dungeon = Dungeon()
        self.dragon_lair = []
        self.stats.dungeon_level = 1
        self.treasures.clear()
        self.hero.is_ability_used = False


    def reset_game(self):
        """Resets game statistics and other parametrs"""
        self.stats.reset()
        self.hero.improved = False


    def _print_dungeon_settings(self):
        """Display dungeon settings"""
        self.print_delay("Количество походов в подземелье - {}."
                         .format(self.settings.max_dungeon_trip))
        self.print_delay("Максимальный уровень подземелья - {}."
                         .format(self.settings.max_dungeon_level))
        self.print_delay("Количество кубиков партии - {}."
                         .format(self.settings.white_dice))
        self.print_delay("Количество кубиков подземелья - {}."
                         .format(self.settings.white_dice))


    def game_procces_cycle(self):
        """Run the game"""
        while True:
            if self.stats.dungeon_trip > self.settings.max_dungeon_trip:
                self._end_of_game()
            try:
                self._new_dungeon_level()
                self._action()
            except Defeat:
                self._leave_the_dungeon(exp=False)
            except Leave:
                self.print_delay('Вы восстанавливаете силы и '
                                 'готовитесь к следующему походу:')
                self._leave_the_dungeon()
    

    def _new_dungeon_level(self):
        """Creating new dungeon level"""

        #Clearing and creating new monsters
        self.dungeon.clear()
        self._create_dungeon()

        # Print info
        self._print_dungeon_info()


    def _create_dungeon(self):
        """Creating new monsters list"""
        # Calculating available dice
        available_dice = self.settings.black_dice - len(self.dragon_lair)

        # Limiting the number of dice 
        monster_num = min(available_dice, self.stats.dungeon_level)

        # Creating dungeon
        self.dungeon.add_unit(n=monster_num) # self.black_die.roll(monster_num) # ["Гоблин"] * 3 # ["Дракон", "Дракон", "Дракон", "Гоблин", "Зелье", "Зелье"] # 


    def _end_of_game(self):
        """End of game"""
        self.print_delay('-' * 100)
        self.print_delay("Игра закончена.\n")
        self.print_delay("Ваш опыт - {}.\n".format(self.hero.exp))
        self.print_delay("Начать игру заново? (да/нет)")

        while True:
            answer = input("Ваш ответ: ").lower()
            if answer == "да":
                self.reset_game()
                return
            elif answer == 'нет':
                sys.exit()
            else:
                self.print_delay('Некорректный ввод')


    def _print_party_info(self):
        """Print game info"""
        # Hero info
        self.print_delay(self.hero)
        # Party
        self.print_delay('Кубики партии - {}'.format(self.party))
        #Treasures
        if self.treasures:
            self.print_delay('Ваши сокровища - {}'.format(self.treasures))
        # Dungeon
        self.print_delay('Кубики подземелья - {}'.format(self.dungeon))
        # Dragon lair
        self.print_delay('Логово дракона - {}\n'.format(self.dragon_lair))


    def _print_dungeon_info(self):
        """Print trip and dungeon level"""
        self.print_delay('-'*100)
        self.print_delay('Поход №{}, Уровень подземелья {}.\n'
                         .format(self.stats.dungeon_trip, 
                                 self.stats.dungeon_level))


    def _dragon_lair(self):
        """Move dragons to dragon's lair"""

        # Choose the right form of "die"
        if self.dungeon.count("Дракон") == 1:
            dice_form = 'кубик'
        elif self.dungeon.count("Дракон") < 5:
            dice_form = 'кубика'
        elif self.dungeon.count("Дракон") >= 5:
            dice_form = 'кубиков'

        self.print_delay('{} {} "Дракон" перемещаются в логово дракона.\n'
                         .format(self.dungeon.count("Дракон"), dice_form))

        # Move dragons to lair
        while "Дракон" in self.dungeon:
            self.dragon_lair.append(self.dungeon.pop(self.dungeon.index('Дракон')))

        self._print_party_info()

        if len(self.dragon_lair) >= 3 and not self.stats.dragon_awake:
            self.print_delay('Дракон пробуждается!\n')
            self.stats.dragon_awake = True


    def _action(self):
        """Requests an action and calls needed method"""
        while True:
            self._print_party_info()
            # Moves dragons to dragons' lair
            if 'Дракон' in self.dungeon:
                self._dragon_lair()

            message, ACTIONS = self.__create_actions_message()
            print(*message, sep = ", ", end = '.\n')
            while True:
                try:
                    action = int(input("Ваш выбор: "))
                    print('')
                    if action > len(message): 
                        raise ValueError
                except ValueError:
                    print("Некорректный ввод")
                else:
                    # Actions
                    if action == ACTIONS['fight']:
                        self._battle()
                    elif action == ACTIONS['scroll']:
                        self._scroll()
                    elif action == ACTIONS['ability']:
                        self.hero.ability()
                    elif action == ACTIONS['treasure']:
                        self.treasures.use_noncombat()
                    elif action == ACTIONS['retreat']:
                        raise Defeat
                    #break


    def __create_actions_message(self):
        """ Create list that contains allowed actions
            and returs it with actions dictionary """
        # Prepare variables to create an action request.
        message = []
        ACTIONS = {"fight" : None,
                   "reward" : None,
                   "scroll" : None,
                   "ability" : None,
                   "treasure" : None,
                   "retreat" : None,
                   }
        action_number = 1

        # Create a request containing all your possibilities
        # Fight
        if self.dungeon.is_monsters() or self.stats.dragon_awake:
            message.append('Сражаться - {}'.format(action_number))
            ACTIONS['fight'] = action_number
            action_number += 1

        # Reward
        elif self.dungeon.is_reward():
            message.append('Получить награду - {}'.format(action_number))
            ACTIONS['reward'] = action_number
            action_number += 1

        # Scroll
        if "Свиток" in self.party:
            message.append('Использовать свиток - {}'.format(action_number))
            ACTIONS['scroll'] = action_number
            action_number += 1

        # Hero ability
        if self.hero.ability_check(usage='ability'):
            message.append('Использовать способность героя - {}'
                           .format(action_number))
            ACTIONS['ability'] = action_number
            action_number += 1

        # Treasure
        if self.treasures.is_noncombat():
            message.append('Использовать сокровище - {}'.format(action_number))
            ACTIONS['treasure'] = action_number
            action_number += 1

        # Reatreat
        message.append('Отступить - {}'.format(action_number))
        ACTIONS['retreat'] = action_number

        return message, ACTIONS


    def _battle(self):
        """Calls common figt or dragon fight"""
        if self.dungeon.is_monsters:
            self._fight()
        else:
            self._dragon_fight()

            
    def _fight(self):
        """Fighting with monsters"""
        if not self.combat_capability_check():
            print("Вы не можете сражаться.")
            raise Defeat

        print("Выберите сопартийца: ")
        unit = self._get_unit("Свиток")
        print("Выберите монстра: ")
        monster = self._get_item(self.dungeon, False, "Сундук", "Зелье")

        #Checks and kills
        self._check_and_kill(unit, monster)
        

    def _dragon_fight(self):
        """Fighting with a dragon"""
        # Creates set of party and removes scroll

        if not self.combat_capability_check(self.settings.dragon_slayers_number):
            print("Вы не можете победить дракона.")
            raise Defeat

        dragon_slayers = []

        self.print_delay("Битва с драконом!\n")

        # Choosing units who will fight with a dragon
        self.print_delay("Выбери сопартийцов, которые будут сражаться с драконом:")
        for i in range(self.settings.dragon_slayers_number):
            self.print_delay('Кубики подземелья - {}'.format(self.party))
            self.print_delay('Драконоборцы - {}'.format(dragon_slayers))

            dragon_slayer = self._get_unit("Свиток", *dragon_slayers)
            dragon_slayers.append(dragon_slayer)
            self.party.remove(dragon_slayer)

        self.print_delay('Драконоборцы - {}\n'.format(dragon_slayers))
        self.print_delay("Дракон побежден!\n")

        self.treasures.get_treasure()
        self.print_delay("Получена 1 ед. опыта\n")
        self.hero.get_exp()
        self.dragon_lair.clear()
        self.stats.dragon_awake = False


    def combat_capability_check(self, monsters_number=1):
        """Checks ability to kill a dragon"""

        # Create party set and remove scroll
        units = set(self.party)
        if "Свиток" in units:
            units.remove('Свиток')

        # Creating combat treasures set and transfom it to units
        combat_treasures_set = set(self.treasures) & self.treasures._combat_treasures
        treasures_to_units = {self.treasures._treasure_to_unit_dict[treasure] 
                              for treasure in combat_treasures_set}

        # Intersection 
        potential_dragon_slayers = units | treasures_to_units

        if self.hero.ability_check(usage='unit', del_units=potential_dragon_slayers):
            if (self.hero.units[0] not in potential_dragon_slayers
                    and self.hero.units[1] not in potential_dragon_slayers):
                potential_dragon_slayers.add(self.hero.units[0])

            elif self.hero.units[0] not in potential_dragon_slayers:
                potential_dragon_slayers.add(self.hero.units[0])

            elif self.hero.units[1] not in potential_dragon_slayers:
                potential_dragon_slayers.add(self.hero.units[1])

        return True if len(potential_dragon_slayers) >= monsters_number else False


    def _scroll(self):
        """Using a scroll"""
        self.party.remove("Свиток")
        white_reroll_list = []
        black_reroll_list = []

        while True:
            self.print_delay('Кубики партии - {}'.format(self.party))
            self.print_delay("Кубики партии, выбранные для переброса - {}"
                             .format(white_reroll_list))
            self.print_delay('Кубики подземелья - {}'.format(self.dungeon))
            self.print_delay('Кубики подземелья, выбранные для переброса - {}'
                             .format(black_reroll_list))
            self.print_delay('')

            black_and_white_list = self.party + self.dungeon
            if not black_and_white_list:
                break
            self.print_delay("Выберите кубик партии или подземелья, "
                             "который хотите перебросить:")
            item = self._get_item(black_and_white_list, back=True)
            if item == 'back':
                break
            elif item in self.party:
                white_reroll_list.append(self.party.pop(self.party.index(item)))
            elif item in self.dungeon:
                black_reroll_list.append(self.dungeon.pop(self.dungeon.index(item)))

        # Roll new items
        white_rerolled_list = self.white_die.roll(len(white_reroll_list))
        black_rerolled_list = self.black_die.roll(len(black_reroll_list))

        # Print transformation
        self.print_delay("Выбранные кубики партии {} перебрасываются в {}."
                         .format(white_reroll_list, white_rerolled_list))
        self.print_delay("Выбранные кубики подземелья {} перебрасыватюся в {}."
                         .format(black_reroll_list, black_rerolled_list))
        self.print_delay('')

        # Extends party and dungeon lists with new rolls of dice
        self.party.extend(white_rerolled_list)
        self.dungeon.extend(black_rerolled_list)


    def _reward(self):
        """Reward cycle"""
        self.print_delay("Время брать награду:\n")
        while "Сундук" in self.dungeon or "Зелье" in self.dungeon:
            self.print_delay('Кубики партии - {}'.format(self.party))
            self.print_delay('Кубики подземелья - {}\n'.format(self.dungeon))
            self.print_delay('Ваш выбор: ')

            action = self._get_item(self.dungeon, back=True)
            if action == 'back': break
            del_units = "Свиток" if action == "Сундук" else None

            print(("Выберите сопартийца, который ") + ("откроет сундуки:"
                  if action == "Сундук" else "выпьет зелья:"))
            unit = self._get_unit(del_units)
            self._kill_unit(unit)

            if action == "Сундук":
                self._chest(unit)
            elif action == "Зелье":
                self._potion()


    def _chest(self, unit):
        """Opens chests after battle and give truasure for every one"""

        # Guardians and thieves open all chests
        if unit in self.units_dict['thief'] or unit in self.units_dict['guardian']:
                self.treasures.get_treasure(self.dungeon.count("Сундук"))

        # Another units open one chest
        else:
            self.treasures.get_treasure()


    def _potion(self):
        """Drinking potions at the end of dungeon"""

        # Process of drinking and adding new units as long as there are potions and dice 
        while "Зелье" in self.dungeon and len(self.party) < 7:
            resurection_number = min((self.settings.white_dice - len(self.party), 
                                      self.dungeon.count("Зелье")))
            self.print_delay('Кубики партии - {}'.format(self.party))
            self.print_delay((('Вы можете вернуть еще {} ') + 
                              ('сопартийца' if resurection_number == 1 
                               else 'сопартиейцев') + '.\n')
                             .format(resurection_number))
            self.dungeon.remove("Зелье")
            self.print_delay('Кого хотите вернуть?')
            self.party.append(self._get_item(self.white_die.sides))

        # Revomes remaining potions
        while "Зелье" in self.dungeon:
            self.dungeon.remove("Зелье")


    def _regrouping(self):
        """Regrouping phase"""
        self.print_delay("\nВы зачистили подземелье!\n")
        self._print_party_info()

        if self.stats.dungeon_level == self.settings.max_dungeon_level:
            self.print_delay("Вы достигли максимального уровня подземелья!\n")
            self._leave_the_dungeon()

        else:
            while True:
                try:
                    self.print_delay("Отдых в таверне - 1, Идти дальше - 2.")
                    action = int(input("Ваш выбор: "))
                    print('')
                except ValueError:
                    self.print_delay("Некорректный ввод")
                else:
                    if action > 2:
                        raise ValueError
                    # Leave the dungeon
                    elif action == 1:
                        raise Leave

                    # New level
                    elif action == 2:
                        self.print_delay('Вы переходите к следующему уровню подземелья.\n')
                        self.stats.dungeon_level += 1
                    break


    def _leave_the_dungeon(self, exp=True):
        """Leave the dungeon and get experience"""
        if exp:
            self.print_delay('Получено {} ед. опыта за уровень подземелья.'
                             .format(self.stats.dungeon_level))

            if self.treasures:
                self.print_delay('Получено {} ед. опыта за сокровища.'
                                 .format(self.treasures.count_exp()))

            trip_exp = self.stats.dungeon_level + self.treasures.count_exp()
            self.hero.get_exp(trip_exp)

        else:
            self.print_delay("Вы вынуждены бежать из подземелья: "
                             "вы не получаете опыта за этот поход.")

        
        self.stats.dungeon_trip += 1
        self._reset_dungeon()


    def _get_item(self, items_list, back=False, *delete_items):
        """Choosing item from 'items_list' and return it
            return False if exception was raised"""
        unique_list = sorted(list(set(items_list)))

        # Deleting scrolls, chests and potions of necessity
        for item in delete_items:
            if item in unique_list:
                unique_list.remove(item)

        index = self._get_index_from_items_list(unique_list, back)

        return 'back' if index == 'back' else unique_list[index]


    def _get_unit(self, *del_units):
        """Get a unit from the party and treasures, if any"""
        unique_units = sorted(list(set(self.party)))

        # Deleting units
        for unit in del_units:
            if unit in unique_units:
                unique_units.remove(unit)

        # Get index
        request = self._get_index_from_items_list(
            unique_units, 
            treasure=self.treasures.is_combat(del_units),
            hero=self.hero.ability_check(usage='unit', del_units=del_units)
            )

        if isinstance(request, int):
            return unique_units[request]
        elif request == 'treasure':
            return self.treasures.use_combat(del_units)
        elif request == 'hero':
            return self.hero.ability(del_units)


    def _get_index_from_items_list(self, items_list:list, 
                                   back:bool=False, 
                                   treasure:bool=False, 
                                   hero:bool=False) -> int:

        """Creating a string of numbered items in a list
            if 'back' - add extra index to come back"""
        numbered_items_list = []
        aux_index = len(items_list)
        BACK = TREASURE = HERO = 0

        for index, item in enumerate(items_list, start=1):
            numbered_items_list.append(f'{item} - {index}')

        # Back option
        if back:
            aux_index += 1
            BACK = aux_index
            numbered_items_list.append(f'Далее - {aux_index}')
        # Possibility to use treasure while choosing unit
        if treasure:
            aux_index += 1
            TREASURE = aux_index
            numbered_items_list.append(f'Использовать сокровище - {aux_index}')
        # Possibility to use hero ability while choosing unit
        if hero:
            aux_index += 1
            HERO = aux_index
            numbered_items_list.append(f'Использовать способность героя - {aux_index}')

        print(*numbered_items_list, sep=', ', end='.\n')

        while True:
            print('Ваш выбор: ', end='')

            try:
                index = int(input())
                if index > aux_index or index <= 0:
                    raise ValueError
            except ValueError:
                print("Некорректный ввод")
            else:
                print('')
                if index <= len(items_list):
                    return index - 1
                elif index == BACK:
                    return 'back'
                elif index == TREASURE:
                    return 'treasure'
                elif index == HERO:
                    return 'hero'
              
                
    def _check_and_kill(self, unit, monster):
        """ Checks a unit and a monster interaction
            and kills monsters
        """
        assert (unit in self.white_die.sides and 
                monster in self.black_die.sides), "Для проверки юнит-монстр пришел не юнит"

        if (unit in self.units_dict['warrior'] and monster == "Гоблин" or
                unit in self.units_dict['cleric'] and monster == "Скелет" or
                unit in self.units_dict['mage'] and monster == "Слизень" or
                unit in self.units_dict['guardian']):
            self._kill_all(monster)
        else:
            self._kill_one(monster)

        self._kill_unit(unit)


    def _kill_all(self, monster):
        """Kill all monsters of the same type"""
        while monster in self.dungeon:
            self.dungeon.remove(monster)


    def _kill_one(self, monster):
        """Kill one monster"""
        self.dungeon.remove(monster)


    def _kill_unit(self, unit):
        """Moves a unit from the party to the cemetery"""
        self.party.remove(unit)


    def print_delay(self, message):
        """Print message and sleep"""
        print(message)
        sleep(self.settings.time_delay)