from random import randint
database = 'words_for_repeat.txt'
repeat_time = 8 #начальное значение теста, в котором попадется слово для повторения

#WHEN I FINISH WORK, I WILL TRANSLATE ALL COMMENTS FROM RUSSIAN TO ENGLISH

class Card:
    """Constructor, 4 properties and __eq__"""
    def __init__(self, word: str, translate: str, level: int, time_repeat=repeat_time):
        """Constructor accept word, its translate and the hard level"""
        if word == '':
            raise ValueError
        if translate == '':
            raise ValueError
        self._word = word
        self._translate = translate
        self._level = level
        self._repeat = time_repeat
    
    def __str__(self):
        return self._word

    @property
    def word(self):
        return self._word

    @property
    def translate(self):
        return self._translate

    @property
    def level(self):
        return self._level
    
    @property
    def repeat(self):
        return self._repeat

    def __eq__(self, __o: object) -> bool:
        if (self._word==__o._word and self._translate==__o._translate and self._level == __o._level and self._repeat == __o._repeat):
            return True


class Round:
    """Functions:
        1. check_result
        2. choose random words
        3. writing words in file
        4. import new word
        5. export new word
        5. delete word
        6. define new word
        Constructor:
        It takes cards number and time of test, also the cards list is created"""
    def __init__(self, number_cards, time):
        """!
            """
        self._time = time
        self._number_cards = number_cards
        self._cards = []
 

    @property
    def number_of_cards(self):
        return self._number_cards

    @number_of_cards.setter
    def number_of_cards(self, value):
        self._number_cards = value

    @property
    def time(self):
        return self._time

    @property
    def cards(self):
        return self._cards
    
    def check_result(self, sorted_cards, sorted_translate, time):
        """Two conditions of winning:
        1. The test time is less tham the predicated time
        2. All words are done correctly"""
        bad_words = []
        # good_words = []
        if time > self._time:
            return sorted_cards
        for pair_card in zip(sorted_cards, sorted_translate):
            if pair_card[0]._translate != pair_card[1]:
                bad_words.append(pair_card[0])
            # else:
            #     good_words.append(pair_card[0])
        return bad_words

    def words_for_repeat(self, words, file=database):
        """Writing test word to the file.
            The repeat of the test words are increasing in 4 times.
            The repeat of not test word are decreasing in 2 times
            If the repeat of not test word equals 1, nothing to do"""
        all_lines = []
        with open(file, 'r+') as f:
            all_lines = f.readlines()
            f.seek(0)
            f.truncate()
        all_words = []
        for line in all_lines:
            parts = line.split('-')
            word, translate, level, repeat = parts[0], parts[1], parts[2], parts[3].rstrip(),
            card = Card(word, translate, int(level), int(repeat))
            all_words.append(card)
        flag = 0
        for card in all_words:
            for test_word in words:
                if card._word == test_word._word:
                    card._repeat = 4 * card._repeat
                    flag = 1
            if flag == 0:
                if card._repeat == 1:
                    continue
                else:
                    card._repeat = int(card._repeat / 2)
        new_words = []
        for card in all_words:
            new_words.append(f'{card.word}-{card.translate}-{card.level}-{card.repeat}\n')
        with open(file, 'w') as f:
            f.write("".join(new_words))
        return all_words


    def export_card(self, card: Card, file=database):
        """Define and export new word
            Check the condtion that the exported word does not exist
            If it does not exist, write to the file"""
        with open(file, 'r+') as f:
            all_lines = f.readlines()
            f.seek(0)
            f.truncate()
            for line in all_lines:
                parts = line.split('-')
                it_word, it_translate, it_level, it_repeat = parts[0], parts[1], parts[2], parts[3]
                if (it_word == card.word):
                    f.write("".join(all_lines))
                    raise ValueError
            all_lines.append(f'{card._word}-{card._translate}-{card._level}-{card._repeat}\n')
            # for line in all_lines:
            #     f.write(line)
            f.write("".join(all_lines))

    def import_card(self, cards, file=database):
        """Import takes cards of current test.
            We choose the random word in the file until we find not tested word"""
        with open(file, 'r') as f:
            all_lines = f.readlines()
            line_count = len(all_lines)
            random_line = randint(0, line_count-1)
            pair = all_lines[random_line]
            parts = pair.split('-')
            word, translate, level, repeat = parts[0], parts[1], parts[2], parts[3].rstrip(), 
            card = Card(word, translate, int(level))
            while card in cards:
                random_line = randint(0, line_count-1)
                pair = all_lines[random_line]
                parts = pair.split('-')
                word, translate, level, repea0 = parts[0], parts[1], parts[2], parts[3].rstrip()
                card = Card(word, translate, int(level))
            cards.append(card)
            return cards

    def define_new_card(self, word, translate, level: int, cards):
        """Define new card takes word, translate and level, cards"""
        if (word == "" or translate == ""):
            raise ValueError
        for card in cards:
            if (card.word == word):
                raise ValueError
        card = Card(word, translate, level)
        cards.append(card)
        return cards

    def delete_card(self, card: Card, file = database): 
        """Deleting card takes cards. (It is not used in design, because I think 
        the user have not to change the database, but it is implemented
        1. takes card to delete
        2. rewrite all file without this card"""
        all_words = []
        with open(file, 'r+') as f:
            all_lines = f.readlines()
            word = f'{card._word}-{card._translate}-{card._level}-{card._repeat}'
            f.seek(0)
            f.truncate()
            new_words = []
            flag = 0
            for line in all_lines:
                parts = line.split('-')
                word, translate, level, repeat = parts[0], parts[1], parts[2], parts[3].rstrip(), 
                if word == card._word:
                    flag = 1
                    continue
                else:
                    new_words.append(line)
            f.write("".join(new_words))
            if flag == 0:
                raise ValueError
            return new_words
    
    def choose_random_cards(self, file = database):
        """Sort cards by repeat time
        From this list choose the words we needed"""
        test_cards = []
        with open(file, 'r+') as f:
            all_words = f.readlines()
        repeat_words = []
        for line in all_words:
            parts = line.split('-')
            word, translate, level, repeat = parts[0], parts[1], parts[2], parts[3].rstrip(), 
            if int(repeat) != 1:
                continue
            else:
                repeat_words.append(line)
        test_words = []
        for i in range(0, self._number_cards):
            parts = repeat_words[i].split('-')
            word, translate, level, repeat = parts[0], parts[1], parts[2], parts[3].rstrip(), 
            card = Card(word, translate, level)
            test_words.append(card)
            self._cards.append(card)
        return test_words

        


