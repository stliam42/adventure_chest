from treasures import Treasures
from adventure_chest import AdventureChest

#tr = Treasures(3)
#exp = tr.count_exp()
#print(tr._treasures)

#print(tr.is_combat(("Вор", "Свиток")))

#class DelegateAbility:

#    #def __init__(self):
#    #def __getattribute__(self, name):
#    #    return __print_units if name == __print_units else False

#    def __get__(self, instance, owner):
#        return instance.__dict__[ability]

#    def __print_units(self):
#        print(self.units)

#    def ability(self):
#        print(self.units)


#class Hero:

#    def __init__(self):
#        self.name = 'name'
#        self.units = ('war', 'mage')
#        self.ability = getattr(DelegateAbility(), ability)

#hero = Hero()
#print(hero.ability)
#hero.ability()

#class DelegateTo:
#    def __init__(self, to, method=None):
#        self.to = to
#        self.method = method

#    def __get__(self, obj, objecttype):
#        print('obj - ', obj)
#        print('to -', self.to)
#        print('-'*100)
#        print(obj.__class__.__dict__.items())

#        #return self.__info

#        if self.method is not None:
#            return getattr(getattr(obj, self.to), self.method)

#        for method, v in obj.__class__.__dict__.items():
#            print(method, v, self)
#            if v is self:
#                self.method = method
#                return getattr(getattr(obj, self.to), method)

#    def __info(self):
#        print(self.to)

#class Foo:
#    upper = DelegateTo('v', 'capitalize')
#    __len__ = DelegateTo('l')
#    __iter__ = DelegateTo('l')

#    def __init__(self):
#            self.v = 'world'
#            self.l = 100500


#foo = Foo()
#print(foo.upper())

class Ability:

    @staticmethod
    def unit_ability(units:tuple, ac_game:AdventureChest) -> unit:
        print(*(unit for unit in units))


class Hero:

    def __init__(self, name):
        self.name = name
        self.units = ('war', 'mage')
        
    def ability(self):
        Ability.unit_ability(self.units)

hero = Hero('Red')

hero.ability()