from time import sleep
import sys

from dice import White_die, Black_die
from statistics import Stats
from settings import Settings
from treasures import Treasures
from exceptions import Defeat, Leave


class AdventureChest():
    """Adventure Chest game class"""
    

    def __init__(self):
        """Inintialization parametrs"""

        # Game stats
        self.stats = Stats()

        # Game settings
        self.settings = Settings()

        # Dice
        self.white_die = White_die()
        self.black_die = Black_die()

        # Treasures
        self.treasures = Treasures(self)

        # Player's party, monters, cemetery and dragon lists
        self._reset()
        self.cemetery = []

        self._print_dungeon_settings()

    def _reset(self):
        """Reset lists and part of stats"""
        self.party = self.white_die.roll(self.settings.white_dice)
        self.dungeon = []
        self.dragon_lair = []
        self.stats.dungeon_level = 1
        #self.treasures.clear()


    def _print_dungeon_settings(self):
        """Display dungeon settings"""
        print("Ваш герой - ???")
        self.delay()
        print(f"Количество походов в подземелье - {self.settings.max_dungeon_trip}.")
        self.delay()
        print(f"Максимальный уровень подземелья - {self.settings.max_dungeon_level}.")
        self.delay()
        print(f"Количество кубиков партии - {self.settings.white_dice}.")
        self.delay()
        print(f"Количество кубиков подземелья - {self.settings.white_dice}.")
        self.delay()


    def run(self):
        """Run the game"""
        while True:
            if self.stats.dungeon_trip > self.settings.max_dungeon_trip:
                self._end_of_game()
            try:
                self._new_dungeon_level()
                self._battle()
                if "Сундук" in self.dungeon or "Зелье" in self.dungeon:
                    self._reward()
                self._regrouping()
            except Defeat:
                self._defeat()
            except Leave:
                print('Вы восстанавливаете силы и готовитесь к следующему походу:')
                self.delay()
                self._leave_the_dungeon()
    

    def _end_of_game(self):
        """End of game"""
        print('-' * 100)
        self.delay()
        print("Игра закончена.\n")
        self.delay()
        print(f"Ваш опыт - {self.stats.exp}.\n")
        self.delay()
        print("Начать игру заново? (да/нет)")
        self.delay()
        while True:
            answer = input("Ваш ответ: ").lower()
            if answer == "да":
                self.stats.reset()
                return
            elif answer == 'нет':
                sys.exit()
            else:
                print('Некорректный ввод')
                self.delay()


    def _new_dungeon_level(self):
        """Creating new dungeon level"""

        #Clearing and creating new monsters
        self.dungeon.clear()
        self._create_dungeon()

        # Print info
        self._print_dungeon_info()


    def _dragon_lair(self):
        """Move dragons to dragon's lair"""

        # Choose the right form of "die"
        if self.dungeon.count("Дракон") == 1:
            dice_form = 'кубик'
        elif self.dungeon.count("Дракон") < 5:
            dice_form = 'кубика'
        elif self.dungeon.count("Дракон") >= 5:
            dice_form = 'кубиков'

        print(f'{self.dungeon.count("Дракон")} {dice_form} "Дракон" перемещаются в логово дракона.\n')
        self.delay()

        # Move dragons to lair
        while "Дракон" in self.dungeon:
            self.dragon_lair.append(self.dungeon.pop(self.dungeon.index('Дракон')))

        self._print_party_info()

        if len(self.dragon_lair) >= 3 and not self.stats.dragon_awake:
            print('Дракон пробуждается!\n')
            self.stats.dragon_awake = True


    def _create_dungeon(self):
        """Creating new monsters list"""
        # Calculating available dice
        available_dice = self.settings.black_dice - len(self.dragon_lair)

        # Limiting the number of dice 
        monster_num = min(available_dice, self.stats.dungeon_level)

        # Creating dungeon
        self.dungeon = ["Дракон", "Дракон", "Дракон", "Гоблин", "Зелье", "Зелье"] # self.black_die.roll(monster_num) #   ["Сундук", "Сундук", "Сундук"] #  ["Зелье", "Зелье", "Зелье"] # 


    def _print_party_info(self):
        """Print game info"""
        # Party
        print(f'Кубики партии - {self.party}')
        self.delay()
        #Treasures
        if self.treasures:
            print(f'Ваши сокровища - {self.treasures}')
            self.delay()
        # Dungeon
        print(f'Кубики подземелья - {self.dungeon}')
        self.delay()
        # Dragon lair
        print(f'Логово дракона - {self.dragon_lair}\n')
        self.delay()


    def _print_dungeon_info(self):
        """Print trip and dungeon level"""
        print('-'*100)
        print(f'Поход №{self.stats.dungeon_trip}, Уровень подземелья {self.stats.dungeon_level}.\n')
        self.delay()


    def _scroll(self):
        """Using a scroll"""
        self.party.remove("Свиток")
        white_reroll_list = []
        black_reroll_list = []

        while True:
            print(f'Кубики партии - {self.party}')
            self.delay()
            print(f"Кубики партии, выбранные для переброса - {white_reroll_list}")
            self.delay()
            print(f'Кубики подземелья - {self.dungeon}')
            self.delay()
            print(f'Кубики подземелья, выбранные для переброса - {black_reroll_list}')
            self.delay()
            print('')

            black_and_white_list = self.party + self.dungeon
            if not black_and_white_list:
                break
            print("Выберете кубик партии или подземелья, который хотите перебросить:")
            self.delay()
            item = self._get_item(black_and_white_list, back=True)
            if not item:
                break
            elif item in self.party:
                white_reroll_list.append(self.party.pop(self.party.index(item)))
            elif item in self.dungeon:
                black_reroll_list.append(self.dungeon.pop(self.dungeon.index(item)))

        # Roll new items
        white_rerolled_list = self.white_die.roll(len(white_reroll_list))
        black_rerolled_list = self.black_die.roll(len(black_reroll_list))

        # Print transformation
        print(f"Выбранные кубики партии {white_reroll_list} перебрасываются в {white_rerolled_list}.")
        self.delay()
        print(f"Выбранные кубики подземелья {black_reroll_list} перебрасываюся в {black_rerolled_list}.")
        self.delay()
        print('')

        # Extends party and dungeon lists with new rolls of dice
        self.party.extend(white_rerolled_list)
        self.dungeon.extend(black_rerolled_list)


    def _action(self, fight):
        """Return number of action and dictionary (action-number)"""
        # Prepare variables to create an action request.
        request = []
        FIGHT=SCROLL=ABILITY=TREASURE=RETREAT=0
        action_number = 1

        # Create a request containing all your possibilities
        # Fight
        request.append(f'Сражаться - {action_number}')
        FIGHT = action_number
        action_number += 1
                
        # Scroll
        if "Свиток" in self.party:
            request.append(f'Использовать свиток - {action_number}')
            SCROLL = action_number
            action_number += 1

        # Hero ability
        if not self.stats.ability_used:
            request.append(f'Использовать способность героя - {action_number}')
            ABILITY = action_number
            action_number += 1

        # Treasure
        if self.treasures.is_noncombat():
            request.append(f'Использовать сокровище - {action_number}')
            TREASURE = action_number
            action_number += 1

        # Reatreat
        request.append(f'Отступить - {action_number}')
        RETREAT = action_number


        print(*request, sep = ", ", end = '.\n')
        while True:
            try:
                action = int(input("Ваш выбор: "))
                print('')
            except ValueError:
                print("Некорректный ввод")
            else:
                if action > action_number: raise ValueError

                # Actions
                if action == FIGHT:
                    fight()
                elif action == SCROLL:
                    self._scroll()
                elif action == ABILITY:
                    pass                                    #CREATE ME
                elif action == TREASURE:
                    self.treasures.use_noncombat()  #FIXME
                elif action == RETREAT:
                    raise Defeat
                break

    def _battle(self):
        """Battle cycle"""
        while True:
            self._print_party_info()

            # If you have no units - you lose
            if not self.party:
                raise Defeat

            # Moves dragons to dragons' lair
            if 'Дракон' in self.dungeon:
                self._dragon_lair()

            # Break the cycle if no monsters left
            if ("Гоблин" not in self.dungeon and "Скелет" not in self.dungeon and 
                "Слизень" not in self.dungeon and not self.stats.dragon_awake):
                break
            # Request an action with monsters fight
            elif ("Гоблин" in self.dungeon or "Скелет" in self.dungeon or 
                "Слизень" in self.dungeon):
                self._action(self._fight)
            # Request an action with dragon fight
            else:
                self._action(self._dragon_fight)

            
    def _fight(self):
        """Fighting with monsters"""
        if not self.combat_capability_check():
            print("Вы не можете сражаться.")
            raise Defeat

        print("Выберите сопартийца: ")
        self.delay()
        unit = self._get_unit("Свиток")
        print("Выберите монстра: ")
        self.delay()
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

        print("Битва с драконом!\n")
        self.delay()

        # Choosing units who will fight with a dragon
        print("Выбери сопартийцов, которые будут сражаться с драконом:")
        self.delay()
        for i in range(self.settings.dragon_slayers_number):
            print(f'Драконоборцы - {dragon_slayers}')
            self.delay()
            dragon_slayer = self._get_unit("Свиток", *dragon_slayers)
            dragon_slayers.append(dragon_slayer)
            self.party.remove(dragon_slayer)

        print(f'Драконоборцы - {dragon_slayers}\n')
        self.delay()
        print("Дракон побежден!\n")
        self.delay()

        self.treasures.get_treasure()
        print("Получена 1 ед. опыта\n")
        self.delay()
        self.stats.trip_exp += 1
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
        treasures_to_units = {self.treasures._treasure_to_unit_dict[treasure] for treasure in combat_treasures_set}

        # Intersection 
        potential_dragon_slayers = units | treasures_to_units

        return True if len(potential_dragon_slayers) >= monsters_number else False


    def _reward(self):
        """Reward cycle"""
        print("Получаем награду:\n")
        while "Сундук" in self.dungeon or "Зелье" in self.dungeon:
            print(f'Кубики подземелья - {self.dungeon}\n')
            self.delay()
            print('Ваш выбор: ')
            action = self._get_item(self.dungeon, back=True)
            if action == "Сундук":
                self._chest()
            elif action == "Зелье":
                self._potion()
            else:
                break


    def _potion(self):
        """Drinking potions at the end of dungeon"""
        # Chooses the units who will drink potions
        
        print('Выбери сопартийца, который выпьет зелья:')
        unit = self._get_unit()
        self._kill_the_unit(unit)

        # Process of drinking and adding new units as long as there are potions and dice 
        while "Зелье" in self.dungeon and len(self.party) < 7:
            resurection_number = min((self.settings.white_dice - len(self.party), 
                                      self.dungeon.count("Зелье")))
            print(f'Вы можете вернуть еще {resurection_number} сопартийца.\n')
            self.dungeon.remove("Зелье")
            print('Кого хотите вернуть?')
            self.party.append(self._get_item(self.white_die.sides))

        # Revomes remaining potions
        while "Зелье" in self.dungeon:
            self.dungeon.remove("Зелье")


    def _chest(self):
        """Opens chests after battle and give truasure for every one"""
        print('Выбери сопартийца, который откроет сундуки:')
        unit = self._get_unit("Свиток")

        # Guardians and thieves open all chests
        if unit == "Вор" or unit == "Страж":
            while "Сундук" in self.dungeon:
                self.treasures.get_treasure()

        # Another units open one chest
        else:
            self.treasures.get_treasure()

        self._kill_the_unit(unit)

    def _regrouping(self):
        """Regrouping phase"""
        print("Вы зачистили подземелье!\n")
        self.delay()

        if self.stats.dungeon_level == self.settings.max_dungeon_level:
            print("Вы достигли максимального уровня подземелья!\n")
            self.delay()
            self._leave_the_dungeon()

        else:
            while True:
                try:
                    print("Отдых в таверне - 1, Идти дальше - 2.")
                    self.delay()
                    action = int(input("Ваш выбор: "))
                    print('')
                except ValueError:
                    print("Некорректный ввод")
                else:
                    if action > 2:
                        raise ValueError
                    # Leave the dungeon
                    elif action == 1:
                        raise Leave

                    # New level
                    elif action == 2:
                        print('Вы переходите к следующему уровню подземелья.\n')
                        self.delay()
                        self.stats.dungeon_level += 1
                    break


    def _leave_the_dungeon(self, exp=True):
        """Leave the dungeon and get experience"""
        if exp:
            print(f'Получено {self.stats.dungeon_level} ед. опыта за уровень подземелья.')
            self.delay()
            print(f'Получено {self.treasures.count_exp()} ед. опыта за сокровища.')
            self.delay()
            self.stats.trip_exp = self.stats.dungeon_level + self.treasures.count_exp()
        else:
            self.stats.trip_exp = 0

        self.stats.exp += self.stats.trip_exp
        self.stats.dungeon_trip += 1
        self._reset()


    def _defeat(self):  #FIX ME
        """If you lose your trip - you have no exp"""
        print("Вы вынуждены бежать из подземелья: вы не получаете опыта за этот поход.")
        self.delay()
        self._leave_the_dungeon(exp=False)

    def _check_and_kill(self, unit, monster):
        """ Checks a unit and a monster interaction
            and kills monsters
        """
        assert unit in self.white_die.sides, "Пришло что-то не то"

        if (unit == "Воин" and monster == "Гоблин" or
                unit == "Клирик" and monster == "Скелет" or
                unit == "Маг" and monster == "Слизень" or
                unit == "Страж"):
            self._kill_all(monster)
        else:
            self._kill_one(monster)

        self._kill_the_unit(unit)


    def _get_item(self, items_list, back=False, *delete_items):
        """Choosing item from 'items_list' and return it
            return False if exception was raised"""
        unique_list = sorted(list(set(items_list)))

        # Deleting scrolls, chests and potions of necessity
        for item in delete_items:
            if item in unique_list:
                unique_list.remove(item)

        index = self._get_index_from_items_list(unique_list, back)

        return False if index == len(unique_list) else unique_list[index]


    def _get_unit(self, *del_units):
        """Get a unit from the party and treasures, if any"""
        unique_units = sorted(list(set(self.party)))

        # Deleting units
        for unit in del_units:
            if unit in unique_units:
                unique_units.remove(unit)

        # Get index
        index = self._get_index_from_items_list(unique_units, treasure=self.treasures.is_combat(del_units))
        return (self.treasures.use_combat(del_units) if index == len(unique_units)
                else unique_units[index])


    def _get_index_from_items_list(self, items_list: list, 
                                           back:bool=False, treasure:bool=False) -> int:
        """Creating a string of numbered items in a list
            if 'back' - add extra index to come back"""
        numbered_items_list = []

        for index, item in enumerate(items_list, start=1):
            numbered_items_list.append(f'{item} - {index}')

        if back:
            numbered_items_list.append(f'Далее - {len(items_list) + 1}')

        if treasure:
            numbered_items_list.append(f'Использовать сокровище - {len(items_list) + 1}')

        print(*numbered_items_list, sep=', ', end='.\n')

        while True:
            print('Ваш выбор: ', end='')

            try:
                index = int(input())
                if index > len(numbered_items_list):
                    raise ValueError
            except ValueError:
                print("Некорректный ввод")
            else:
                print('')
                return index - 1


    def _kill_all(self, monster):
        """Kill all monsters of the same type"""
        while monster in self.dungeon:
            self.dungeon.remove(monster)


    def _kill_one(self, monster):
        """Kill one monster"""
        self.dungeon.remove(monster)


    def delay(self):
        """Time delay"""
        sleep(self.settings.time_delay)


    def _kill_the_unit(self, unit):
        """Moves a unit from the party to the cemetery"""
        self.party.remove(unit)