from adventure_chest import AdventureChest

list_ = ['hello', 'world', 'my', 'name']

ac_game = AdventureChest()
#ac_game.run()

while True:
    #print(ac_game._get_index_from_items_list(['hello', 'world', 'its', 'me'], back=True, hero=True, treasure=True))
    print(ac_game._get_unit("Воин"))


