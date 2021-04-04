class Settings():
    """Settings for AC game"""

    DEFAULT = {'time_delay': 0.1,
               'dice': 7,
               'max_dungeon_level': 10,
               'max_dungeon_trip': 3,
               'random_hero': True,
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
        self.random_hero = True

    @property
    def is_default(self):
        """ Check if the settings are default"""
        return (True if (self.time_delay == Settings.DEFAULT['time_delay'] and 
                        self.white_dice == self.black_dice == Settings.DEFAULT['dice'] and
                        self.max_dungeon_level == Settings.DEFAULT['max_dungeon_level'] and
                        self.max_dungeon_trip == Settings.DEFAULT['max_dungeon_trip'] and
                        self.random_hero == Settings.DEFAULT['random_hero']) 
                else False)

    def show(self):
        """Display dungeon settings"""
        print("Текущие настройки:")
        print("Количество кубиков партии - {}."
                .format(self.white_dice))
        print("Количество кубиков подземелья - {}."
                .format(self.white_dice))
        print("Максимальный уровень подземелья - {}."
                .format(self.max_dungeon_level))
        print("Количество походов в подземелье - {}."
                .format(self.max_dungeon_trip))
        print("Случайный герой - " + ("да." if self.random_hero else "нет."))
        print('')

    def change(self, new_settings:dict):
        """ Change the settings"""
        self.time_delay = new_settings['time_delay']
        self.white_dice = new_settings['white_dice']
        self.black_dice = new_settings['black_dice']
        self.max_dungeon_level = new_settings['max_dungeon_level']
        self.max_dungeon_trip = new_settings['max_dungeon_trip']
        self.random_hero = new_settings['random_hero']

if __name__ == "main":
    main()
