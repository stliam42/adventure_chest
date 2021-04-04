from time import sleep
from random import choice


from group import Party, Dungeon, DragonLair
from stats import Stats
from settings import Settings
from treasures import Treasures
from exceptions import Defeat, Leave
import hero 
import pymorphy2; morph = pymorphy2.MorphAnalyzer()


class AdventureChest():
    """Adventure Chest game class"""

    def __init__(self):
        """Inintialization parametrs"""
        self.reset()

    def _reset_dungeon(self):
        """Reset dungeon"""
        self.party.create(number=self.settings.white_dice)
        self.dungeon.clear()
        self.dragon_lair.clear()
        self.stats.dungeon_level = 1
        #self.hero.reset_abilities()

    def reset(self):
        """Create game attributes"""
        # Game stats
        self.stats = Stats()

        # Game settings
        self.settings = Settings()

        # Treasures
        self.treasures = Treasures(self)

        # Units dictionary for heroes abilities
        self.units_dict = {"warrior" : ("Воин"), 
                           "cleric" : ("Клирик"), 
                           "mage" : ("Маг"), 
                           "thief": ("Вор"), 
                           "guardian" : ("Страж"),
                           "scroll" : ("Свиток"),
                           "super_unit" : (),
                           "temp_units" : [],
                           }

        # Groups
        self.party = Party()
        self.dungeon = Dungeon()
        self.dragon_lair = DragonLair()

        # Game mechanics
        self.dragon_slayers_number = 3 # Number of units who will slay a dragon
        self.reward_before_fight = False

    def start(self):
        """Game launch method. Greeting, settings and start"""
        self.print_delay("Добро пожаловать в \"Сундук приключений\"!")
        self.print_delay("Версия игры - 1.0.1.")
        while True:
            self.print_delay("1 - Играть, 2 - Настройки.")
            answer = self.input(2)
            if answer == 1:
                self.set_up()
                self.game_procces_cycle()
            elif answer == 2:
                self.change_settings()

    def set_up(self):
        """ Prepare game to play"""
        self.settings.show()
        # Get a hero
        self.hero = hero.get_hero(self, random = self.settings.random_hero)
        self.hero.introduce()
        # Use passive
        if not self.hero.is_passive_change_party:
            self.hero.passive()

    def change_settings(self):
        """ Offer to change settings"""
        self.settigs.show()

    def input(self, n:int) -> int:
        """ Input the number from 1 to n and return it"""
        while True:
            try:
                answer = int(input("Ваш выбор: "))
                print('')
                if answer > n or answer < 0:
                    raise ValueError
            except:
                self.print_delay("Некорректный ввод")
            else:
                return answer

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
        monster_number = min(available_dice, self.stats.dungeon_level)

        # Creating dungeon
        self.dungeon.add_unit(self.stats.dungeon_level)
        # self.dungeon.add_unit(units=
        #                      ["Гоблин"] * 3 + 
        #                      ["Скелет"] * 2 + 
        #                      ["Слизень"] * 0 + 
        #                      ["Дракон"] * 0 +
        #                      ["Зелье"] * 1 +
        #                      ["Сундук"] * 2)

    def _end_of_game(self):
        """End of game"""
        self.print_delay('-' * 100)
        self.print_delay("Игра закончена.\n")
        if self.treasures:
            treasure_exp = self.treasures.count_exp()
            self.print_delay('Получено {} ед. опыта за сокровища.'
                                .format(treasure_exp))

            self.hero.get_exp(treasure_exp, False)

        self.print_delay("За эту игру вы получили {} ед. опыта.\n".format(self.hero.exp))
        self.print_delay("Начать игру заново?"
                         "1 - да, 2 - нет.")

        answer = self.input(2)
        if answer == "да":
            self.reset()
            return
        elif answer == 'нет':
            sys.exit()


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

        # Move dragons to lair (morph is used for number matching)
        self.print_delay('{} {} "Дракон" {} в логово дракона.\n'
                         .format(self.dungeon.count("Дракон"), 
                                 morph.parse('кубик')[0].make_agree_with_number(self.dungeon.count("Дракон")).word,
                                 "перемещается" if self.dungeon.count("Дракон") == 1 else "перемещаются"))

        self.dragon_lair.extend(self.dungeon.move_dragons())

        self._print_party_info()

        if (len(self.dragon_lair) >= self.dragon_slayers_number 
            and not self.dragon_lair.is_awake):
            self.print_delay('Дракон пробуждается!\n')

    def _action(self):
        """Requests an action and calls needed method"""
        while True:
            self._print_party_info()
            # Active passive ability
            if not self.hero.is_passive_used and self.hero.is_passive_change_party:
                self.hero.passive()
                continue
            # Moves dragons to dragons' lair
            if 'Дракон' in self.dungeon:
                self._dragon_lair()
            # Leave the dangeon if it's empty
            if not self.dungeon and not self.dragon_lair.is_awake:
                self._regrouping()
                break

            message, ACTIONS = self.__create_action_possibilities()
            print(*message, sep = ", ", end = '.\n')
            action = self.input(len(message))

            # Actions
            if action == ACTIONS['fight']:
                self._fight()
            elif action == ACTIONS['scroll']:
                self._scroll()
            elif action == ACTIONS['ability']:
                self.hero.ability()
            elif action == ACTIONS['treasure']:
                self.treasures.use_noncombat()
            elif action == ACTIONS['reward']:
                self._reward()
            elif action == ACTIONS['retreat']:
                raise Defeat
            elif action == ACTIONS['continue']:
                self._regrouping()
                break

    def __create_action_possibilities(self):
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
                   "continue" : None
                   }

        action_number = 1

        # Create a request containing all your possibilities
        # Fight
        if self.dungeon.is_monsters() or self.dragon_lair.is_awake:
            message.append('Сражаться - {}'.format(action_number))
            ACTIONS['fight'] = action_number
            action_number += 1
        # Reward
        if (self.dungeon.is_reward() and (not self.dungeon.is_monsters() 
            and not self.dragon_lair.is_awake or self.reward_before_fight)):
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
        if self.dungeon.is_monsters() or self.dragon_lair.is_awake:
            message.append('Отступить - {}'.format(action_number))
            ACTIONS['retreat'] = action_number
        else:
            message.append('Продолжить - {}'.format(action_number))
            ACTIONS['continue'] = action_number

        return message, ACTIONS

    def _fight(self):
        """Calls common figt or dragon fight"""
        if self.dungeon.is_monsters():
            self._monster_fight()
        else:
            self._dragon_fight()
            
    def _monster_fight(self):
        """Fighting with monsters"""
        if not self.combat_capability_check():
            print("Вы не можете сражаться.")
            raise Defeat

        print("Выберите сопартийца: ")
        unit = self._get_unit(self.units_dict['scroll'])
        print("Выберите монстра: ")
        monster = self._get_item(self.dungeon, False, "Сундук", "Зелье")

        # Checks and kills
        self._check_and_kill(unit, monster)

        # Some heroer buffs unit and they can kill one more monster
        if unit in self.units_dict['super_unit']:
            print("Выберите дополнительного монстра: ")
            add_monster = self._get_item(self.dungeon, False, "Сундук", "Зелье")
            self.dungeon.kill_unit(add_monster)

    def _dragon_fight(self):
        """Fighting with a dragon"""
        # Creates set of party and removes scroll

        if not self.combat_capability_check(self.settings.dragon_slayers_number):
            print("Вы не можете победить дракона.")
            raise Defeat

        dragon_slayers = []

        self.print_delay("Битва с драконом!\n")
        self.print_delay("Для победы над драконом необходимо {} сопартийца."
                         .format(self.settings.dragon_slayers_number))

        # Choosing units who will fight with a dragon
        self.print_delay("Выбери сопартийцев, которые будут сражаться с драконом:")
        for i in range(self.settings.dragon_slayers_number):
            self.print_delay('Кубики подземелья - {}'.format(self.party))
            self.print_delay('Драконоборцы - {}'.format(dragon_slayers))

            dragon_slayer = self._get_unit(self.units_dict['scroll'], 
                                           *dragon_slayers)
            dragon_slayers.append(dragon_slayer)
            self.party.remove(dragon_slayer)

        self.print_delay('Драконоборцы - {}\n'.format(dragon_slayers))
        self.print_delay("Дракон побежден!\n")

        self.treasures.get_treasure()
        self.print_delay("Получена 1 ед. опыта.\n")
        self.hero.get_exp()
        self.dragon_lair.clear()

    def combat_capability_check(self, monsters_number=1):
        """Checks ability to kill a dragon"""

        # Create party set and remove scroll
        units = set(self.party)
        if "Свиток" in units:
            units.remove("Свиток")

        # Creating combat treasures set and transfom it to units
        combat_treasures_set = set(self.treasures) & self.treasures._combat_treasures
        treasures_to_units = {self.treasures._treasure_to_unit_dict[treasure] 
                              for treasure in combat_treasures_set}

        # Intersection 
        potential_monsters_slayers = units | treasures_to_units

        # Add a hero if it can be used as unit
        if self.hero.ability_check(usage='unit', del_units=potential_monsters_slayers):
            if (self.hero.units[0] not in potential_monsters_slayers
                    and self.hero.units[1] not in potential_monsters_slayers):
                potential_monsters_slayers.add(self.hero.units[0])

            elif self.hero.units[0] not in potential_monsters_slayers:
                potential_monsters_slayers.add(self.hero.units[0])

            elif self.hero.units[1] not in potential_monsters_slayers:
                potential_monsters_slayers.add(self.hero.units[1])

        # Add scrolls if your hero is Enchantress

        return (True if len(potential_monsters_slayers) + 
               (self.party.count('Свиток') if not self.units_dict['scroll'] else 0)
                >= monsters_number 
                else False)

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
        white_rerolled_list = [choice(self.party.units) for i in range(len(white_reroll_list))]
        black_rerolled_list = [choice(self.dungeon.units) for i in range(len(black_reroll_list))]

        # Print transformation
        if white_rerolled_list:
            self.print_delay("Выбранные кубики партии {} перебрасываются в {}."
                         .format(white_reroll_list, white_rerolled_list))
        if black_rerolled_list:
            self.print_delay("Выбранные кубики подземелья {} перебрасыватюся в {}."
                         .format(black_reroll_list, black_rerolled_list))
        self.print_delay('')

        # Extends party and dungeon lists with new rolls of dice
        self.party.extend(white_rerolled_list)
        self.dungeon.extend(black_rerolled_list)

    def _reward(self):
        """Reward cycle"""
        self.print_delay("Время брать награду:\n")

        # Create reward list. It needs for HalfGoblin.
        reward_dice = []
        

        while "Сундук" in self.dungeon or "Зелье" in self.dungeon:
            if "Зелье" in self.dungeon:
                reward_dice.append("Зелье")
            if "Сундук" in self.dungeon:
                reward_dice.append("Сундук")

            self.print_delay('Кубики партии - {}'.format(self.party))
            self.print_delay('Кубики подземелья - {}\n'.format(reward_dice))
            self.print_delay('Ваш выбор: ')

            action = self._get_item(reward_dice, back=True)

            if action == 'back': 
                break

            # Delete scroll if you chose chest
            del_units = (self.units_dict['scroll'] 
                         if action == "Сундук" else None)

            print(("Выберите сопартийца, который ") + ("откроет сундуки:"
                  if action == "Сундук" else "выпьет зелья:"))
            unit = self._get_unit(del_units)
            self.party.kill_unit(unit)
            reward_dice.clear()

            if action == "Сундук":
                self._chest(unit)
            elif action == "Зелье":
                self._potion()

    def _chest(self, unit):
        """Opens chests after battle and give truasure for every one"""

        # Guardians and thieves open all chests
        if unit in self.units_dict['thief'] or unit in self.units_dict['guardian']:
            while "Сундук" in self.dungeon:
                self.treasures.get_treasure()
                self.dungeon.remove("Сундук")

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
            self.party.append(self._get_item(self.party.units))

        # Revomes remaining potions
        while "Зелье" in self.dungeon:
            self.dungeon.remove("Зелье")

    def _regrouping(self):
        """Regrouping phase"""
        self.print_delay("Вы зачистили подземелье!\n")
        
        while self.units_dict['temp_units']:
            self.print_delay('{} покидает группу.\n'
                             .format(self.units_dict['temp_units'][0]))
            self.party.remove(self.units_dict['temp_units'][0])
            self.units_dict['temp_units'].pop(0)

        self._print_party_info()
        if self.stats.dungeon_level == self.settings.max_dungeon_level:
            self.print_delay("Вы достигли максимального уровня подземелья!\n")
            self._leave_the_dungeon()

        else:
            self.print_delay("Отдых в таверне - 1, Идти дальше - 2.")
            action = self.input(2)
            
            # Leave the dungeon
            if action == 1:
                raise Leave

            # New level
            elif action == 2:
                self.print_delay('Вы переходите к следующему уровню подземелья.\n')
                self.stats.dungeon_level += 1

    def _leave_the_dungeon(self, exp=True):
        """Leave the dungeon and get experience"""
        if exp:
            self.print_delay('Получено {} ед. опыта за уровень подземелья.'
                             .format(self.stats.dungeon_level))
            self.hero.get_exp(self.stats.dungeon_level)
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
            # There is an Enchantress passive which allows you to 
            # use scrolls like any type of units.
            if unique_units[request] == 'Свиток' and not self.units_dict['scroll']:
                self.print_delay("Выберите сопартийца, в качестве "
                                 "которого будет использован свиток:")
                unit = self._get_item(self.party.units, *del_units, 'Свиток')
                self.party.remove('Свиток')
                self.party.insert(0, unit)
                return unit
            else:
                # Remove temporary units from dictionary. Ability of some heroes
                if unique_units[request] in self.units_dict['temp_units']:
                    self.units_dict['temp_units'].remove(unique_units[request])
                return unique_units[request]

        elif request == 'treasure':
            return self.treasures.use_combat(del_units)
        elif request == 'hero':
            return self.hero.ability(del_units)

    def _get_index_from_items_list(self, 
                                   items_list:list, 
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

        index = self.input(aux_index)

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
        assert (unit in self.party.units and 
                monster in self.dungeon.units), ("Для проверки юнит-монстр пришел"
                                                 "не юнит или не монстр")

        if (unit in self.units_dict['warrior'] and monster == "Гоблин" or
                unit in self.units_dict['cleric'] and monster == "Скелет" or
                unit in self.units_dict['mage'] and monster == "Слизень" or
                unit in self.units_dict['guardian']):
            self.dungeon.kill_unit(unit=monster, all=True)
        else:
            self.dungeon.kill_unit(unit=monster)

        self.party.kill_unit(unit)

    def print_delay(self, message):
        """Print message and sleep"""
        print(message)
        sleep(self.settings.time_delay)


if __name__ == "main":
    main()