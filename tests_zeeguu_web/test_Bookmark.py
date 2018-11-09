from zeeguu_web.api_communication.models.Bookmark import Bookmark


class TestBookmark:

    def test_from_json(self):
        json_dict = {
            'id': 47891,
            'to': 'alleged',
            'from_lang': 'es',
            'to_lang': 'en',
            'title' : '',
            'url': 'http://www.eluniversal.com.mx/mundo/homenajean-en-los-angeles-actriz-porno-que-enfrenta-trump',
            'origin_importance': 0,
            'starred': False,
            'origin_rank':1000,
            'learned_datetime':'2017-10-10T10:10:10',
            'created_day': '2017-10-10T10:10:10',
            'time': '2017-10-10T10:10:35.750065Z',
            'from': 'supuesta',
            'context': 'Hurpy durpy durp',
            'article_id': '47891'
        }
        bm = Bookmark.from_json(json_dict)
        assert bm.id == 47891
        assert bm.to == 'alleged'
        assert bm.from_lang == 'es'
        assert bm.to_lang == 'en'
        assert bm.url.title == ''
        assert bm.url.url == 'http://www.eluniversal.com.mx/mundo/homenajean-en-los-angeles-actriz-porno-que-enfrenta-trump'
        assert bm.origin_importance == ''
        assert bm.starred == False
        assert bm.from_ == 'supuesta'
        assert bm.context == 'Hurpy durpy durp'

    def test_first_N_words_of_context_shorter(self):
        text = '1 2 3 4 5 6 7'
        context = Bookmark.get_first_N_words_of_context(text)
        assert context == text

    def test_first_N_words_of_context_longer(self):
        text = '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45.'
        shortened_text = '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42'
        context = Bookmark.get_first_N_words_of_context(text)
        assert context == shortened_text

    def test_importance_float(self):
        text = Bookmark.string_representation_of_importance(2.31)
        assert text == "<span style='font-size:8pt'>|</span><span style='font-size:7pt'>|</span>"

    def test_importance_below_1(self):
        text = Bookmark.string_representation_of_importance(0.1)
        assert text == ''
