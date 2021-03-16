import  group

party = group.Party()

party.add_unit(n=7)
print(party)

party.delete_unit('Вор')
print(party)

party.add_unit(unit='Воин')
print(party)

party.insert('Маг')
print(party)
