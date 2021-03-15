from fileshelper import FilesHelper
import unittest
import os

# Control + Shift + P
# Python: Configure Tests
# https://code-maven.com/slides/python/pytest-class

class FilesHelperTest(unittest.TestCase):
    
    def setUp(self):
        self.fileshelper = FilesHelper()
        self.create_file()
    
    def create_file(self):
        content = 'created from test'
        self.working_path = os.path.dirname(os.path.abspath(__file__)) +  '\\TestDirectory\\'
        self.backup_directory = os.path.dirname(os.path.abspath(__file__)) + "\\backups"
        self.test_file = self.working_path + "01ISIN45678912test.txt"
        result = self.fileshelper.create_file(content, self.test_file)

    def test_create_directory(self):
        result = self.fileshelper.create_directory(self.working_path)
        self.assertTrue(result)

       
    def test_backup_file(self):
         result = self.fileshelper.backup_file(self.test_file, self.backup_directory)
         self.assertTrue(result)

    def test_backup_file_error(self):
         self.assertRaises(FileNotFoundError,self.fileshelper.backup_file,'none','no_existe.txt')
         
    

