import os
import random
import time

import slackclient

BOT_NAME = 'sacred_deer'
BOT_ID = None # 'U2M6BHP4Y'
TOKEN = os.environ.get('TOKEN')


slack_client = slackclient.SlackClient(TOKEN)

def get_bot_id():
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                return user.get('id')
    else:
        raise LookupError("Could not find bot user with the name " + BOT_NAME)


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    responses = [
        "Yes",
        "Niet",
        "It doesn't matter",
        "Chill, bro",
        "Tolsto",
        "Yes, but zrya",
        "Nein! Nein! Nein!!!",
        "100%",
        "1 of 100",
        "Try again"
    ]
    response = random.choice(responses)
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)
    print(time.strftime('%d-%m-%Y %H:%M.%S')+ ' ' + command + ' --- ' + response)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    global BOT_ID
    if not BOT_ID:
        BOT_ID = get_bot_id()
    at_bot = "<@" + BOT_ID + ">"
    
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and at_bot in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(at_bot)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print("Sacred Deer connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
