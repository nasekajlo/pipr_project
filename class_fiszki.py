from random import randint
database = 'cards.txt'
words_for_repeat = 'words_for_repeat.txt'

class Card:
    def __init__(self, word: str, translate: str, level: int):
        """Конструктор принимает само слово, его перевод и уровень сложности"""
        if word == '':
            raise ValueError
        if translate == '':
            raise ValueError
        self._word = word
        self._translate = translate
        self._level = level
    
    def __str__(self):
        return self._word

#функция для записи ошибочных слов в отдельных файл для повторения
class Round:
    def __init__(self, cards, time):
        """ NOT FINISHED!
            Конструктор раунда принимает список фишек и время выполнения теста"""
        self._time = time
        self._cards = cards
    
    def check_result(self, sorted_cards, sorted_translate, time, test_time):
        """Два критерия по оценке теста:
            1. Время выполнения меньше времени, отведенного на тест
            2. Слова сопоставлены правильно
           Если время выполнения меньше, все слова не будут засчитаны
           Если время соблюдено, то засчитываются правильные сопоставление
           В итоге возвращается список неправильных слов"""
        bad_words = []
        #good_words = []
        if time > test_time:
            bad_words = sorted_cards
            return 
        for pair_card in zip(sorted_cards, sorted_translate):
            if pair_card[0]._translate != pair_card[1]._word:
                bad_words.append(pair_card[0])
           # else:
                #good_words.append(pair_card[0])
        return bad_words

    def bad_words_for_repeat(self, bad_words, file = words_for_repeat):
        """Записываем неправильные слова в файл для особого повторения"""
        with open(file, 'w') as f:
            for card in bad_words:
                f.write(f'{card._word}-{card._translate}-{card._level}\n')

    def add_new_card(self, word, translate):
        """DELETE AT THE END"""
        card = Card(word, translate)
        self.append(card)

    def export_card(self, card: Card, file=database):
        """Експорт принимает фишку, которую нужно экспортировать
            и файл, в который нужно ее сохранить(файл определен как константа"""
        with open(file, 'w') as f:
            f.write(f'{card._word}-{card._translate}-{card._level}/n')

    def import_card(self, cards, file=database):
        """Импорт принимает список разыгрываемых карточек и файл, их которого импортируется фишка.
            1. Считываются все строки файла
            2. Выбирается рандомное слово (слово+перевод+уровень)
            3. Если такого слова нет в данном тесте, оно импортируется
            4. Если попали в слово, которое уже есть в тесте, выбираем еще иаз рандомное слово
            5. И так до тех пор пока не найдем неповторяющиеся слово"""
        with open(file, 'w') as f:
            line_count = sum(1 for line in f)
            random_line = randint(1, line_count)
            pair = f.readline(random_line)
            word_trans_level = pair.split('-')
            card = Card(word_trans_level[0], word_trans_level[1], word_trans_level[2])
            while card in cards:
                random_line = randint(1, line_count)
                pair = f.readline(random_line)
                word_trans_level = pair.split('-')
                card = Card(word_trans_level[0], word_trans_level[1], word_trans_level[2])
            cards.append(card)

    def define_new_card(self, word, translate, level: int, file = database):
        """Добавление новой карточки вручную.
           На вход принимается слово, перевод, уровень сложности и файл для записи
            1. Считываются все уже существующиеся из файла
            2. Проверка: если такое слово уже есть, выходим из функции
            3. Если нет, добавляем новое слово
           Тут исключено добавление одного и того же слова с разным уровнем сложности."""
        all_words = []
        with open(file, 'w') as f:
            all_words = f.readlines()
            word_translate_level = f'{word}-{translate}-{level}'
            for word in all_words:
                iterate_word, iterate_translate, iterate_level = word.split('-')
                if (iterate_word == word):
                    return
            f.write(word_translate_level)

    def delete_card(self, card: Card, file = database): 
        """На вход принимаются сама фишка и файл, из которого будет удалять слово
            1. Считываем все строки
            2. Очищаем весь файл
            3. Перезаписываем все строки
            4. Если встретили ту которую нужно удалить, просто пропускаем"""
        all_words = []
        with open(file, 'r+') as f:
            all_words = f.readlines()
            word_translate_level = f'{card._word}-{card._translate}-{card._level}'
            f.seek(0)
            f.truncate()
            for word in all_words:
                if word.strip("\n") != word_translate_level:
                    f.write(word+"\n")
    
    def choose_random_cards(self, number_of_cards: int, file = database):
        test_cards = []
        with open(file, 'r+') as f:
            all_words = f.readlines()
        for i in range(number_of_cards):

    def play_round(self, file = database):
        """В процессе разработки (сначала дописать генерацию карточек и их запись"""
        all_words = []
        with open(file, 'r+') as f:
            all_words = f.readlines()
        with open('round.txt', 'w') as f:
            for i in range(0, number_of_cards-1):
                random_line = randint(0, len(all_words)-1)
                f.write(all_words[random_line])
                all_words.pop()


