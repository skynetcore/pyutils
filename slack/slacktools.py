#!/usr/bin/python
#
# Copyright 2019 skynetcore
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# this contains class for slack notification modules
# please run the below step in the system you are deploying
# - pip3 install slackclient
#
# and request a personal token from admin, then store the value
# as SLACK_API_TOKEN in bash rc or environemental variable
# also store your user name for which token was issued as
# SLACK_API_USER
#
# example:
#
# import slacktools
#
# bot = SlackBot("#your-channel")
# bot.notify("your scheduled task is completed")
#


# headers
import os
import slack


# public const texts
botmsg_id  = 'chat.postMessage'
botmoji  = ':robot_face:'


# class definition
class SlackBot:
    def __init__(self, channel):
        # make sure you have the below added in environment variable
        self.__token = os.environ['SLACK_API_TOKEN']
        self.__username = os.environ['SLACK_API_USER']
        # accept channel name even if # is missing
        if channel[0] == '#':
            self.__channel = channel
        else:
            self.__channel = '#' + channel;
        # initialize slack client
        self.__slackbot = SlackClient(self.token)
        self.__intro_msg = ""


    # debug parameters
    def debug(self):
        # list all data and perform checks
        print('slack token    : ' + self.__token)
        print('slack username : ' + self.__username)
        print('slack channel  : ' + self.__channel)
        print('slack bot obj  : ' + self.__slackbot)


    # get intro message
    def __getintro_msg(self):
        if len(self.__intro_msg) < 2:
            self.__intro_msg = 'Hi Team, this is your IMP slack bot chatting :tada:'
        return self.__intro_msg


    # set intro message
    def setintro_msg(self, message):
        self.__intro_msg = str(message)


    # auto message
    def __introduce(self):
        self.__slackbot.api_Call(botmsg_id, channel=self.__channel, text=self.__intro_msg, username=self.__username, icon_emoji=botmoji)


    # learn api
    def __learn(self, data):
       print('learning api integration TBD')


    # notify the channel
    def notify(self, message):
        print('[imp][automata] - notifying slack channel {0} '.format(self.__channel))
        self.__learn(message)
        self.__introduce()
        self.__slackbot.api_call(botmsg_id, channel=self.__channel, text=message, username=self.__username, icon_emoji=botmoji)

# end of class
