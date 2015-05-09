# This code is written by Cem Iskir for Open Source SW Eng Course

import json
import sqlite3
import re

#
# Functions for sanitizing given string in order to prevent SQL Injection
# It basically removes everything other than alphanumerical characters and returns the result
#
def sanitizeMe(givenstr):
    return sanitize(givenstr, '[^a-zA-Z0-9]')


def sanitizeNumber(givenstr):
    return sanitize(givenstr, '[^a-zA-Z0-9.]')


def sanitize(givenstr, regex):
    regex = re.compile(regex)
    return regex.sub('', givenstr)

#
# Checks if a given table is in database
# It doesn't check if that table belongs to some other user.
# To guarantee ownership we should pass the parameter as USERNAME_TABLENAME
#
def checkIfExistedInRealTime(givenstr, shouldBeSanitized):
    #if given argument is a string
    if isinstance(givenstr, str):
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        if shouldBeSanitized == True:
            c.execute("pragma table_info("+sanitizeMe(str(givenstr))+")")
        else:
            c.execute("pragma table_info("+givenstr+")")

        primaryKeyName = ''
        primaryKeyType = ''
        counter = 0

        # returns an empty list if nothing is existed, returns primary key and type of primary key if primary key exists
        # result for pragma is cid-name-type-notnull-dflt_value_pk
        # format of received message will be 0 username TEXT 1 None 0
        # where the last value is a binary field standing for if that field is the primary key
        # Assumed that a table must have a primary key, if it doesn't this function can return a random field as a primary key
        for row in c:
            for elem in row:
                #if field name
                if (counter % 6) == 1:
                    primaryKeyName = str(elem)
                if (counter % 6) == 2:
                    primaryKeyType = str(elem)
                elif (counter % 6) == 5:
                    if(elem == 1):
                        conn.close()
                        return [primaryKeyName, primaryKeyType]
                counter += 1

        conn.close()
        return []

#
# Returns the names of the table, given delimiter is used as a separator
#
def getAllTableNames(username, delimiter):

    #if given argument is a string
    if isinstance(username, str):
        conn = sqlite3.connect('example.db')
        c = conn.cursor()

        statem = 'select TableName from tables_' + username + ';'
        c.execute(statem)

        result = ''

        for row in c:
            for elem in row:
                # if the table isn't an intermediate table
                if not elem.startswith('inter_'):
                    result += elem
            result += delimiter

        conn.close()
        if result != '':
            return result[:-1]
        else:
            return ''

#
# tablename isn't protected from SQL injection
# it takes username, tablename and json file object as the parameter
# returns a list which has 2 elements. First element is the name of the primary key field
# while the second one is the type of the field
# returns list if empty string if table cannot be found
#
def returnPrimary(username,tableName,data):

    if not data is None:
        #Checking JSON file
        for table in data['table']:
            if sanitizeMe(table['name']) == tableName:
                for eachField in table['fields']:
                    if eachField['primary'] == True:
                        return [sanitizeMe(eachField['name']), sanitizeMe(eachField['type'])]

                #Table doesn't have user specified primary key column, retur the default 'ID'
                return ['ID', 'INTEGER']

    #Checking existed tables from database
    result = checkIfExistedInRealTime(username + '_' + tableName,False)
    #returns empty string if table cannot be found
    return result

#Main Program
#This program takes a
def processJSON(username, dbname, jsonfilename):

    # These variables are used for inserting the information of newly created table to tables_USERNAME table.
    allTableNames = []
    allTablePrimaries= []

    #MALICIOUS PARAMETERS
    if not (isinstance(username, str) and isinstance(dbname, str) and isinstance(jsonfilename, str)):
        return

    intermediateCreateStatement = ''
    addNewlyCreatedTablesStatement = ''

    with open(jsonfilename) as data_file:
        data = json.load(data_file)

    #If JSON file cannot be opened return
    if data is None:
        return

    conn = sqlite3.connect(dbname)

    c = conn.cursor()

    table = None

    dataTypes = ('TEXT', 'REAL', 'INTEGER')

    try:
        statement = ''
        for table in data['table']:
            if str(data['operation']) == 'create':
                statement += 'CREATE TABLE IF NOT EXISTS ' + username + '_' + sanitizeMe(str(table['name'])) + ' ('

                allTableNames.append(username + '_' + sanitizeMe(str(table['name'])))

                #iterating through each field

                hasprimaryKey = False
                #hold the primary key for the current table while iteration through tables in JSON files
                currentPrimary = ''
                # in case there is no given primary key, the generated primary key column will be INTEGER
                currentPrimaryType = 'INTEGER'

                #creating SQL statement for table creation
                for name in table['fields']:
                    statement += '_' + sanitizeMe(str(name['name'])) + ' '

                    datatype = sanitizeMe(str(name['type']).upper())
                    if datatype in dataTypes:
                        statement += datatype + ' '
                    elif datatype == 'BOOLEAN':
                        statement += 'INTEGER '

                    if name['primary'] == True:
                        statement += 'PRIMARY KEY '
                        hasprimaryKey = True
                        currentPrimary = '_' + sanitizeMe(str(name['name']));
                        currentPrimaryType = sanitizeMe(str(name['type']).upper())
                        allTablePrimaries.append(currentPrimary)
                    else:
                        if name['null'] == False:
                            statement += 'NOT NULL '
                            if name['unique'] == True:
                                statement += 'UNIQUE '
                        else:
                            statement += 'NULL '

                        #look at default
                        if name['default'] is not None:
                            statement += 'DEFAULT '
                            if datatype == 'BOOLEAN':
                                if name['default'] == True:
                                    statement += '1'
                                else:
                                    statement += '1'
                            elif datatype == 'INTEGER' or datatype == 'REAL':
                                statement += sanitizeNumber(str(name['default']))
                            elif datatype == 'TEXT':
                                statement += '\'' + sanitizeMe(str(name['default'])) + '\''

                    statement += ','

                if not hasprimaryKey:
                    statement += "ID INTEGER PRIMARY KEY AUTOINCREMENT"
                    allTablePrimaries.append("ID")
                else:
                    statement = statement[:-1]



                #used for removing/appending semicolon at the end of the statement
                foreignRelationExisted = False

                #Handling relations
                try:
                    for foreignField in table['foreign-fields']:

                        foreignRelationExisted = True

                        getForeignPrimary = returnPrimary(username,sanitizeMe(foreignField['foreign-table']),data)
                        #get the primary key of the
                        foreignTablePrimary = getForeignPrimary[0]
                        foreignTablePrimaryType = getForeignPrimary[1]


                        if foreignField["relation-model"] == 'M-to-1':
                            statement += ',FOREIGN KEY ('

                            #adding current table's primary key
                            if not hasprimaryKey:
                                statement += "ID"
                            else:
                                statement += currentPrimary

                            statement += ') REFERENCES '+ username + '_' + sanitizeMe(foreignField["foreign-table"]) + '(' + foreignTablePrimary + ')'

                        #
                        # Creating intermediate table to ensure Many to Many relationship
                        # EX: if we want to create an intermediate table between A and B, we need to give a name for
                        # that table. The format will be:
                        # USERNAME + 'inter_' + X + '_' + Y
                        # where Y alphabetically comes after X
                        #
                        elif foreignField["relation-model"] == 'M-to-M':

                            intermediateCreateStatement = 'CREATE TABLE IF NOT EXISTS '

                            intermediateTable = username + '_inter_'

                            if sanitizeMe(foreignField["foreign-table"]) > sanitizeMe(table['name']):
                                intermediateTable += sanitizeMe(table['name']) + '_' + sanitizeMe(foreignField["foreign-table"])
                            else:
                                intermediateTable += sanitizeMe(foreignField["foreign-table"]) + '_' + sanitizeMe(table['name'])

                            #Adding intermediateTable to the list of tables
                            allTablePrimaries.append("")
                            allTableNames.append(intermediateTable)

                            #create the statement for intermediate table-later append it to statement
                            #Adding intermediate table's name to the statement
                            intermediateCreateStatement += intermediateTable + '('
                            A = sanitizeMe(table["name"])
                            idA = 'ID_' + A
                            typeA = currentPrimaryType
                            primA = 'ID'
                            if hasprimaryKey:
                                primA = currentPrimary

                            #All info for table B
                            B = sanitizeMe(foreignField["foreign-table"])
                            idB = 'ID_' + B
                            typeB = foreignTablePrimaryType
                            primB = foreignTablePrimary

                            #Adding the fields
                            intermediateCreateStatement +=  idA + ' ' + typeA + ', '
                            intermediateCreateStatement +=  idB + ' ' + typeB + ', '
                            intermediateCreateStatement +=  'FOREIGN KEY(' + idA + ') REFERENCES ' + A + '(' + primA + '), '
                            intermediateCreateStatement +=  'FOREIGN KEY(' + idB + ') REFERENCES ' + B + '(' + primB + ')'



                            #print(foreignField["foreign-table"] + '==' + foreignField["relation-model"])

                            intermediateCreateStatement += ');'
                            pass


                #foreign-fields may not be existed
                #it may also be occurred because a malicious file which doesn't have "relation-model" and/or "foreign-table"
                #So cleanup everything you need to
                except KeyError:
                    pass

                statement += ');'

            elif str(data['operation']) == 'update':
                print('UPDATE SELECTED')
            else:
                raise KeyError

        #Appending newly created user tables to tables_USERNAME

        #guaranteeing that we have table in server side. This can be optimized if we are sure that the table is existed
        statement += 'CREATE TABLE IF NOT EXISTS tables_' + username + '(TableName TEXT PRIMARY KEY, PrimaryName TEXT NULL);'
        #Adding intermediate tables
        statement += intermediateCreateStatement


        #Appending newly created tables into table_USERNAME
        number = len(allTableNames)
        for x in range(0,number):
            addNewlyCreatedTablesStatement += 'INSERT INTO ' + 'tables_' + username + ' VALUES(\'' + allTableNames[x] + '\',\'' + allTablePrimaries[x] + '\');'



        statement += addNewlyCreatedTablesStatement


        #CREATED SQL QUERY
        #print(statement)

        try:
            c.executescript(statement)
        #this happens when u try to insert a record that isn't unique but have unique constraint etc. Can be ignored
        #for test cases
        except sqlite3.IntegrityError:
                pass

        conn.close()

    except KeyError:
        pass