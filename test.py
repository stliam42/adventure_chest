class MinMaxWordFinder:
    def __init__(self):
        self.short = []
        self.long = ['']
    
    def add_sentence(self, sentence):
        words = sentence.split()
        longest_word_lenght = max(map(len, words))
        shortest_word_lenght = min(map(len, words))
        
        longest_words = [word for word in words if len(word) == longest_word_lenght]
        shortest_words = [word for word in words if len(word) == shortest_word_lenght]

        for i in words:
            #Longest words
            if len(i) == maxi:
                if self.long[-1] != i and len(self.long[-1]) == len(i):
                    self.long.append(i)
                elif len(self.long[-1]) < len(i):
                    self.long.clear()
                    self.long.append(i)
            # Shortest words
            if len(i) == mini:
                if self.short == []:
                    self.short.append(i)
                elif self.short[-1] != i and len(self.short[-1]) == len(i):
                    self.short.append(i)
                elif len(self.short[-1]) > len(i):
                    self.short.clear()
                    self.short.append(i)
                
    def shortest_words(self):
        return sorted(self.short)
    
    def longest_words(self):
        return sorted(self.long)

    def print_info(self):
        print(' '.join(self.short))
        print(' '.join(self.long))


finder = MinMaxWordFinder()
#finder.add_sentence('hello')
finder.print_info()
#finder.add_sentence('abc')
#finder.print_info()
#finder.add_sentence('world')
#finder.print_info()
#finder.add_sentence('def')
#finder.print_info()
#finder.add_sentence('asdf')
#finder.print_info()
#finder.add_sentence('qwert')
#finder.print_info()
#finder.add_sentence('abc')
#finder.print_info()
#finder.add_sentence('qwerty')
#finder.print_info()

