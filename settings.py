class Settings():
    """Settings for AC game"""

    def __init__(self):
        # Delay for printing messages
        self.time_delay = 0.1
        # Dice
        self.white_dice = 7
        self.black_dice = 7
        # Dungeon
        self.max_dungeon_level = 10
        self.max_dungeon_trip = 3
        self.dragon_slayers_number = 3 # Number of units who will slay a dragon

        # Hero
        self.random_hero = False

        # Game process
        self.reward_before_fight = False

    def show(self):
        """Display dungeon settings"""
        print("Текущие настройки подземелья:")
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
