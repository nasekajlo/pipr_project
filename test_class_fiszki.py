from class_fiszki import *
import pytest
database = 'word_for_repeat_test.txt'
database1 = 'words_import.txt'
database2 = 'words_delete.txt'
database3 = 'word_for_repeat_test.txt'

def test_init_card():
    card = Card("cześć", "hello", 1)
    assert card.word == "cześć"
    assert card.translate == "hello"
    assert card.level == 1
    assert card.repeat == 8

def test_error_card():
    with pytest.raises(ValueError):
        card = Card("", "hello", 1)
        assert card.word == "cześć"

def test_round_init():
    number_of_cards = 10
    time = 60
    round = Round(number_of_cards, time)
    assert round.number_of_cards == 10
    assert round.time == 60

def test_export_card():
    card = Card("broskwina", "peach", 3)
    round = Round(5, 60)
    round.export_card(card, "new_test.txt")
    with open("new_test.txt", 'r') as f:
        f.readline()
        f.readline()
        f.readline()
        str = f.readline()
    assert str == f'broskwina-peach-3-8\n'

def test_export_exist_card():
    with pytest.raises(ValueError):
        card = Card("broskwina", "peach", 3)
        round = Round(5, 60)
        round.export_card(card, "new_test.txt")
        with open("new_test.txt", 'r') as f:
            f.readline()
            f.readline()
            f.readline()
            str = f.readline()

def test_import_card():
    card1 = Card("jablko", "apple", 2)
    card2 = Card("siema", "bye", 1)
    cards = [card1, card2]
    round = Round(5, 60)
    new_cards = round.import_card(cards, database1)
    expected_card = Card('truskawka', 'strawberry', 3)
    assert new_cards[2].word == 'truskawka'

def test_define_new_card():
    card1 = Card("jablko", "apple", 2)
    card2 = Card("siema", "bye", 1)
    cards = [card1, card2]
    round = Round(5, 60)
    card3 = Card("malpa", "monkey", 3)
    new_cards = round.define_new_card("malpa", "monkey", 3, cards)
    assert new_cards[2] == card3

def test_define_exist_card():
    with pytest.raises(ValueError):
        card1 = Card("jablko", "apple", 2)
        card2 = Card("siema", "bye", 1)
        card3 = Card("malpa", "monkey", 3)
        cards = [card1, card2, card3]
        round = Round(5, 60)
        round.define_new_card("malpa", "monkey", 3, cards)

def test_define_card_empty_word():
    with pytest.raises(ValueError):
        card1 = Card("jablko", "apple", 2)
        card2 = Card("siema", "bye", 1)
        card3 = Card("malpa", "monkey", 3)
        cards = [card1, card2, card3]
        round = Round(5, 60)
        round.define_new_card("", "monkey", 3, cards)

def test_define_card_empty_trans():
    with pytest.raises(ValueError):
        card1 = Card("jablko", "apple", 2)
        card2 = Card("siema", "bye", 1)
        card3 = Card("malpa", "monkey", 3)
        cards = [card1, card2, card3]
        round = Round(5, 60)
        round.define_new_card("malpa", "", 3, cards)

def test_delete_card():
    card2 = Card("siema", "bye", 1)
    round = Round(5, 60)
    new_words = round.delete_card(card2, database2)
    assert len(new_words) == 11

def test_delete_not_existing_card():
    with pytest.raises(ValueError):
        card = Card("dom", "house", 1)
        round = Round(5, 60)
        new_words = round.delete_card(card, database2)
        assert len(new_words) == 11

def test_random_cards():
    round = Round(6, 60)
    random_words = round.choose_random_cards(database3)
    assert random_words[0].word == 'truskawka'
    assert random_words[4].word == 'szczotka'
    assert random_words[5].word == "szkola"

def test_check_result_true():
    card1 = Card("jablko", "apple", 2)
    card2 = Card("siema", "bye", 1)
    card3 = Card("malpa", "monkey", 3)
    card4 = Card("szczotka", "hairbrush", 2)
    tr_card1 = "apple"
    tr_card2 = "bye"
    tr_card3 = "monkey"
    tr_card4 = "hairbrush"
    sorted_cards = [card1, card2, card3, card4]
    sorted_translate = [tr_card1, tr_card2, tr_card3, tr_card4]
    round = Round(4, 60)
    bad_words = round.check_result(sorted_cards, sorted_translate, 50)
    assert bad_words == []

def test_check_result_false():
    card1 = Card("jablko", "apple", 2)
    card2 = Card("siema", "bye", 1)
    card3 = Card("malpa", "monkey", 3)
    card4 = Card("szczotka", "hairbrush", 2)
    tr_card1 = "apple"
    tr_card2 = "bye"
    tr_card3 = "monkey"
    tr_card4 = "hairbrush"
    sorted_cards = [card1, card2, card3, card4]
    sorted_translate = [tr_card2, tr_card1, tr_card3, tr_card4]
    round = Round(4, 60)
    bad_words = round.check_result(sorted_cards, sorted_translate, 50)
    assert bad_words == [card1, card2]

def test_check_result_more_time():
    card1 = Card("jablko", "apple", 2)
    card2 = Card("siema", "bye", 1)
    card3 = Card("malpa", "monkey", 3)
    card4 = Card("szczotka", "hairbrush", 2)
    tr_card1 = "apple"
    tr_card2 = "bye"
    tr_card3 = "monkey"
    tr_card4 = "hairbrush"
    sorted_cards = [card1, card2, card3, card4]
    sorted_translate = [tr_card1, tr_card2, tr_card3, tr_card4]
    round = Round(4, 60)
    bad_words = round.check_result(sorted_cards, sorted_translate, 70)
    assert bad_words == [card1, card2, card3, card4]

def test_words_for_repeat():
    card1 = Card("jablko", "apple", 2, 8)
    card2 = Card("siema", "bye", 1, 4)
    card3 = Card("malpa", "monkey", 2, 4)
    card4 = Card("szczotka", "hairbrush", 2, 1)
    cards = [card1, card2, card3, card4]
    round = Round(4, 60)
    update_words = round.words_for_repeat(cards, database3)
    assert update_words[0].repeat == 32
    assert update_words[1].repeat == 16
    assert update_words[2].repeat == 1
    assert update_words[8].repeat == 4
    assert update_words[11].repeat == 16