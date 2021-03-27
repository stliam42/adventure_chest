##import hero

#import pymorphy2

#morph = pymorphy2.MorphAnalyzer()

#name = morph.parse("Драконоборец")[0]
#print(name.inflect({'ablt'})[0].capitalize())

test_list = [1,2,3,4,5,6,1,5,4,3,2,1,5]

for i in range(len(test_list)):
    if test_list[i] == 1:
        index = i

test_list.pop(index)
