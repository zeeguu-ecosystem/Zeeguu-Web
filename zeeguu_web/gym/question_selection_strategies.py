import flask
from zeeguu.model.text import Text
from zeeguu.model.user_word import UserWord
from zeeguu.model.bookmark import Bookmark
from zeeguu.model.language import Language
from user_message import UserVisibleException
import random
from datetime import timedelta, date

def new_random_question():
    bookmarks = (
            Bookmark
            .query.filter_by(user=flask.g.user)
            .join(UserWord, Bookmark.origin)
            .join(Language, UserWord.language)
            .join(Text, Bookmark.text)
            .filter(UserWord.language == flask.g.user.learned_language)
            .filter(Text.content != "")
    ).all()

    if len(bookmarks) == 0:
        raise UserVisibleException("It seems you have nothing to learn...")

    bookmark = random.choice(bookmarks)

    text_to_display = bookmark.text.content

    for each in bookmark.text.all_bookmarks():
        if not bookmark.translations_rendered_as_text() == each.translations_rendered_as_text():
            text_to_display = text_to_display.replace (each.origin.word, each.origin.word + " ("+each.translations_rendered_as_text()+")")


    return {
        "question": bookmark.translations_rendered_as_text(),
        "example":text_to_display,
        "url":bookmark.text.url.url,
        "answer": bookmark.origin.word,
        "bookmark_id": bookmark.id,
        "id": bookmark.id,
        "rank": bookmark.origin.importance_level(),
        "reason": "Random Word",
        "starred": False
    }



def select_next_card_aware_of_days(cards):

    interesting_intervals = [1,2,7,31]
    interesting_dates = [date.today() - timedelta(days=x) for x in interesting_intervals]


    interesting_cards = [card for card in cards if card.last_seen.date() in interesting_dates]
    interesting_cards.sort(key=lambda card: card.bookmark.origin.importance_level())

    if interesting_cards:
        card = interesting_cards[0]
        card.set_reason("seen on: " + card.last_seen.strftime("%d/%m/%y"))
        return card

    cards_not_seen_today = [card for card in cards if card.last_seen.date() != date.today()]
    cards_not_seen_today.sort(key=lambda card: card.bookmark.origin.importance_level())

    if cards_not_seen_today:
        card = cards_not_seen_today[0]
        card.set_reason("seen on: " + card.last_seen.strftime("%d/%m/%y"))
        return card

    # All cards were seen today. Just return a random one
    if cards:
        card = random.choice(cards)
        card.set_reason("random word: all others are seen today.")
        return card

    return None


