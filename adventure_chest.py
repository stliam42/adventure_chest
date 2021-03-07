from time import sleep
import os

from dice import White_die, Black_die
from statistics import Stats
from settings import Settings
from treasures import Treasures

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

        # Player's party, monters, cemetery and dragon lists
        self.party = self.white_die.roll(self.settings.amount_of_dice)
        self.dungeon = []
        self.dragon_lair = []
        self.cemetery = []

        # Treasures
        self.treasures = Treasures(self)


    def run(self):
        """Run the game"""
        while True:
            self._new_dungeon_level()
            self._battle()
            if self.stats.dragon_awake:
                self._dragon_fight()
            if "Сундук" in self.dungeon or "Зелье" in self.dungeon:
                self._reward()

            

    def _new_dungeon_level(self):
        """Creating new dungeon level"""
        # Inc level
        self.stats.dungeon_level += 1

        #Clearing and creating new monsters
        self.dungeon.clear()
        self._create_dungeon()

        # Clear text
        # os.system('cls||clear')

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
        available_dice = self.settings.amount_of_dice - len(self.dragon_lair)

        # Limiting the number of dice 
        monster_num = min(available_dice, self.stats.dungeon_level)

        # Creating dungeon
        self.dungeon = ["Дракон", "Дракон", "Дракон", "Гоблин"] # self.black_die.roll(monster_num) # ["Сундук", "Сундук", "Сундук"] #  ["Зелье", "Зелье", "Зелье"] # 


    def _print_party_info(self):
        """Print game info"""
        # Party
        print(f'\nВаша команда - {self.party}')
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

        self.delay()


    def _print_dungeon_info(self):
        """Print trip and dungeon level"""
        print('-'*100)
        print(f'Поход №{self.stats.trip_number}, Уровень подземелья {self.stats.dungeon_level}.')
        self.delay()


    def _scroll(self):
        """Using a scroll"""
        self.party.remove("Свиток")
        white_reroll_list = []
        black_reroll_list = []

        while True:
            black_and_white_list = self.party + self.dungeon
            if not black_and_white_list:
                break
            print("Выберете кубик партии или подземелья(оставьте ввод пустым если выбор окончен): ")
            item = self._get_item(black_and_white_list, True)
            if item == False:
                break
            elif item in self.white_die.sides:
                white_reroll_list.append(self.party.pop(self.party.index(item)))
            elif item in self.black_die.sides:
                black_reroll_list.append(self.dungeon.pop(self.dungeon.index(item)))

        # Extends party and dungeon lists with new rolls of dice
        self.party.extend(self.white_die.roll(len(white_reroll_list)))
        self.dungeon.extend(self.black_die.roll(len(black_reroll_list)))

        self._print_party_info()

    def _action(self, fight):
        """Return number of action and dictionary (action-number)"""
        # Prepare variables to create an action request.
        request = []
        actions_dict = {}
        action_number = 1

        # Create a request containing all your options
        # Fight option
        request.append(f'{action_number} - Сражаться')
        actions_dict['FIGHT'] = action_number
        action_number += 1
                
        # Scroll option
        if "Свиток" in self.party:
            request.append(f'{action_number} - Использовать свиток')
            actions_dict['SCROLL'] = action_number
            action_number += 1

        # Hero ability option
        if not self.stats.ability_used:
            request.append(f'{action_number} - Использовать способность героя')
            actions_dict['ABILITY'] = action_number
            action_number += 1

        # Treasure
        if self.treasures:
            request.append(f'{action_number} - Использовать сокровище')
            actions_dict['TREASURE'] = action_number
            action_number += 1

        print(*request, sep = ", ", end = '.\n')
        action = int(input("Ваш выбор: "))

        # Actions
        if action == actions_dict['FIGHT']:
            fight()
        elif action == actions_dict['SCROLL']:
            self._scroll()
        elif action == actions_dict['ABILITY']:
            pass                                    #CREATE ME
        elif action == actions_dict['TREASURE']:
            self.treasures.use(type='non-combat')   #FIXME


    def _battle(self):
        """Battle cycle"""
        while True:
            self._print_party_info()
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
        print("\nВыберите сопартийца: ")
        unit = self._get_unit("Свиток")
        print("Выберите монстра: ")
        monster = self._get_item(self.dungeon, False, "Сундук", "Зелье")

        #Checks and kills
        self._check_and_kill(unit, monster)
        


    def _dragon_fight(self):
        """Fighting with a dragon"""
        # Creates set of party and removes scroll
        print("\nБитва с драконом!")
        self.delay()

        dragon_slayers = list(set(self.party))
        if "Свиток" in dragon_slayers:
            dragon_slayers.remove('Свиток')

        # Checks ability to fight
        if len(dragon_slayers) < self.settings.dragon_slayers_number:
            print("You can't fight with the dragon\n")
            return

        # Choosing units who will fight with a dragon
        print("Выбери сопартийцов, которые будут сражаться с драконом:")
        for i in range(self.settings.dragon_slayers_number):
            dragon_slayer = self._get_item(dragon_slayers)
            dragon_slayers.remove(dragon_slayer)
            self.party.remove(dragon_slayer)

        print("Дракон побежден!")
        self.dragon_lair.clear()
        self.stats.dragon_awake = False


    def _reward(self):
        """Reward cycle"""
        print("Получаем награду:")
        while "Сундук" in self.dungeon or "Зелье" in self.dungeon:
            print(f'Кубики подземелья - {self.dungeon}')
            self.delay()
            print('Ваш выбор: ')
            action = self._get_item(self.dungeon, True)
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
            print(f'Вы можете вернуть еще {self.settings.self.amount_of_dice - len(self.party)}сопартийца')
            self.dungeon.remove("Зелье")
            print('Кого хотите вернуть?')
            self.party.append(self._get_item(self.white_die.sides))

        # Revomes remaining potions
        while "Зелье" in self.dungeon:
            self.dungeon.remove("Зелье")

        self._print_party_info()


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
        try:
            index = int(input(self._get_items_str(unique_list, back)))
        except ValueError:
            print("Некорректный ввод")
        else:
            return False if index == len(unique_list) else unique_list[index]

    def _get_unit(self, *del_units):
        """Get a unit from the party and treasures, if any"""
        unique_units = sorted(list(set(self.party)))

        # Deleting units
        for unit in del_units:
            if unit in unique_units:
                unique_units.remove(unit)

        try:
            index = int(input(self._get_items_str(unique_units, treasure=self.treasures.is_combat)))
        except ValueError:
            print("Некорректный ввод")
        else:
            return (self.treasures.use_combat(del_units) if index == len(unique_units)
                    else unique_units[index])


    def _get_items_str(self, items_list, back=False, treasure=False):
        """Creating a string of numbered items in a list
            if 'back' - add extra index to come back"""
        numbered_items = ""

        for index, item in enumerate(items_list):
            numbered_items += f'{item} - {index}, '

        if back:
            numbered_items += f'Назад - {len(items_list)}, ' 

        if treasure:
            numbered_items += f'Использовать сокровище - {len(items_list)}, '

        # Replace the last comma with a period
        numbered_items = numbered_items[::-1].replace(',', '.', 1)[::-1]
        
        numbered_items += '\n'

        return numbered_items


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
        self.cemetery.append(self.party.pop(self.party.index(unit)))