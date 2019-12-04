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
# this contains class for smtp mail notification modules
# please run the below step in the system you are deploying
# - pip3 install smtplib
#
# and store smtp credentials
# as MAIL_API_ADDRESS in bash rc or environemental variable
# also store your password for which address is registered
# as MAIL_API_PASSWD
#
# example:
#
# import mailtools
#
# mbot = MailBot('smtp-mail-server-address', port-number)
# mbot.notify('receiver@address.com','your message goes here')
#


# headers
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# const variables
minsubjlen = 5
minformatlen = 10


# class definition
class MailBot:
    # constructor
    def __init__(self, smtp_server_address, smtp_server_port):
        self.__useraddr = os.environ['MAIL_API_ADDRESS']
        self.__userpass = os.environ['MAIL_API_PASSWD']
        self.__smtpaddr = smtp_server_address
        self.__smtpport = smtp_server_port
        self.__subject = ""
        self.__html_content = bool(0)
        self.__html_format = ""


    # set html support
    def enable_html_content(self, enable):
        self.__html_content = bool(enable)


    # set subject
    def set_subject(self, subject):
        if len(subject) > minsubjlen:
            self.__subject = subject


    # get subject
    def __get_subject(self):
        if len(self.__subject) < minsubjlen:
            self.__subject = 'IMP Auto Mail Bot Notification'
        return self.__subject

    # set custom body in html
    # please have data place holders like {0} placed for message
    # or edit the way you need for a beautiful mail
    def set_html_format(self, html_string):
        self.__html_format = html_string

    # get html format
    def __format_to_html(self, message):
        html_string = ''
        if len(self.__html_format) < minformatlen:
            # default format, you can change this aswell and have image links
            html_string = '<html><head>IMP</head><body>{0}</body></html>'
        else:
            html_string = self.__html_format
        return html_string.format(message)

    # notify is used to send mail notification
    # message can also be in html format
    def notify(self, to_address, from_address, message):
        message = MIMEMultipart()
        if bool(self.__html_content):
            message = MIMEMultipart('alternative')
        message['From'] = self.__useraddr
        message['To'] = to_address
        message['Subject'] = self.__get_subject()
        text_raw = message
        text_html = self.__format_to_html(text_raw)
        plain_part = MIMEText(text_raw, 'plain')
        # attach
        message.attach(plain_part)
        if bool(self.__html_content):
            html_part = MIMEText(text_html, 'html')
            message.attach(html_part)
        # create session
        session = smtplib.SMTP(self.__smtpaddr, self.__smtpport)
        session.starttls()
        session.login(self.__useraddr, self.__userpass)
        session.sendmail(self.__useraddr, to_address, message.as_string())
        session.quit()

# end of class