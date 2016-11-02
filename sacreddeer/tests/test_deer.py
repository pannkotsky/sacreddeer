#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sacreddeer import sacred_deer_bot
from sacreddeer.tests import test_base


class TestBot(test_base.TestBotBase):
    bot_class = sacred_deer_bot.SacredDeer

    def _check_response(self, lang):
        responses = {
            'en': [
                u"Yes",
                u"No",
                u"It doesn't matter",
                u"Chill, bro",
                u"Ha-ha, very funny",
                u"Yes, but shouldn't",
                u"Never",
                u"100%",
                u"1 of 100",
                u"Try again"
            ],
            'ru': [
                u"Да",
                u"Нет",
                u"Это не важно",
                u"Спок, бро",
                u"Толсто",
                u"Да, хотя зря",
                u"Никогда",
                u"100%",
                u"1 из 100",
                u"Еще разок"
            ],
            'ua': [
                u"Так",
                u"Ні",
                u"Немає значення",
                u"Не сци, козаче",
                u"Товсто",
                u"Так, хоча даремно",
                u"Ніколи",
                u"100%",
                u"1 із 100",
                u"Спробуй ще"
            ],
            'de': [
                u"Ja",
                u"Nein",
                u"Das ist nicht jebachtung",
                u"Uspokojten, Bruder",
                u"Tolstische",
                u"Ja, aber Dolbojobist",
                u"Nie",
                u"100%",
                u"1 von 100",
                u"Poprobiren es noch einmal"
            ]
        }
        responses_list = responses.get(lang)
        cmd = u'{} test command'.format(lang)
        self.handle_command(cmd, responses_list)

    def test_handle_command(self):
        pass

    def test_handle_command_ru(self):
        self._check_response('ru')

    def test_handle_command_ua(self):
        self._check_response('ua')

    def test_handle_command_en(self):
        self._check_response('en')

    def test_handle_command_de(self):
        self._check_response('de')
