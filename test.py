import pymorphy2

morph = pymorphy2.MorphAnalyzer()

monster = morph.parse('Монстра')[0]
print(monster)
print(monster.make_agree_with_number(2).word)



