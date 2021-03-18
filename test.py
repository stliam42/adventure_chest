import hero

import pymorphy2

morph = pymorphy2.MorphAnalyzer()

for i in range(10):
    print(morph.parse('перемещается')[0].make_agree_with_number(i).word)