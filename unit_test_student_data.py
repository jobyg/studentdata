import unittest
import studentData
import pandas as pd
import numpy as np

class TestDataImport(unittest.TestCase):
    """
    Testing File
    """

    def test_data_fields(self):
        """
        Test the file header.
        This checks if we have all the field names we expect in data
        """
        incompleteData = {'student_id': [1, 2, 3, 4, 5],
        'score': [1, 2, 3, 4, 5.0],
        'grade': ['4', '3', 'K', '2', '1']}

        validData = {'student_id': [1, 2, 3, 4, 5],
        'score': [1, 2, 3, 4, 5.0],
        'grade': ['4', '3', 'K', '2', '1'],
        'test': ['reading', 'Reading', 'Math', 'math', 'Math'],
        'district': ['f', 'f', 't', 'true', 'TruE'] }

        # No data
        # We are unable to read data from the file
        res = studentData.data_import()
        self.assertEqual(isinstance(res ,pd.DataFrame),True)

        # Incomplete Data
        # data does not have all the fields we expect
        df = pd.DataFrame(incompleteData)
        res = studentData.data_import(df)
        self.assertNotEqual(isinstance(res, pd.DataFrame),True)

        # Valid Data
        df = pd.DataFrame(validData)
        res = studentData.data_import(df)
        self.assertEqual(isinstance(res, pd.DataFrame),True)

    def test_clean_testData(self):
        """
        Test the test data
        Data about test. I don't have the master subjects/test.Assuming all the data
        valid except null or blank
        TODO: Also I can put some checks if the data is normalized
        """
        validData = {'student_id': [1, 2, 3, 4, 5],
        'score': [1, 2, 3, 4, 5.0],
        'grade': ['4', '3', 'K', '2', '1'],
        'test': ['reading', 'Reading', 'Math', 'math', 'Math'],
        'district': ['f', 'f', 't', 'true', 'TruE'] }

        inValidData = {'student_id': [1, 2, 3, 4, 5],
        'score': [1, 2, 3, 4, 5.0],
        'grade': ['4', '3', 'K', '2', '1'],
        'test': ['reading', 'Reading', 'Math', '', 'Math'],
        'district': ['f', 'f', 't', 'true', 'TruE'] }

        # Invalid Data
        # conatains some blank data
        res = studentData.data_import(pd.DataFrame(inValidData))
        self.assertEqual(len(res), 4)

        # Valid Data
        res = studentData.data_import(pd.DataFrame(validData))
        self.assertEqual(len(res), 5)

    def test_clean_grade(self):
        """
        Test the grade data
        Assuming K and then 1-12 is valid data
        """
        validData = {'student_id': [1, 2, 3, 4, 5],
        'score': [1, 2, 3, 4, 5.0],
        'grade': ['4', '3', 'K', '2', '1'],
        'test': ['reading', 'Reading', 'Math', 'math', 'Math'],
        'district': ['f', 'f', 't', 'true', 'TruE'] }

        inValidData = {'student_id': [1, 2, 3, 4, 5],
        'score': [1, 2, 3, 4, 5.0],
        'grade': ['4', '3', 'K', '2', '13'],
        'test': ['reading', 'Reading', 'Math', 'ReAding', 'Math'],
        'district': ['f', 'f', 't', 'true', 'TruE'] }

        # Invalid Data
        res = studentData.data_import(pd.DataFrame(inValidData))
        self.assertEqual(len(res), 4)

        # Valid Data
        res = studentData.data_import(pd.DataFrame(validData))
        self.assertEqual(len(res), 5)

    def test_clean_score(self):
        """
        Test the score data
        Assuning valid scores are between 9 to 5.0
        """
        validData = {'student_id': [1, 2, 3, 4, 5],
        'score': [1, 2, 3, 4, 5.0],
        'grade': ['4', '3', 'K', '2', '1'],
        'test': ['reading', 'Reading', 'Math', 'math', 'Math'],
        'district': ['f', 'f', 't', 'true', 'TruE'] }

        inValidData = {'student_id': [1, 2, 3, 4, 5],
        'score': [1, 2, 5.3, 4, 5.0],
        'grade': ['4', '3', 'K', '2', '1'],
        'test': ['reading', 'Reading', 'Math', 'ReAding', 'Math'],
        'district': ['f', 'f', 't', 'true', 'TruE'] }

        # Invalid Data
        res = studentData.data_import(pd.DataFrame(inValidData))
        self.assertEqual(len(res), 4)

        # Valid Data
        res = studentData.data_import(pd.DataFrame(validData))
        self.assertEqual(len(res), 5)

    def test_duplicate_date(self):
        """
        Test the duplicate data
        Assuming student id, grade and test are keys to determine the unique record
        """
        validData = {'student_id': [1, 2, 3, 4, 5],
        'score': [1, 2, 3, 4, 5.0],
        'grade': ['4', '3', 'K', '2', '1'],
        'test': ['reading', 'Reading', 'Math', 'math', 'Math'],
        'district': ['f', 'f', 't', 'true', 'TruE'] }

        inValidData = {'student_id': [1, 1, 3, 4, 5],
        'score': [1, 2, 1.2, 4, 5.0],
        'grade': ['4', '4', 'K', '2', '1'],
        'test': ['reading', 'Reading', 'Math', 'ReAding', 'Math'],
        'district': ['f', 'f', 't', 'true', 'TruE'] }

        # Invalid Data
        res = studentData.data_import(pd.DataFrame(inValidData))
        self.assertEqual(len(res), 4)

        # Valid Data
        res = studentData.data_import(pd.DataFrame(validData))
        self.assertEqual(len(res), 5)

if __name__ == '__main__':
    unittest.main()