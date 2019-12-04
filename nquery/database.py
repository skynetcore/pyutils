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
# this contains class for nquery database tool
# please run the below steps in the system you are deploying
# - pip3 install mysql
# - pip3 install pymssql
# - pip3 install sqllite3
#
# and store the variable NQUERY_API_DATABASE in bash rc or environmental variable
# as 'mysql' or 'mssql' or 'sqlite'
# example:
#
# import nquery
#
# nq = NQuery() or // sqlite
#      NQuery('localhost', 3306, 'root','rootpwd') // mssql or mysql
# nq.connect('path\to\sqlite-file.db') or
#   .connect('database-name') // mssql or mysql
#
# nq.fetchby('one') or nq.fetchby('all') or nq.fetchby('many', 1280)
#
# nq.enquire('select * from table_name where some condition')
#
# data = nq.getdata()
# print(data)
#

# headers
import os

# database
try:
    if os.environ['NQUERY_API_DATABASE'] == 'mysql':
        import mysql.connector
        from mysql.connector import Error
        dbid = 'mysql'
        print('mysql connector loaded')
    elif os.environ['NQUERY_API_DATABASE'] == 'mssql':
        import pymssql
        from pymssql import Error
        dbid = 'mssql'
    elif os.environ['NQUERY_API_DATABASE'] == 'sqlite':
        import sqlite3
        from sqlite3 import Error
        dbid = 'sqlite'
except Exception as e:
    print('[nquery][init] - failed due to invalid environment variable configuration')

# constants
dbminlen = 3

# class sqlquery
class NQuery:
    # initialize data
    def __init__(self, dburl='localhost', dbport=3306, user='root', passwd='root'):
        self.__dburl = dburl
        self.__dbport = dbport
        self.__dbname = 'mybase'
        self.__dbuser = user
        self.__dbpass = passwd
        self.__fetchby = 'one'
        self.__fetchsize = 10
        self.__fetchfin = False


    # select a database
    def selectdb(self, dbname):
       self.__dbname = dbname


    # establish connection to database
    def connect(self, dbname='null'):
       if dbname != 'null' and len(dbname) > dbminlen:
           self.__dbname = dbname
       # enumerate connector
       if dbid == 'mysql':
           self.__connector = mysql.connector
       elif dbid == 'mssql':
           self.__connector = pymssql
       elif dbid == 'sqlite':
           self.__connector = sqllite3
       try:
           # now connect
           if dbid != 'sqllite':
               self.__dbase = self.__connector.connect(host=self.__dburl, database=self.__dbname, user=self.__dbuser, password=self.__dbpass, port=self.__dbport)
           else:
               self.__dbase = self.__connector.connect(self.__dbname)
           # take cursor
           if self.__dbase:
               self.__cursor = self.__dbase.cursor()
       except Error as e:
           print('[nquery][connect] - returned error as ', e)


    # close connection to database
    def close(self):
        try:
            if (self.__dbase.is_connected()):
                self.__cursor.close()
                self.__dbase.close()
        except Error as e:
            print('[nquery][close] - returned error as ', e)


    # quick validate a query TBD
    def __is_valid_sql(self, query):
        return True


    # define fetch size in query
    def fetchby(self, fetch='one', size=10):
        self.__fetchby = fetch
        self.__fetchsize = size
        print('[nquery][fetchby] set to {0} by size {1}'.format(fetch, size))


    # execute query
    def enquire(self, query):
        noerror = True
        self.__fetchfin = False
        try:
            # connect if connecton closed
            if self.__connector and not self.__dbase.is_connected():
                self.connect()
            # quick validate query
            if self.__is_valid_sql(query) and self.__cursor:
                print('[nquery][runsql] - executing sql query')
                self.__cursor.execute(query)
                # fetch if required
                if self.__fetchby == 'one':
                    self.__fetched = self.__cursor.fetchone()
                    self.__fetchfin = True
                elif self.__fetchby == 'many':
                    self.__fetched = self.__cursor.fetchmany(self.__fetchsize)
                    self.__fetchfin = True
                elif self.__fetchby == 'all':
                    self.__fetched = self.__cursor.fetchall()
                    self.__fetchfin = True
                # end
        except Error as e:
            print('[nquery][runsql] - query returned error ', e)
            noerror = False
        finally:
            # close even in failure
            self.close()
        return noerror

    # execute commit/insert and get row id
    def commit(self, query):
        row_id = 0
        self.__fetchfin = False
        try:
            # connect if connecton closed
            if self.__connector and not self.__dbase.is_connected():
                self.connect()
            # quick validate query
            if self.__is_valid_sql(query) and self.__cursor:
                print('[nquery][runsql] - executing sql commit')
                self.__cursor.execute(query)
                self.__dbase.commit()
                row_id = self.__cursor.lastrowid
        except Error as e:
            print('[nquery][runsql] - commit returned error ', e)
            row_id = -1
        finally:
            # close even in failure
            self.close()
        return row_id


    # fetch data
    def getdata(self):
        if self.__fetchfin and self.__fetched:
            return self.__fetched
        print('[nquery][getdata] - completed')

# end of class
