from adventure_chest import AdventureChest


ac_game = AdventureChest()
#ac_game.game_procces_cycle()




print(ac_game.hero.ability_check())
ac_game.hero.get_exp(5)

ac_game.dungeon = ["Гоблин", "Сундук", "Зелье"]*3
ac_game.party.create(3)
ac_game.treasures.get_treasure(5)

ac_game._print_party_info()

ac_game.hero.ability()

ac_game._print_party_info()





