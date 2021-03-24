#import hero

import pymorphy2

morph = pymorphy2.MorphAnalyzer()

name = morph.parse("Драконоборец")[0]
print(name.inflect({'ablt'})[0].capitalize())