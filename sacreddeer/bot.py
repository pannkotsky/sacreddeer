import logging
import os
import random
import time

import slackclient

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO)


class Bot(object):
    def __init__(self, name, token):
        self.name = name
        self.client = slackclient.SlackClient(token)
        self.bot_id = self._get_bot_id()

    def _get_bot_id(self):
        api_call = self.client.api_call("users.list")
        if api_call.get('ok'):
            # retrieve all users so we can find our bot
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == self.name:
                    return user.get('id')
        else:
            raise LookupError("Could not find bot user with the name " +
                              self.name)

    def handle_command(self, cmd, chan):
        """
            Receives commands directed at the bot and determines if they
            are valid commands. If so, then acts on the commands. If not,
            returns back what it needs for clarification.
        """
        responses = {
            'en': [
                "Yes",
                "No",
                "It doesn't matter",
                "Chill, bro",
                "Ha-ha, very funny",
                "Yes, but shouldn't",
                "Never",
                "100%",
                "1 of 100",
                "Try again"
            ],
            'ru': [
                "Да",
                "Нет",
                "Это не важно",
                "Спок, бро",
                "Толсто",
                "Да, хотя зря",
                "Никогда",
                "100%",
                "1 из 100",
                "Еще разок"
            ],
            'ua': [
                "Так",
                "Ні",
                "Немає значення",
                "Не сци, козаче",
                "Товсто",
                "Так, хоча даремно",
                "Ніколи",
                "100%",
                "1 із 100",
                "Спробуй ще"
            ],
            'de': [
                "Ja",
                "Nein",
                "Das ist nicht jebachtung",
                "Uspokojten, Bruder",
                "Tolstische",
                "Ja, aber Dolbojobist",
                "Nie",
                "100%",
                "1 von 100",
                "Poprobiren es noch einmal"
            ]
        }
        lang = cmd[:2] if len(cmd) >= 2 else 'ru'
        responses_list = responses.get(lang) or responses['ru']
        response = random.choice(responses_list)
        self.client.api_call("chat.postMessage", channel=chan,
                             text=response, as_user=True)
        logging.info('Command: "%s", response: "%s"', cmd, response)

    def parse_slack_output(self, slack_rtm_output):
        """
            The Slack Real Time Messaging API is an events firehose.
            this parsing function returns None unless a message is
            directed at the Bot, based on its ID.
        """
        at_bot = "<@" + self.bot_id + ">"

        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and 'text' in output and at_bot in output['text']:
                    # return text after the @ mention, whitespace removed
                    return output['text'].split(at_bot)[1].strip().lower(), \
                           output['channel']
        return None, None

    def run(self, read_socket_delay=1):
        if self.client.rtm_connect():
            logging.info("Sacred Deer connected and running!")
            while True:
                command, channel = self.parse_slack_output(
                    self.client.rtm_read())
                if command and channel:
                    self.handle_command(command, channel)
                time.sleep(read_socket_delay)
        else:
            logging.error("Connection failed. Invalid Slack token or bot ID?")


if __name__ == "__main__":
    bot = Bot('sacred_deer', os.environ.get('TOKEN'))
    bot.run()
