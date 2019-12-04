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
# example:
#
# import ipman
# # --- GET request
# postman = IPMan('googleapis.com/api/location', False)
# postman.add_header('somekey':'value')
# postman.add_param('somekey': 'somedata')
# data = postman.get()
# print(data)
#
# # ---  POST request
# postman = IPMan('googleapis.com/api/location', True)
# postman.add_header('somekey':'value')
# postman.add_data('somekey': 'somedata')
# postman.add_file('file_name': 'file_path\path')
# data = postman.post()
# print(data)
#


# headers
import json
import requests


# class ipman
class IPMan:
    def __init__(self, url, post=True):
        self.post = post
        self.__headers = {}
        # conditional data
        if not post:
            self.__params = {}
        else:
            self.__data = {}
            self.__files = {}
        # url is mandatory
        self.__url = url


    # add HTTP header
    def add_header(self, header_name, header_val):
        key = header_name
        value = header_val
        # check and enter
        if len(key) > 0 and isinstance(key, str) and len(value) > 0 and isinstance(value, str):
            self.__headers[key] = value
        else:
            print('[ipman] - could not add header due to invalid data')


    # add data for POST requests
    def add_data(self, data_name, data_value):
        key = data_name
        value = data_value
        if len(key) > 0 and isinstance(key, str) and len(value) > 0 and isinstance(value, str):
            self.__data[key] = value
        else:
            print('[ipman] - could not add payload due to invalid data')


    # add params for http GET requests
    def add_param(self, param_name, param_value):
        key = param_name
        value = param_value
        if len(key) > 0 and isinstance(key, str) and len(value) > 0 and isinstance(value, str):
            self.__params[key] = value
        else:
            print('[ipman] - could not add param due to invalid data')


    # add files for upload using POST
    def add_file(self, file_name, file_path):
        key = file_name
        value = open(file_path, 'rb')
        if len(key) > 0 and isinstance(key, str) and len(value) > 0 and isinstance(value, str):
            self.__files[key] = value
        else:
            print('[ipman] - could not add file due to an error caused with file')


    # send a POST request
    def postdata(self):
        print('[ipman] - sending request to {0}'.format(self.__url))
        resp = requests.post(self.__url, headers=self.__headers, files=self.__files, data=self.__data)
        self.__resp = resp
        return self.__resp


    # send a GET request
    def getdata(self):
        print('[ipman] - sending request to {0}'.format(self.__url))
        resp = requests.get(self.__url, headers=self.__headers, params=self.__params)
        self.__resp = resp
        return self.__resp

# end of class
