from time import sleep

from dice import White_die, Black_die
from statistics import Stats
from settings import Settings

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

        # Player's party, monters, cemetry and dragon lists
        self.party = self.white_die.roll(self.settings.amount_of_dice)
        self.dungeon = []
        self.dragon = []
        self.cemetry = []


    def run(self):
        """Run the game"""
        while True:
            self._new_dungeon_level()

            #Fighting cycle
            while "Гоблин" in self.dungeon or "Скелет" in self.dungeon or "Слизень" in self.dungeon:
                if 'Дракон' in self.dungeon:
                    self._dragon_lair()
                request = 1
                if "Свиток" in self.party:
                    request = int(input('1 - Деремся, 2 - Используем свиток\n'))
                if request == 1:
                    self._fight()
                elif request == 2:
                    self._scroll()

            # Reward cycle
            while "Сундук" in self.dungeon or "Зелье" in self.dungeon:
                print('Чистим сундуки и зелья:')
                request = self._get_item(self.dungeon)
                if request == "Сундук":
                    break
                elif request == "Зелье":
                    self._potion()
            

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

        # Move dragons to lair
        while "Дракон" in self.dungeon:
            self.dragon.append(self.dungeon.pop(self.dungeon.index('Дракон')))

        self._print_party_info()

        if len(self.dragon) >= 3 and not self.stats.dragon_awake:
            print('Дракон пробуждается!\n')
            self.stats.dragon_awake = True


    def _create_dungeon(self):
        """Creating new monsters list"""
        # Calculating available dice
        available_dice = self.settings.amount_of_dice - len(self.dragon)
        # Limiting the number of dice 
        if self.stats.dungeon_level > self.settings.amount_of_dice:
            monster_num = self.settings.amount_of_dice
        else:
            monster_num = self.stats.dungeon_level

        # Roll all available dice
        if monster_num > available_dice:
            monster_num = available_dice

        # Creating monsters
        self.dungeon = self.black_die.roll(monster_num)


    def _print_party_info(self):
        """Print party and monsters lists"""
        print(f'Ваша команда - {self.party}')
        sleep(self.settings.time_delay)
        print(f'Кубики подземелья - {self.dungeon}')
        sleep(self.settings.time_delay)
        print(f'Логово дракона - {self.dragon}')
        sleep(self.settings.time_delay)
        print(f'Кладбище - {self.cemetry}\n')
        sleep(self.settings.time_delay)


    def _print_dungeon_info(self):
        """Print trip and dungeon level"""
        print(f'Поход №{self.stats.trip_number}, Уровень подземелья {self.stats.dungeon_level}.')
        sleep(self.settings.time_delay)


    def _scroll(self):
        """Using a scroll"""
        self.party.remove("Свиток")
        white_reroll_list = []
        black_reroll_list = []

        while True:
            black_and_white = self.party + self.dungeon
            print("Выберете кубик партии или подземелья(оставьте ввод пустым если выбор окончен): ")
            request = self._get_item(black_and_white)
            if request == '':
                break
            elif request in self.white_die.sides:
                white_reroll_list.append(self.party.pop(self.party.index(request)))
            elif request in self.black_die.sides:
                black_reroll_list.append(self.dungeon.pop(self.dungeon.index(request)))

        self.party.extend(self.white_die.roll(len(white_reroll_list)))
        self.dungeon.extend(self.black_die.roll(len(black_reroll_list)))
        self._print_party_info()

    def _potion(self):
        """Drink potions at the end of dungeon"""
        print('Вебери сопартийца, который возьмет зелья:')
        request = self._get_item(self.party)
        self.party.remove(request)
        while "Зелье" in self.dungeon:
            self.dungeon.remove("Зелье")
            print('Кого вы хотите добавить?')
            self.party.append(self._get_item(self.white_die.sides))
        self._print_party_info()


    def _fight(self):
        """Fighting"""
        print("Выберите сопартийца: ")
        member = self._get_item(self.party, del_scroll=True)
        print("Выберите монстра: ")
        monster = self._get_item(self.dungeon, del_chest=True, del_potion=True)

        # Check warior-monster
        if member == "Воин" and monster == "Гоблин":
            self._kill_all(member, monster)
        elif member == "Воин":
            self._kill_one(member, monster)

        # Check cleric-monster
        if member == "Клирик" and monster == "Скелет":
            self._kill_all(member, monster)
        elif member == "Клирик":
            self._kill_one(member, monster)

        # Check magician-monster
        if member == "Маг" and monster == "Слизень":
            self._kill_all(member, monster)
        elif member == "Маг":
            self._kill_one(member, monster)

        # Check thief-monster
        if member == "Вор":
            self._kill_one(member, monster)

        # Check guardian-monster
        if member == "Страж":
            self._kill_all(member, monster)
        
        self._print_party_info()


    def _get_item(self, list_, del_scroll=False, del_chest=False, del_potion=False):
        """ Choosing member and monster"""
        list_set = list(set(list_))

        while ('Свиток' in list_set and del_scroll or "Сундук" in list_set and del_chest 
               or "Зелье" in list_set and del_potion):
            if 'Свиток' in list_set and  del_scroll:
                list_set.remove('Свиток')
            elif "Сундук" in list_set and del_chest:
                list_set.remove("Сундук")
            elif "Зелье" in list_set and del_potion:
                list_set.remove("Зелье")

        request_str = self._get_items_str(list_set)

        try:
            item = list_set[int(input(request_str))]
        except:
            return ''
        else:
            return item

    def _get_items_str(self, list_):
        """ Creating string for list's item"""
        items_str = ""

        for i in range(len(list_)):
            items_str += f'{list_[i]} - {i}, '

        # Replace the last comma with a period
        items_str = items_str[::-1].replace(',', '.', 1)[::-1]
        
        items_str += '\n'

        return items_str

    def _kill_all(self, member, monster):
        """Kill all monsters of the same type"""
        self.cemetry.append(self.party.pop(self.party.index(member)))
        while monster in self.dungeon:
            self.dungeon.remove(monster)

    def _kill_one(self, member, monster):
        """Kill one monster"""
        self.cemetry.append(self.party.pop(self.party.index(member)))
        self.dungeon.remove(monster)


