#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import mock

from sacreddeer import bot


class TestBot(unittest.TestCase):
    @mock.patch('slackclient.SlackClient.api_call')
    def _init_test_bot(self, mock_api_call):
        mock_api_call.return_value = {'ok': True,
                                      'members': [{'name': 'test_deer',
                                                   'id': '12345'}]}
        test_bot = bot.Bot('test_deer', 'token')
        self.assertTrue(mock_api_call.called)
        return test_bot

    def setUp(self):
        super(TestBot, self).setUp()
        self.bot = self._init_test_bot()

    @mock.patch('slackclient.SlackClient.api_call')
    def _handle_command(self, cmd, responses, mock_api_call):
        self.bot.handle_command(cmd, 'channel')
        self.assertTrue(mock_api_call.called)
        call_args = mock_api_call.call_args[0]
        call_kwargs = mock_api_call.call_args[1]
        self.assertEqual('chat.postMessage', call_args[0])
        self.assertTrue(call_kwargs['as_user'])
        self.assertEqual('channel', call_kwargs['channel'])
        self.assertIn(call_kwargs['text'], responses)

    def test_handle_command_ua(self):
        cmd = u'ua Мене звільнять?'
        responses_ua = [
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
        ]
        self._handle_command(cmd, responses_ua)
