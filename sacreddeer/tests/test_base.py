#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import mock

from sacreddeer import base


class TestBotBase(unittest.TestCase):
    bot_class = base.Bot

    @mock.patch('slackclient.SlackClient.api_call')
    def _init_test_bot(self, bot_class, mock_api_call):
        mock_api_call.return_value = {'ok': True,
                                      'members': [{'name': 'test_bot',
                                                   'id': '12345'}]}
        test_bot = bot_class('test_bot', 'token')
        self.assertTrue(mock_api_call.called)
        return test_bot

    def setUp(self):
        super(TestBotBase, self).setUp()
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

    def test_handle_command(self):
        self.handle_command('command', ['Hello!'])
