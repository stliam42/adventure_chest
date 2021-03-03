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
        self.dungeon = self.black_die.roll(monster_num) # ["Сундук", "Сундук", "Сундук"] # ["Дракон", "Дракон", "Дракон", "Гоблин"] # ["Зелье", "Зелье", "Зелье"] # 


    def _print_party_info(self):
        """Print game info"""
        # Party
        print(f'Ваша команда - {self.party}')
        self.delay()
        #Treasures
        if self.treasures:
            print(f'Ваши сокровища - {self.treasures}')
            self.delay()
        # Dungeon
        print(f'Кубики подземелья - {self.dungeon}')
        self.delay()
        # Dragon lair
        print(f'Логово дракона - {self.dragon_lair}')
        self.delay()
        # Cemetery
        print(f'Кладбище - {self.cemetery}\n')
        self.delay()


    def _print_dungeon_info(self):
        """Print trip and dungeon level"""
        print('-'*100)
        print(f'Поход №{self.stats.trip_number}, Уровень подземелья {self.stats.dungeon_level}.')
        self.delay()


    def _scroll(self):
        """Using a scroll"""
        self.cemetery.append(self.party.pop(self.party.index("Свиток")))
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

        # Extends party and dungeon lists with new members
        self.party.extend(self.white_die.roll(len(white_reroll_list)))
        self.dungeon.extend(self.black_die.roll(len(black_reroll_list)))

        self._print_party_info()


    def _battle(self):
        """Battle cycle"""
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
            FIGHT = SCROLL = ABILITY = TREASURE = 0

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
                TREASURE = action_number
                action_number += 1

            print(*request, sep = ", ", end = '.\n')
            action = int(input("Ваш выбор: "))

            # Actions
            if action == FIGHT:
                self._fight()
            elif action == SCROLL:
                self._scroll()
            elif action == ABILITY:
                pass
            elif action == TREASURE:
                self.treasures.use(type='non-combat')

    def _fight(self):
        """Fighting with monsters"""
        print("\nВыберите сопартийца: ")
        member = self._get_item(self.party, False, "Свиток")
        print("Выберите монстра: ")
        monster = self._get_item(self.dungeon, False, "Сундук", "Зелье")

        #Checks and kills
        self._check_and_kill(member, monster)
        
        self._print_party_info()

    def _dragon_fight(self):
        """Fighting with a dragon"""
        # Creates set of party and removes scroll
        print("Битва с драконом!")
        self.delay()

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
        # Chooses the member who will drink potions
        print('Выбери сопартийца, который выпьет зелья:')
        member = self._get_item(self.party)
        self._kill_the_member(member)

        # Process of drinking and adding new members as long as there are potions and dice 
        while "Зелье" in self.dungeon and self.cemetery:
            self.dungeon.remove("Зелье")
            print('Кого вы хотите добавить?')
            self.party.append(self._get_item(self.white_die.sides))
            self.cemetery.pop()

        # Revomes remaining potions
        while "Зелье" in self.dungeon:
            self.dungeon.remove("Зелье")

        self._print_party_info()


    def _chest(self):
        """Opens chests after battle"""
        print('Выбери сопартийца, который откроет сундуки:')
        member = self._get_item(self.party, True, "Свиток")

        # Break if get_item returned False
        if not member:
            return
        # Guardians and thieves open all chests
        if member == "Вор" or member == "Страж":
            while "Сундук" in self.dungeon:
                self.treasures.get_treasure()

        # Another members open one chest
        else:
            self.treasures.get_treasure()

        self._kill_the_member(member)


    def _check_and_kill(self, member, monster):
        """ Checks a member and a monster interaction_d
            and kills monsters
        """
        assert member in self.white_die.sides, "Пришло что-то не то"

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

        self._kill_the_member(member)

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

    def get_member(self, members_list):
        """Get a member from the member list and treasure list, if any"""
        pass


    def _get_items_str(self, items_list, back):
        """Creating a string of numbered items in a list
            if 'back' - add extra index to come back"""
        numbered_items = ""

        for i in range(len(items_list)):
            numbered_items += f'{items_list[i]} - {i}, '

        if back:
            numbered_items += f'Назад - {len(items_list)}, ' 

        # Replace the last comma with a period
        numbered_items = numbered_items[::-1].replace(',', '.', 1)[::-1]
        
        numbered_items += '\n'

        return numbered_items


    def _kill_all(self, member, monster):
        """Kill all monsters of the same type"""
        while monster in self.dungeon:
            self.dungeon.remove(monster)


    def _kill_one(self, member, monster):
        """Kill one monster"""
        self.dungeon.remove(monster)


    def delay(self):
        """Time delay"""
        sleep(self.settings.time_delay)


    def _kill_the_member(self, member):
        """Moves a member from the party to the cemetery"""
        self.cemetery.append(self.party.pop(self.party.index(member)))