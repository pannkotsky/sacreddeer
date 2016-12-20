#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import mock

from sacreddeer import sacred_deer_bot


class TestBot(unittest.TestCase):
    bot_class = sacred_deer_bot.SacredDeer

    @mock.patch('slackclient.SlackClient.api_call')
    def _init_test_bot(self, bot_class, mock_api_call):
        mock_api_call.return_value = {'ok': True,
                                      'members': [{'name': 'test_bot',
                                                   'id': '12345'}]}
        test_bot = bot_class('test_bot', 'token')
        self.assertTrue(mock_api_call.called)
        return test_bot

    def setUp(self):
        super(TestBot, self).setUp()
        self.bot = self._init_test_bot(self.bot_class)

    @mock.patch('slackclient.SlackClient.api_call')
    def handle_command(self, cmd, responses, mock_api_call):
        self.bot.handle_command(cmd, 'channel')
        self.assertTrue(mock_api_call.called)
        call_args = mock_api_call.call_args[0]
        call_kwargs = mock_api_call.call_args[1]
        self.assertEqual('chat.postMessage', call_args[0])
        self.assertTrue(call_kwargs['as_user'])
        self.assertEqual('channel', call_kwargs['channel'])
        self.assertIn(call_kwargs['text'], responses)

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

    def test_handle_command_ru(self):
        self._check_response('ru')

    def test_handle_command_ua(self):
        self._check_response('ua')

    def test_handle_command_en(self):
        self._check_response('en')

    def test_handle_command_de(self):
        self._check_response('de')
