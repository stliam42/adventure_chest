from time import sleep

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
            self._fight_options()
            if self.stats.dragon_awake:
                self._dragon_fight()
            self._reward()
            

    def _new_dungeon_level(self):
        """Creating new dungeon level"""
        # Inc level
        self.stats.dungeon_level += 1

        #Clearing and creating new monsters
        self.dungeon.clear()
        self._create_dungeon()

        # Print info
        self._print_dungeon_info()
        self._print_party_info()


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
        self._delay()

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
        self.dungeon = self.black_die.roll(monster_num) # ["Дракон", "Дракон", "Дракон", "Гоблин"] #


    def _print_party_info(self):
        """Print party and monsters lists"""
        print(f'Ваша команда - {self.party}')
        self._delay()
        print(f'Кубики подземелья - {self.dungeon}')
        self._delay()
        print(f'Логово дракона - {self.dragon_lair}')
        self._delay()
        print(f'Кладбище - {self.cemetery}\n')
        self._delay()


    def _print_dungeon_info(self):
        """Print trip and dungeon level"""
        print(f'Поход №{self.stats.trip_number}, Уровень подземелья {self.stats.dungeon_level}.')
        self._delay()


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
            item = self._get_item(black_and_white_list)
            if item == '':
                break
            elif item in self.white_die.sides:
                white_reroll_list.append(self.party.pop(self.party.index(item)))
            elif item in self.black_die.sides:
                black_reroll_list.append(self.dungeon.pop(self.dungeon.index(item)))

        # Extends party and dungeon lists with new members
        self.party.extend(self.white_die.roll(len(white_reroll_list)))
        self.dungeon.extend(self.black_die.roll(len(black_reroll_list)))

        self._print_party_info()


    def _potion(self):
        """Drinking potions at the end of dungeon"""
        # Chooses the member who will drink potions
        print('Выбери сопартийца, который выпьет зелья:')
        member = self._get_item(self.party)
        self._kill_the_member(member)

        # Process of drinking and adding new members
        while "Зелье" in self.dungeon and self.cemetery:
            self.dungeon.remove("Зелье")
            print('Кого вы хотите добавить?')
            self.party.append(self._get_item(self.white_die.sides))

        self._print_party_info()


    def _fight_options(self):
        """Fighting cycle"""
        while True:
            # Moves dragons to dragons' lair
            if 'Дракон' in self.dungeon:
                self._dragon_lair()

            # Break the cycle if no monsters left
            if ("Гоблин" not in self.dungeon and "Скелет" not in self.dungeon and 
                "Слизень" not in self.dungeon):
                break

            # Prepare variables to create an action request
            request = []
            action_number = 1

            # Create a request containing all your options
            # Fight option
            request.append(f'{action_number} - Сражаться')
            FIGHT = action_number
            action_number += 1
                
            # Scroll option
            if "Свиток" in self.party:
                request.append(f'{action_number} - Использовать свиток')
                SCROLL = action_number
                action_number += 1

            # Hero ability option
            if not self.stats.ability_used:
                request.append(f'{action_number} - Использовать способность героя')
                ABILITY = action_number
                action_number += 1

            # Treasure
            if self.treasures:
                request.append(f'{action_number} - Использовать сокровище')
                TRAESURE = action_number
                action_number += 1

            print(*request, sep = ", ", end = '.\n')
            action = int(input("Ваш выбор: "))

            # Actions
            if action == FIGHT:
                self._fight()
            elif action == SCROLL:
                self._scroll()

    def _fight(self):
        """ Fighting with monsters"""
        print("\nВыберите сопартийца: ")
        member = self._get_item(self.party, del_scroll=True)
        print("Выберите монстра: ")
        monster = self._get_item(self.dungeon, del_chest=True, del_potion=True)

        #Checks and kills
        self._check_and_kill(member, monster)
        
        self._print_party_info()

    def _dragon_fight(self):
        """ Fighting with a dragon"""
        # Creates set of party and removes scroll
        print("Битва с драконом!")
        self._delay()

        dragon_slayers = list(set(self.party))
        if "Свиток" in dragon_slayers:
            dragon_slayers.remove('Свиток')
        # Checks ability to fight
        if len(dragon_slayers) < self.settings.dragon_slayers_number:
            print("You can't fight with the dragon\n")
            return

        # Choosing member who will fight with a dragon
        print("Выбери сопартийцов, которые будут сражаться с драконом:")
        for i in range(self.settings.dragon_slayers_number):
            dragon_slayer = self._get_item(dragon_slayers)
            dragon_slayers.remove(dragon_slayer)
            self.party.remove(dragon_slayer)

        print("Дракон побежден!")
        self.dragon_lair.clear()


    def _reward(self):
        """Reward cycle"""
        while "Сундук" in self.dungeon or "Зелье" in self.dungeon:
            print('Чистим сундуки и зелья:')
            action = self._get_item(self.dungeon)
            if action == "Сундук":
                #self._chest() #create me
                break
            elif action == "Зелье":
                self._potion()

    def _check_and_kill(self, member, monster):
        """ Checks a member and a monster interaction
            and kills monsters
        """
        # Warrior
        if member == "Воин": 
            if monster == "Гоблин":
                self._kill_all(member, monster)
            else:
                self._kill_one(member, monster)
        # Cleric
        elif member == "Клирик":
            if monster == "Скелет":
                self._kill_all(member, monster)
            else:
                self._kill_one(member, monster)
        # Magician
        elif member == "Маг":
            if monster == "Слизень":
                self._kill_all(member, monster)
            else:
                self._kill_one(member, monster)
        # Theif
        elif member == "Вор":
            self._kill_one(member, monster)
        # Guardian
        elif member == "Страж":
            self._kill_all(member, monster)


    def _get_item(self, items_list, del_scroll=False, del_chest=False, del_potion=False):
        """Choosing item from 'items_list' and return it"""
        unique_list = sorted(list(set(items_list)))

        # Deleting scrolls, chests and potions of necessity
        if 'Свиток' in unique_list and  del_scroll:
            unique_list.remove('Свиток')
        if "Сундук" in unique_list and del_chest:
            unique_list.remove("Сундук")
        if "Зелье" in unique_list and del_potion:
            unique_list.remove("Зелье")

        try:
            item = unique_list[int(input(self._get_items_str(unique_list)))]
        except:
            return ''
        else:
            return item


    def _get_items_str(self, items_list):
        """Creating a string of numbered items in a list"""
        numbered_items = ""

        for i in range(len(items_list)):
            numbered_items += f'{items_list[i]} - {i}, '

        # Replace the last comma with a period
        numbered_items = numbered_items[::-1].replace(',', '.', 1)[::-1]
        
        numbered_items += '\n'

        return numbered_items


    def _kill_all(self, member, monster):
        """Kill all monsters of the same type"""
        self._kill_the_member(member)
        while monster in self.dungeon:
            self.dungeon.remove(monster)


    def _kill_one(self, member, monster):
        """Kill one monster"""
        self._kill_the_member(member)
        self.dungeon.remove(monster)

    def _delay(self):
        """Time delay"""
        sleep(self.settings.time_delay)

    def _kill_the_member(self, member):
        """Moves a member from the party to the cemetery"""
        self.cemetery.append(self.party.pop(self.party.index(member)))