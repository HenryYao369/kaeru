import unittest
from GenerateTable import *

class TestGenerateMethods(unittest.TestCase):
    def test_sanitizeMe(self):
        self.assertEqual(sanitizeMe('-%323@\'.'),'323' )

    def test_sanitizeNumber(self):
        self.assertEqual(sanitizeNumber('-%323@\'.'),'323.' )

    # Testinf if a table is existed
    def test_checkIfExistedInRealTime(self):
        self.assertEqual(checkIfExistedInRealTime('anyUser_myMalicioustable6', False),['_username','TEXT'])

    # Testinf the result for non-existed table
    def test_checkIfExistedInRealTime_nonExistedTable(self):
        self.assertEqual(checkIfExistedInRealTime('NOTEXISTED', False),[])

    def test_getAllTableNames(self):
        self.assertEqual(getAllTableNames('anyUser', '-'),'anyUser_inter_myMalicioustable3_myMalicioustable6-anyUser_myMalicioustable3-anyUser_myMalicioustable4-anyUser_myMalicioustable6')

    # Testing if the function can find the primary key from the JSON file if not existed in database
    def test_returnPrimary_json(self):
        jsonfilename = 'example2.json'
        with open(jsonfilename) as data_file:
            self.assertEqual(returnPrimary('anyUser','testTable',json.load(data_file)),['username','TEXT'])

    # Testing if the function can find the primary key from the database (in case the table isn't existed in JSON file
    # but it is in db
    def test_returnPrimary_db(self):
        jsonfilename = 'example2.json'
        with open(jsonfilename) as data_file:
            self.assertEqual(returnPrimary('anyUser','myMalicioustable6',json.load(data_file)),['_username','TEXT'])

if __name__ == '__main__':
    #Executing main program to prepare the environment for testing
    processJSON('anyUser','example.db','example.json')
    unittest.main()