class Settings():
    """Settings for AC game"""

    DEFAULT = {'time_delay': 0.7,
               'dice': 7,
               'max_dungeon_level': 10,
               'max_dungeon_trip': 3,
               }

    def __init__(self):
        self.reset()

    def reset(self):
        # Delay for printing messages
        self.time_delay = Settings.DEFAULT['time_delay']
        # Dice
        self.white_dice = Settings.DEFAULT['dice']
        self.black_dice = Settings.DEFAULT['dice']
        # Dungeon
        self.max_dungeon_level = Settings.DEFAULT['max_dungeon_level']
        self.max_dungeon_trip = Settings.DEFAULT['max_dungeon_trip']

        # Hero
        self.random_hero = False

    @property
    def is_default(self):
        """ Check if the settings are default"""
        return (True if (self.time_delay == Settings.DEFAULT['time_delay'] and 
                        self.white_dice == self.black_dice == Settings.DEFAULT['dice'] and
                        self.max_dungeon_level == Settings.DEFAULT['max_dungeon_level'] and
                        self.max_dungeon_trip == Settings.DEFAULT['max_dungeon_trip'] and
                        self.dragon_slayers_number == Settings.DEFAULT['dragon_slayers_number']) 
                else False)

    def show(self):
        """Display dungeon settings"""
        print("Текущие настройки:")
        print("Количество походов в подземелье - {}."
                .format(self.max_dungeon_trip))
        print("Максимальный уровень подземелья - {}."
                .format(self.max_dungeon_level))
        print("Количество кубиков партии - {}."
                .format(self.white_dice))
        print("Количество кубиков подземелья - {}."
                .format(self.white_dice))
        print("Случайный герой - " + ("да." if self.random_hero else "нет."))
        print('')

        

    def set(self):
        """ Change game settings """
        pass


    def request_settings(self):
        while True:
            try:
                print("1 - Пользовательские настройки, 2 - Использовать стандартные.")
                answer = int(input("Ваш выбор: "))
            except:
                self.print_delay("Некорректный ввод")
            else:
                if answer > 2:
                    raise ValueError
                elif answer == 1:
                    white_dice = int(input("Введите количество кубиков партии: "))
                    self.settings.white_dice = 0
                else:
                    break

if __name__ == "main":
    main()
