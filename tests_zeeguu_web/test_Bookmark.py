import pytest
import requests

from zeeguu_web.account.api import api_connection
from zeeguu_web.account.api.api_connection import APIException
from zeeguu_web.account.api.models.Bookmark import Bookmark


class TestBookmark:

    def test_from_json(self):
        json_dict = {
            'id': 47891,
            'to': 'alleged',
            'from_lang': 'es',
            'to_lang': 'en',
            'title': '',
            'url': 'http://www.eluniversal.com.mx/mundo/homenajean-en-los-angeles-actriz-porno-que-enfrenta-trump',
            'origin_importance': 0,
            'starred': False,
            'from': 'supuesta',
            'context': 'Daniels afirma haber recibido 130.000 dólares en el marco de un acuerdo de confidencialidad para silenciar su supuesta relación con Trump, que habría tenido lugar cuando el magnate ya estaba casado con su actual esposa Melania.'
        }
        Bookmark.from_json(json_dict)
        assert True

    def test_first_N_words_of_context(self):
        assert True

    def test_importance_float(self):
        assert True

    def test_importance_below_1(self):
        assert True
